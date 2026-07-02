import json
import hashlib
import redis

# Connect to the local Redis container running on port 6379
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def get_cache_key(prompt: str) -> str:
    """Hashes the prompt to create a unique, safe Redis key"""
    return hashlib.sha256(prompt.encode()).hexdigest()

def get_cached_response(prompt: str):
    try:
        key = get_cache_key(prompt)
        cached_data = redis_client.get(key)
        if cached_data:
            return json.loads(cached_data)
    except Exception as e:
        print(f"⚠️ Redis Error (Read): {e}")
    return None

def set_cached_response(prompt: str, response_data: dict, ttl_seconds: int = 3600):
    """Saves to Redis with a 1-hour expiration time (TTL)"""
    try:
        key = get_cache_key(prompt)
        redis_client.setex(key, ttl_seconds, json.dumps(response_data))
    except Exception as e:
        print(f"⚠️ Redis Error (Write): {e}")