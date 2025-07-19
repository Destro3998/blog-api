import time
import json
from functools import wraps
from collections import OrderedDict

class LRUCache:
    """Simple LRU Cache implementation"""
    
    def __init__(self, capacity=100):
        self.capacity = capacity
        self.cache = OrderedDict()
    
    def get(self, key):
        if key in self.cache:
            # Move to end (most recently used)
            self.cache.move_to_end(key)
            return self.cache[key]
        return None
    
    def put(self, key, value):
        if key in self.cache:
            # Move to end (most recently used)
            self.cache.move_to_end(key)
        else:
            if len(self.cache) >= self.capacity:
                # Remove least recently used item
                self.cache.popitem(last=False)
        self.cache[key] = value

# Global cache instance
cache = LRUCache(capacity=1000)

def cache_result(ttl=300):
    """Cache decorator with TTL"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            cache_key = f"{func.__name__}:{hash(str(args) + str(sorted(kwargs.items())))}"
            
            # Try to get from cache
            cached_result = cache.get(cache_key)
            if cached_result and time.time() < cached_result['expires']:
                return cached_result['data']
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache.put(cache_key, {
                'data': result,
                'expires': time.time() + ttl
            })
            
            return result
        return wrapper
    return decorator

def invalidate_cache(pattern=None):
    """Invalidate cache entries matching pattern"""
    if pattern:
        keys_to_remove = [key for key in cache.cache.keys() if pattern in key]
        for key in keys_to_remove:
            cache.cache.pop(key, None)
    else:
        cache.cache.clear()

def get_cache_stats():
    """Get cache statistics"""
    return {
        'size': len(cache.cache),
        'capacity': cache.capacity,
        'hit_rate': getattr(cache, 'hits', 0) / max(getattr(cache, 'total_requests', 1), 1)
    } 