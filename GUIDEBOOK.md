# GeoCDN Simulator Guidebook

> A hands-on simulator for understanding geographic CDN routing, caching, cache hits/misses, and latency.

## 1. Core Concepts

### What is a CDN?

A **Content Delivery Network (CDN)** is a group of geographically distributed servers that speeds up the delivery of web content by bringing copies of that content closer to users.

Instead of every request traveling to one central server, users can be served by a nearby **Edge Server**.

### Origin Server vs Edge Server

* **Origin Server** — The main server and source of truth for the content.
* **Edge Server (CDN)** — A server located closer to the user that temporarily stores copies of content from the Origin Server.

### Cache HIT vs Cache MISS

**Cache MISS**

The requested content is not available on the selected Edge Server.

```text
Client → Router → Nearest CDN → Cache MISS → Origin
       ← Router ← Nearest CDN ← Content ──────
```

The CDN must contact the Origin Server, resulting in higher latency.

**Cache HIT**

The requested content is already stored on the selected Edge Server.

```text
Client → Router → Nearest CDN → Cache HIT
       ← Router ← Nearest CDN
```

The Origin Server is bypassed, resulting in a much faster response.

---

## 2. Sequence of Events

### First Request — Cache MISS

When content is requested for the first time:

```text
Client
  ↓
Router
  ↓
Nearest CDN
  ↓
Content not in cache
  ↓
Origin Server
  ↓
Nearest CDN
  ↓
Client
```

**Result:** Slow response because the request has to reach the Origin Server.

### Second Request — Cache HIT

When the same content is requested again from the same CDN:

```text
Client
  ↓
Router
  ↓
Nearest CDN
  ↓
Content found in cache
  ↓
Client
```

**Result:** Very fast response because the Origin Server is not contacted.

---

## 3. How Geographic Routing Works

The simulator determines which CDN should handle a request based on the client's geographic location.

The client provides:

* Latitude
* Longitude

The Router calculates the distance between the client and each available CDN location.

### Haversine Formula

The simulator uses the **Haversine formula** to calculate the great-circle distance between two points on Earth.

The formula is useful because the Earth is approximately spherical.

Conceptually:

```text
Client Location
      │
      ├──────────────→ Bangalore CDN
      │                 Distance calculated
      │
      └──────────────→ North India CDN
                        Distance calculated
```

The Router selects the CDN with the shortest calculated distance.

### Example

For a client located in Chennai:

```text
Chennai
   │
   ├── Bangalore CDN    ≈ 290 km
   │
   └── North India CDN  ≈ much farther
```

Therefore, the Router selects the **Bangalore CDN**.

---

## 4. Project Architecture

The simulator consists of five processes:

```text
                    ┌──────────────────┐
                    │      Client      │
                    │      :8004       │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │      Router      │
                    │      :8003       │
                    └────────┬─────────┘
                             │
                    ┌────────┴─────────┐
                    ▼                  ▼
          ┌─────────────────┐  ┌─────────────────┐
          │ Bangalore CDN   │  │ North India CDN │
          │      :8001      │  │      :8002      │
          └────────┬────────┘  └────────┬────────┘
                   │                    │
                   └──────────┬─────────┘
                              ▼
                    ┌──────────────────┐
                    │  Origin Server   │
                    │      :8000       │
                    └──────────────────┘
```

Because all components run on the same physical computer, different **ports** are used to simulate separate servers.

| Component       |   Port | Responsibility               |
| --------------- | -----: | ---------------------------- |
| Origin Server   | `8000` | Stores the original content  |
| Bangalore CDN   | `8001` | Simulates an edge cache      |
| North India CDN | `8002` | Simulates another edge cache |
| Router          | `8003` | Selects the nearest CDN      |
| Client          | `8004` | Sends requests               |

---

## 5. Latency Simulation

A real local application can communicate between processes in less than a millisecond.

That would make the difference between a CDN cache HIT and MISS difficult to observe.

Therefore, the simulator artificially introduces delays using Python's `time.sleep()`.

### Simulated Latencies

```text
Origin Server
    ↓
~200 ms delay

CDN Server
    ↓
~20 ms delay
```

A cache MISS therefore takes significantly longer than a cache HIT.

For example:

```text
Cache MISS
Client → CDN → Origin → CDN → Client
             ~200 ms+
```

versus:

```text
Cache HIT
Client → CDN → Client
             ~20 ms
```

