# CDN Simulator

A beginner-friendly, Python-based simulator that shows how a Content Delivery Network (CDN) uses geographic routing, edge caching, cache expiration, and origin failover to serve content faster and more reliably.

## What this project does

This project simulates a small CDN setup. Instead of contacting the origin directly, the client sends a request to the router. The router compares the client's coordinates against available edge locations and forwards the request to the nearest CDN node.

Each CDN node:

- Maintains its own in-memory cache
- Returns fast responses on cache hits
- Expires cached entries after a TTL
- Falls back to a backup origin if the primary origin is unavailable

## Architecture

```text
                 +----------------------+
                 | Primary Origin :8000 |
                 +----------+-----------+
                            |
                 +----------v-----------+
                 | Fallback Origin:8004 |
                 +----------------------+

      +-------------------+     +--------------------+
      | Bangalore CDN     |     | North India CDN    |
      | :8001             |     | :8002              |
      +---------+---------+     +---------+----------+
                \                         /
                 \                       /
                  +----------+----------+
                             |
                     +-------v-------+
                     | Router :8003  |
                     +-------+-------+
                             |
                     +-------v-------+
                     | CLI Client    |
                     +---------------+
```

## Features

- Geographic routing using the Haversine formula
- Independent edge caches for each CDN node
- TTL-based cache expiration
- Primary origin plus fallback origin support
- Simulated latency to make HIT vs MISS behavior easy to observe
- Interactive CLI with predefined Indian cities and custom coordinates

## Tech Stack

- Python 3.10+
- FastAPI
- Uvicorn
- Requests

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate it:
   ```bash
   venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Run the Simulator

Open five terminals for the services and one more for the client. Activate the virtual environment in each terminal first.

1. Start the primary origin:
   ```bash
   python origin_server.py
   ```
2. Start the Bangalore CDN:
   ```bash
   python bangalore_cdn.py
   ```
3. Start the North India CDN:
   ```bash
   python north_cdn.py
   ```
4. Start the router:
   ```bash
   python router.py
   ```
5. Start the fallback origin:
   ```bash
   python origin_fallback.py
   ```
6. In a separate terminal, start the client:
   ```bash
   python client.py
   ```

## Default Ports

| Component | Port |
| --- | ---: |
| Primary Origin | `8000` |
| Bangalore CDN | `8001` |
| North India CDN | `8002` |
| Router | `8003` |
| Fallback Origin | `8004` |

## Example Demo Flow

1. Request content `101` from Chennai. The router should choose Bangalore and return a cache `MISS`.
2. Request content `101` again from Chennai. The router should again choose Bangalore, but this time return a cache `HIT`.
3. Wait more than `60` seconds and request `101` again from Chennai. The cached entry should expire and produce another `MISS`.
4. Stop `origin_server.py` and request content again. The CDN should fetch from `origin_fallback.py` if it is running.

## Notes

- Cache TTL is currently `60` seconds in [config.py](C:/Users/ritam/Desktop/work/projects/cdn-simul/config.py).
- The fallback origin returns the same sample content, but its messages are marked as backup content.
- This is an educational simulator, not a production CDN implementation.
