"""
router.py
The Geo Router. It calculates the geographic distance between the client
and available CDN nodes, then proxies the request to the nearest one.
"""

import time
import logging
import requests
import uvicorn
from fastapi import FastAPI, HTTPException
import config
from geo import calculate_distance

# Set up simple logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s INFO [ROUTER] %(message)s")

app = FastAPI(title="Geo Router")

@app.get("/health")
def health_check():
    return {"status": "healthy", "server": "Router"}

@app.get("/route")
def route_request(lat: float, lon: float, content_id: str):
    start_time = time.time()
    
    logging.info(f"Client request from: {lat}, {lon} for content {content_id}")
    
    # 1. Calculate distances
    dist_bangalore = calculate_distance(lat, lon, config.BANGALORE_COORDS[0], config.BANGALORE_COORDS[1])
    dist_north = calculate_distance(lat, lon, config.NORTH_CDN_COORDS[0], config.NORTH_CDN_COORDS[1])
    
    logging.info(f"Bangalore distance: {dist_bangalore} km")
    logging.info(f"North India distance: {dist_north} km")
    
    # 2. Select nearest CDN
    if dist_bangalore <= dist_north:
        selected_cdn_url = config.BANGALORE_CDN_URL
        selected_cdn_name = "Bangalore CDN"
    else:
        selected_cdn_url = config.NORTH_CDN_URL
        selected_cdn_name = "North India CDN"
        
    logging.info(f"Selected: {selected_cdn_name}")
    
    # 3. Forward request to selected CDN
    try:
        cdn_response = requests.get(f"{selected_cdn_url}/content/{content_id}", timeout=5)
        
        if cdn_response.status_code == 404:
            raise HTTPException(status_code=404, detail="Content not found")
        cdn_response.raise_for_status()
        
        data = cdn_response.json()
        
        end_time = time.time()
        total_time_ms = int((end_time - start_time) * 1000)
        
        # 4. Return formatted response to client
        return {
            "client_location": {"lat": lat, "lon": lon},
            "distances_km": {
                "Bangalore": dist_bangalore,
                "North_India": dist_north
            },
            "selected_cdn": selected_cdn_name,
            "cache_status": data.get("cache_status", "UNKNOWN"),
            "content": data.get("content", {}),
            "response_time_ms": total_time_ms
        }

    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to contact {selected_cdn_name}: {str(e)}")
        raise HTTPException(status_code=502, detail=f"CDN Unavailable: {selected_cdn_name}")

if __name__ == "__main__":
    print(f"Starting Router on port {config.ROUTER_PORT}...")
    uvicorn.run(app, host="127.0.0.1", port=config.ROUTER_PORT)