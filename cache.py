"""
cache.py
Implements a simple in-memory dictionary cache for the CDN edge servers.
"""

class SimpleCache:
    def __init__(self):
        # The dictionary storing our cached content
        self.store = {}
        # Statistics tracking
        self.hits = 0
        self.misses = 0

    def get(self, key: str):
        """Retrieve an item from the cache. Updates hit/miss stats."""
        if key in self.store:
            self.hits += 1
            return self.store[key]
        else:
            self.misses += 1
            return None

    def set(self, key: str, value: dict):
        """Store an item in the cache."""
        self.store[key] = value

    def exists(self, key: str) -> bool:
        """Check if an item exists in the cache without updating stats."""
        return key in self.store

    def clear(self):
        """Empty the cache and reset statistics."""
        self.store.clear()
        self.hits = 0
        self.misses = 0

    def stats(self) -> dict:
        """Return current cache statistics."""
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