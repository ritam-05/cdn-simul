"""
origin_server.py
Simulates the main backend/database server. It holds the source of truth for all content.
"""

import time
import uvicorn
from fastapi import FastAPI, HTTPException
import config

app = FastAPI(title="Origin Server")

# In-memory "Database"
CONTENT_DB = {
    "101": {
        "id": "101",
        "title": "CDN Demo Content",
        "message": "Hello from the Origin Server! This is the source of truth."
    },
    "102": {
        "id": "102",
        "title": "Python Distributed Systems",
        "message": "Learning how routing and caching works in a CDN."
    },
    "103": {
        "id": "103",
        "title": "Geographic Routing Guide",
        "message": "Latency is reduced by serving content closer to the user."
    }
}

@app.get("/health")
def health_check():
    return {"status": "healthy", "server": "Origin"}

@app.get("/content/{content_id}")
def get_content(content_id: str):
    # Simulate high latency (network distance / DB query time)
    time.sleep(config.ORIGIN_LATENCY)
    
    if content_id not in CONTENT_DB:
        raise HTTPException(status_code=404, detail="Content not found on Origin")
        
    return {
        "content": CONTENT_DB[content_id],
        "served_by": "Origin Server",
        "timestamp": time.time()
    }

if __name__ == "__main__":
    print(f"Starting Origin Server on port {config.ORIGIN_PORT}...")
    uvicorn.run(app, host="127.0.0.1", port=config.ORIGIN_PORT)