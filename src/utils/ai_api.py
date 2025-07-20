import aiohttp
import json
import hashlib
import asyncio
from config import OPENROUTER_API_KEY, MODEL_NAME
from functools import lru_cache

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

async def get_ai_response(prompt: str, system_prompt: str) -> str:
    """Асинхронно получает ответ от AI с обработкой ошибок и кешированием"""
    # Создаем уникальный ключ для кеширования
    cache_key = f"{system_prompt[:50]}_{prompt[:100]}"
    cache_key = hashlib.md5(cache_key.encode()).hexdigest()
    
    # Проверка кеша
    if cache_key in get_ai_response.cache:
        return get_ai_response.cache[cache_key]
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt[:1500]},  # Ограничиваем длину
            {"role": "user", "content": prompt[:1000]}            # Ограничиваем длину
        ],
        "temperature": 0.7,
        "max_tokens": 600  # Ограничиваем длину ответа
    }
    
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=30)) as session:
            async with session.post(OPENROUTER_URL, headers=headers, json=payload) as response:
                if response.status == 429:
                    return "⚠️ Упс, я сегодня слишком много запросов сделал! Попробуй через минуту, брат!"
                
                if response.status != 200:
                    error = await response.text()
                    return f"🚫 Ошибка {response.status}: {error[:200]}"
                
                data = await response.json()
                response_text = data['choices'][0]['message']['content']
                
                # Сохраняем в кеш
                get_ai_response.cache[cache_key] = response_text
                return response_text
    
    except asyncio.TimeoutError:
        return "⏳ Сервер долго не отвечает, попробуй ещё раз позже!"
    except Exception as e:
        return f"🔥 Критическая ошибка: {str(e)}"

# Инициализируем кеш
get_ai_response.cache = {}