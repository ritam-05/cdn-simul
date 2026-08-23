"""
config.py
Centralized configuration for the GeoCDN Simulator.
Contains URLs, ports, and geographic coordinates for our servers.
"""

# Origin Server Configuration
ORIGIN_PORT = 8000
ORIGIN_URL = f"http://127.0.0.1:{ORIGIN_PORT}"

# Bangalore CDN Configuration
BANGALORE_CDN_PORT = 8001
BANGALORE_CDN_URL = f"http://127.0.0.1:{BANGALORE_CDN_PORT}"
BANGALORE_COORDS = (12.9716, 77.5946) # Latitude, Longitude

# North India CDN Configuration
NORTH_CDN_PORT = 8002
NORTH_CDN_URL = f"http://127.0.0.1:{NORTH_CDN_PORT}"
NORTH_CDN_COORDS = (28.6139, 77.2090) # Latitude, Longitude (Delhi)

# Router Configuration
ROUTER_PORT = 8003
ROUTER_URL = f"http://127.0.0.1:{ROUTER_PORT}"

# Simulated Latencies (in seconds)
ORIGIN_LATENCY = 0.2    # 200ms simulating heavy DB query/distance
CDN_LATENCY = 0.02      # 20ms simulating edge server speed