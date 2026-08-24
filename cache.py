"""
cache.py
Implements an in-memory dictionary cache with TTL (Time To Live).
"""
import time
import config

class SimpleCache:
    def __init__(self):
        self.store = {}
        self.hits = 0
        self.misses = 0

    def get(self, key: str):
        """Retrieve an item. Returns None if missing OR expired."""
        if key in self.store:
            entry = self.store[key]
            
            # Check if TTL has expired
            if time.time() < entry['expires_at']:
                self.hits += 1
                return entry['data']
            else:
                # Data is expired - remove it
                del self.store[key]
                
        self.misses += 1
        return None

    def set(self, key: str, value: dict):
        """Store an item with an expiration timestamp."""
        self.store[key] = {
            'data': value,
            'expires_at': time.time() + config.CACHE_TTL_SECONDS
        }

    def exists(self, key: str) -> bool:
        if key in self.store:
            if time.time() < self.store[key]['expires_at']:
                return True
            else:
                del self.store[key]
        return False

    def clear(self):
        self.store.clear()
        self.hits = 0
        self.misses = 0

    def stats(self) -> dict:
        total_requests = self.hits + self.misses
        hit_ratio = 0.0
        if total_requests > 0:
            hit_ratio = round((self.hits / total_requests) * 100, 2)
            
        return {
            "total_items": len(self.store),
            "hits": self.hits,
            "misses": self.misses,
            "hit_ratio_percent": hit_ratio
        }