These delays are intentionally simulated for educational purposes.

---

# 6. Test Scenarios

## Scenario 1 — Geographic Routing

### Objective

Verify that the Router selects the CDN geographically closest to the client.

### Test

Select:

```text
Location: Chennai
```

The Router should calculate distances and select:

```text
Bangalore CDN
```

Expected output:

```text
Bangalore: ~290 km
```

---

## Scenario 2 — North India Routing

### Objective

Verify routing for a client located near the North India CDN.

### Test

Select:

```text
Location: Delhi
```

The Router should select:

```text
North India CDN
```

Expected output:

```text
North India: 0.0 km
```

The exact distance may depend on the coordinates configured in the simulator.

---

## Scenario 3 — Cache MISS → Cache HIT

### Objective

Observe how caching improves response time.

### Step 1 — Request Content `101`

Select:

```text
Location: Chennai
Content ID: 101
```

Expected:

```text
CDN: Bangalore
Cache Status: [MISS]
Response Time: ~240 ms
```

The content is not yet stored in the Bangalore CDN cache.

The request therefore goes to the Origin Server.

### Step 2 — Request Content `101` Again

Keep the location as:

```text
Chennai
```

Request:

```text
Content ID: 101
```

Expected:

```text
CDN: Bangalore
Cache Status: [HIT]
Response Time: ~20–30 ms
```

The Bangalore CDN now has content `101` cached.

The Origin Server is bypassed.

---

## Scenario 4 — Cache Isolation

### Objective

Demonstrate that different Edge Servers maintain independent caches.

### Step 1

Request:

```text
Location: Chennai
Content ID: 101
```

This populates:

```text
Bangalore CDN cache
```

### Step 2

Change the location to:

```text
Delhi
```

Request:

```text
Content ID: 101
```

Expected:

```text
CDN: North India
Cache Status: [MISS]
Response Time: ~240 ms
```

### Why is it a MISS?

Because the caches are independent.

The content exists in:

```text
Bangalore CDN
```

but not in:

```text
North India CDN
```

Therefore, the North India CDN must contact the Origin Server.

---

# 7. Real World vs Simulator

This project is an educational simulation rather than a production CDN.

| Simulator               | Real CDN                                           |
| ----------------------- | -------------------------------------------------- |
| Python Router           | DNS, Anycast, BGP, load balancing, etc.            |
| Python dictionary cache | Redis, Memcached, SSD/RAM-based caching systems    |
| Local processes         | Globally distributed physical/cloud infrastructure |
| Different ports         | Different servers/regions/PoPs                     |
| `time.sleep()` latency  | Actual network latency                             |
| Haversine routing       | More sophisticated traffic and routing systems     |

Real CDN providers such as Cloudflare and AWS CloudFront use highly distributed infrastructure and sophisticated routing, caching, security, and traffic-management systems.

The simulator simplifies these mechanisms so their core behavior can be observed directly.

---

# 8. How to Run

## Prerequisites

Make sure Python is installed.

Verify it with:

```cmd
python --version
```

If `python` is not available but the Python launcher is installed, you can also check:

```cmd
py --version
```

---

## Step 1 — Create a Virtual Environment

Open a terminal in the project directory:

```cmd
python -m venv venv
```

Activate it:

```cmd
venv\Scripts\activate
```

If activation succeeds, your terminal should show something similar to:

```text
(venv) C:\path\to\GeoCDN>
```

---

## Step 2 — Install Dependencies

Run:

```cmd
pip install -r requirements.txt
```

---

## Step 3 — Open Five Terminals

Open **five separate Command Prompt or PowerShell windows**.

Make sure each terminal is inside the project directory.

Activate the virtual environment in each terminal:

```cmd
venv\Scripts\activate
```

---

## Terminal 1 — Origin Server

```cmd
venv\Scripts\activate
python origin_server.py
```

The Origin Server should start on:

```text
http://localhost:8000
```

---

## Terminal 2 — Bangalore CDN

```cmd
venv\Scripts\activate
python bangalore_cdn.py
```

The Bangalore CDN should start on:

```text
http://localhost:8001
```

---

## Terminal 3 — North India CDN

```cmd
venv\Scripts\activate
python north_cdn.py
```

The North India CDN should start on:

```text
http://localhost:8002
```

---

## Terminal 4 — Router

```cmd
venv\Scripts\activate
python router.py
```

The Router should start on:

```text
http://localhost:8003
```

---

