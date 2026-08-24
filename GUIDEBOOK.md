# CDN Simulator Guidebook

> A hands-on simulator for understanding geographic CDN routing, caching, TTL expiration, cache isolation, and origin failover.

## 1. Core Concepts

### What is a CDN?

A Content Delivery Network (CDN) is a group of geographically distributed servers that speeds up content delivery by serving users from locations closer to them.

### Origin Server vs Edge Server

- Origin Server: The source of truth for the content.
- Edge Server (CDN): A nearby server that stores temporary copies of content.

### Cache HIT vs Cache MISS

Cache MISS:

```text
Client -> Router -> Nearest CDN -> Cache MISS -> Origin
       <- Router <- Nearest CDN <- Content
```

The CDN must contact an origin server, so the response is slower.

Cache HIT:

```text
Client -> Router -> Nearest CDN -> Cache HIT
       <- Router <- Nearest CDN
```

The content is already cached, so the response is much faster.

### Cache TTL

Each CDN cache entry has a Time To Live (TTL). In this project, cached content expires after `60` seconds. Once expired, the next request behaves like a cache miss and refreshes the cached value from an origin server.

### Origin Fallback

If the primary origin is unavailable, the CDN tries a fallback origin before returning an error. This keeps the simulator available even when the main origin is offline.

---

## 2. Project Architecture

The simulator consists of six processes:

```text
Client -> Router -> Nearest CDN -> Primary Origin
                                -> Fallback Origin
```

Default ports:

| Component | Port | Responsibility |
| --- | ---: | --- |
| Primary Origin | `8000` | Main content source |
| Bangalore CDN | `8001` | South India edge cache |
| North India CDN | `8002` | North India edge cache |
| Router | `8003` | Selects the nearest CDN |
| Fallback Origin | `8004` | Backup content source |
| Client | local CLI | Sends requests |

Because all components run on the same machine, different ports simulate different services.

---

## 3. How Geographic Routing Works

The client sends:

- Latitude
- Longitude
- Content ID

The router calculates the distance from the client to each CDN location using the Haversine formula and selects the nearest one.

Example:

- Chennai is usually routed to Bangalore CDN.
- Delhi is usually routed to North India CDN.

---

## 4. Request Flow

### First Request

```text
Client
  |
Router
  |
Nearest CDN
  |
Cache MISS
  |
Primary Origin or Fallback Origin
  |
CDN stores response in cache
  |
Client
```

### Repeated Request Before TTL Expiry

```text
Client
  |
Router
  |
Nearest CDN
  |
Cache HIT
  |
Client
```

### Request After TTL Expiry

```text
Client
  |
Router
  |
Nearest CDN
  |
Expired cache entry removed
  |
Cache MISS
  |
Origin fetch
```

---

## 5. Latency Simulation

The simulator intentionally adds delays so cache behavior is easy to observe.

- Origin latency: about `200 ms`
- CDN latency: about `20 ms`

That means:

- A cache miss is noticeably slower.
- A cache hit is noticeably faster.

---

## 6. How to Run

### Step 1: Create and activate a virtual environment

```cmd
python -m venv venv
venv\Scripts\activate
```

### Step 2: Install dependencies

```cmd
pip install -r requirements.txt
```

### Step 3: Start the services

Open separate terminals and run:

```cmd
python origin_server.py
```

```cmd
python bangalore_cdn.py
```

```cmd
python north_cdn.py
```

```cmd
python router.py
```

```cmd
python origin_fallback.py
```

```cmd
python client.py
```

---

## 7. Test Scenarios

### Scenario 1: Geographic Routing

Request content `101` from Chennai. The router should usually choose Bangalore CDN.

Request content `101` from Delhi. The router should usually choose North India CDN.

### Scenario 2: Cache MISS -> HIT

1. Request content `101` from Chennai.
2. Request content `101` again from Chennai.

Expected:

- First request: `MISS`
- Second request: `HIT`

### Scenario 3: TTL Expiration

1. Request content `101` from Chennai.
2. Wait more than `60` seconds.
3. Request content `101` again from Chennai.

Expected:

- The cached item expires.
- The later request becomes a `MISS` again.

### Scenario 4: Cache Isolation

1. Request content `101` from Chennai.
2. Request content `101` from Delhi.

Expected:

- Bangalore CDN may have the item cached.
- North India CDN still starts with its own cache state.

### Scenario 5: Fallback Origin

1. Stop `origin_server.py`.
2. Keep `origin_fallback.py` running.
3. Request an existing content ID.

Expected:

- The CDN should fetch from the fallback origin.
- The response content should indicate backup-origin data.

---

## 8. Real World vs Simulator

| Simulator | Real CDN |
| --- | --- |
| Python router | DNS, Anycast, BGP, load balancing |
| In-memory dictionary cache | Redis, Memcached, SSD/RAM caches |
| Local processes | Distributed global infrastructure |
| Fixed TTL in config | Dynamic caching rules and policies |
| Fallback origin process | Multi-origin or failover infrastructure |
| Simulated latency | Real network latency |

This simulator is intentionally simple so the core CDN ideas are easy to observe.

---

## 9. Key Takeaways

- The router sends users to the nearest CDN based on coordinates.
- Each CDN maintains its own cache.
- Cache hits are faster than cache misses.
- Cached data expires after the configured TTL.
- If the primary origin is down, the CDN can fall back to a backup origin.
