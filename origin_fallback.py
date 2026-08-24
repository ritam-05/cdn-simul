"""
origin_fallback.py
Acts as the backup database if the Primary Origin goes offline.
"""
import time
import uvicorn
from fastapi import FastAPI, HTTPException
import config

app = FastAPI(title="Fallback Origin Server")

# Identical DB, but messages indicate it came from the fallback
CONTENT_DB = {
    "101": {"id": "101", "title": "CDN Demo Content", "message": "[BACKUP] Hello from the Fallback Origin!"},
    "102": {"id": "102", "title": "Python Distributed Systems", "message": "[BACKUP] Learning routing and caching."},
    "103": {"id": "103", "title": "Geographic Routing Guide", "message": "[BACKUP] Latency is reduced locally."}
}

@app.get("/health")
def health_check():
    return {"status": "healthy", "server": "Fallback Origin"}

@app.get("/content/{content_id}")
def get_content(content_id: str):
    time.sleep(config.ORIGIN_LATENCY)
    if content_id not in CONTENT_DB:
        raise HTTPException(status_code=404, detail="Content not found on Fallback Origin")
    return {
        "content": CONTENT_DB[content_id],
        "served_by": "Fallback Origin Server",
        "timestamp": time.time()
    }

if __name__ == "__main__":
    print(f"Starting Fallback Origin on port {config.ORIGIN_FALLBACK_PORT}...")
    uvicorn.run(app, host="127.0.0.1", port=config.ORIGIN_FALLBACK_PORT)