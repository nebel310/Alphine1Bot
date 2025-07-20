import re
from aiogram import types
from .text_processing import split_text

async def safe_reply(message: types.Message, text: str, **kwargs):
    """Отправка сообщения с обработкой markdown и разбивкой"""
    # Чистим проблемные символы
    clean_text = re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', text)
    
    # Разбиваем длинные сообщения
    for part in split_text(clean_text):
        try:
            await message.answer(part, parse_mode='MarkdownV2', **kwargs)
        except Exception:
            # Fallback без markdown
            clean_part = re.sub(r'\\([_*\[\]()~`>#+\-=|{}.!])', r'\1', part)
            await message.answer(clean_part, **kwargs)