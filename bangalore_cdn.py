"""
bangalore_cdn.py
Simulates a CDN Edge Server located in Bangalore, South India.
Includes TTL cache handling and Origin Fallback logic.
"""

import time
import requests
import uvicorn
from fastapi import FastAPI, HTTPException
import config
from cache import SimpleCache

app = FastAPI(title="Bangalore CDN")
cdn_cache = SimpleCache()

@app.get("/health")
def health_check():
    return {"status": "healthy", "server": "Bangalore CDN"}

@app.get("/content/{content_id}")
def get_content(content_id: str):
    # Simulate small edge server processing latency
    time.sleep(config.CDN_LATENCY)
    
    # 1. Check Cache (TTL logic is handled inside cache.py)
    cached_data = cdn_cache.get(content_id)
    if cached_data:
        return {
            "content": cached_data["content"],
            "served_by": app.title, 
            "cache_status": "HIT"
        }
        
    # 2. CACHE MISS -> Fetch from Origin with Fallback Logic
    try:
        # ATTEMPT 1: Primary Origin
        origin_response = requests.get(f"{config.ORIGIN_URL}/content/{content_id}", timeout=2)
        if origin_response.status_code == 404:
            raise HTTPException(status_code=404, detail="Content not found")
        origin_response.raise_for_status()
        data = origin_response.json()
        
    except HTTPException:
        raise  # Pass through the 404 instantly
    except requests.exceptions.RequestException as e:
        print(f"[{app.title}] Primary Origin offline. Triggering Fallback...")
        
        try:
            # ATTEMPT 2: Fallback Origin
            origin_response = requests.get(f"{config.ORIGIN_FALLBACK_URL}/content/{content_id}", timeout=2)
            if origin_response.status_code == 404:
                raise HTTPException(status_code=404, detail="Content not found")
            origin_response.raise_for_status()
            data = origin_response.json()
            
        except requests.exceptions.RequestException:
            # BOTH Origins are down
            raise HTTPException(status_code=502, detail="CDN Error: Both Primary and Fallback Origins are offline.")

    # 3. Store in cache (sets the new TTL)
    cdn_cache.set(content_id, data)
    
    return {
        "content": data["content"],
        "served_by": app.title,
        "cache_status": "MISS"
    }

@app.get("/cache/stats")
def get_cache_stats():
    return cdn_cache.stats()

@app.get("/cache/clear")
def clear_cache():
    cdn_cache.clear()
    return {"message": "Bangalore CDN cache cleared."}

if __name__ == "__main__":
    print(f"Starting Bangalore CDN on port {config.BANGALORE_CDN_PORT}...")
    uvicorn.run(app, host="127.0.0.1", port=config.BANGALORE_CDN_PORT)