## Terminal 5 — Client

```cmd
venv\Scripts\activate
python client.py
```

The client interface should now appear.

---

# 9. First Demonstration

Follow these steps in order.

## Step 1 — Request From Chennai

In **Terminal 5**, select:

```text
2
```

for:

```text
Chennai
```

Then enter:

```text
101
```

as the Content ID.

### Expected Behavior

The Router calculates the distance to each CDN.

You should see something similar to:

```text
Bangalore: 290 km
```

The request should be routed to:

```text
Bangalore CDN
```

Because content `101` has not previously been requested:

```text
Cache Status: [MISS]
```

The request must reach the Origin Server.

Expected response time:

```text
~240 ms
```

---

## Step 2 — Request From Delhi

When the client menu appears again, select:

```text
4
```

for:

```text
Delhi
```

Then request:

```text
101
```

### Expected Behavior

The Router should select:

```text
North India CDN
```

because it is closest to Delhi.

You should see approximately:

```text
North India: 0.0 km
```

The cache status should be:

```text
[MISS]
```

Even though content `101` was previously requested from Chennai, that request populated the **Bangalore CDN cache**, not the North India CDN cache.

Expected response time:

```text
~240 ms
```

---

## Step 3 — Request From Chennai Again

Select:

```text
2
```

for:

```text
Chennai
```

Then enter:

```text
101
```

again.

### Expected Behavior

The Router selects:

```text
Bangalore CDN
```

The Bangalore CDN already has content `101`.

Therefore:

```text
Cache Status: [HIT]
```

The Origin Server is bypassed.

Expected response time:

```text
~20–30 ms
```

---

# 10. Expected Demonstration Flow

The complete demonstration should look conceptually like this:

```text
┌─────────────────────────────────────────────┐
│ 1. Chennai → Content 101                   │
│                                             │
│ Router → Bangalore CDN                     │
│ Cache → MISS                                │
│ Origin → Fetch content                      │
│ Response → ~240 ms                          │
└─────────────────────────────────────────────┘
                     │
                     ▼
          Content 101 cached
          in Bangalore CDN
                     │
                     ▼
┌─────────────────────────────────────────────┐
│ 2. Delhi → Content 101                     │
│                                             │
│ Router → North India CDN                   │
│ Cache → MISS                                │
│ Origin → Fetch content                      │
│ Response → ~240 ms                          │
└─────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────┐
│ 3. Chennai → Content 101                   │
│                                             │
│ Router → Bangalore CDN                     │
│ Cache → HIT                                 │
│ Origin → Bypassed                            │
│ Response → ~20–30 ms                        │
└─────────────────────────────────────────────┘
```

This demonstrates two important CDN concepts:

1. **Geographic routing**
2. **Edge caching**

---

# 11. What You Should Observe

During the demonstration, pay attention to these four things:

### 1. CDN Selection

The Router should select the CDN based on geographic distance.

### 2. Cache Status

A new request should produce:

```text
[MISS]
```

A repeated request from the same CDN should produce:

```text
[HIT]
```

### 3. Response Time

A MISS should be significantly slower:

```text
~240 ms
```

A HIT should be much faster:

```text
~20–30 ms
```

### 4. Cache Isolation

A cached object on one Edge Server should not automatically appear on another Edge Server.

For example:

```text
Bangalore CDN
└── 101 ✓

North India CDN
└── 101 ✗
```

This explains why the Delhi request still produces a cache MISS.

---

# 12. Key Takeaways

After completing the demonstration, you should understand:

* What a CDN is.
* Why CDNs use geographically distributed Edge Servers.
* The difference between an Origin Server and an Edge Server.
* What a cache HIT means.
* What a cache MISS means.
* How geographic routing can select a nearby CDN.
* How the Haversine formula can calculate geographic distance.
* Why cache HITs are faster than cache MISSes.
* Why separate CDN locations can have independent caches.
* How a CDN reduces the number of requests reaching the Origin Server.
* How a real CDN differs from this simplified simulator.

---

# 13. One-Line Mental Model

The entire project can be understood with this simple flow:

```text
Find the nearest CDN
        ↓
Check its cache
        ↓
    ┌───┴───┐
    │       │
   HIT     MISS
    │       │
    ▼       ▼
 Serve    Ask Origin
    │       │
    │       ▼
    │     Cache
    │       │
    └───┬───┘
        ▼
      Client
```

**Nearest CDN + caching = faster content delivery.**
