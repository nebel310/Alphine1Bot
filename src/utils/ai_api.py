import json
import hashlib
import aiohttp
from config import OPENROUTER_API_KEY, MODEL_NAME
from functools import lru_cache

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

@lru_cache(maxsize=100)
def _hash_prompt(prompt: str) -> str:
    return hashlib.md5(prompt.encode()).hexdigest()

async def get_ai_response(prompt: str, system_prompt: str) -> str:
    cache_key = _hash_prompt(f"{system_prompt}{prompt}")
    if cached := get_ai_response.cache.get(cache_key):
        return cached

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(OPENROUTER_URL, headers=headers, json=payload) as response:
            if response.status != 200:
                error = await response.text()
                return f"🚫 Ошибка: {response.status} {error}"

            data = await response.json()
            return data['choices'][0]['message']['content']

# Кеш в памяти
get_ai_response.cache = {}