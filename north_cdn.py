"""
north_cdn.py
Simulates a CDN Edge Server located in Delhi, North India.
It has an identical structure to Bangalore CDN, but maintains its own independent cache.
"""

import time
import requests
import uvicorn
from fastapi import FastAPI, HTTPException
import config
from cache import SimpleCache

app = FastAPI(title="North India CDN")
cdn_cache = SimpleCache()

@app.get("/health")
def health_check():
    return {"status": "healthy", "server": "North India CDN"}

@app.get("/content/{content_id}")
def get_content(content_id: str):
    # Simulate small edge server processing latency
    time.sleep(config.CDN_LATENCY)
    
    # 1. Check Cache
    cached_data = cdn_cache.get(content_id)
    
    if cached_data:
        # CACHE HIT
        return {
            "content": cached_data["content"],
            "served_by": "North India CDN",
            "cache_status": "HIT"
        }
        
    # 2. CACHE MISS -> Fetch from Origin
    try:
        origin_response = requests.get(f"{config.ORIGIN_URL}/content/{content_id}", timeout=5)
        if origin_response.status_code == 404:
            raise HTTPException(status_code=404, detail="Content not found")
        origin_response.raise_for_status()
        
        data = origin_response.json()
        
        # 3. Store in cache for future requests
        cdn_cache.set(content_id, data)
        
        return {
            "content": data["content"],
            "served_by": "North India CDN",
            "cache_status": "MISS"
        }
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error contacting Origin: {str(e)}")

@app.get("/cache/stats")
def get_cache_stats():
    return cdn_cache.stats()

@app.get("/cache/clear")
def clear_cache():
    cdn_cache.clear()
    return {"message": "North India CDN cache cleared."}

if __name__ == "__main__":
    print(f"Starting North India CDN on port {config.NORTH_CDN_PORT}...")
    uvicorn.run(app, host="127.0.0.1", port=config.NORTH_CDN_PORT)