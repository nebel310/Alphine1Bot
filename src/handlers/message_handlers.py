from aiogram import Router, types, F
from aiogram.filters import Command
from utils.telegram_helpers import safe_reply
from utils.ai_api import get_ai_response
from keyboards.reply import get_main_keyboard
from prompts import SYSTEM_PROMPT, expense_analysis_prompt, money_question_prompt
import re

router = Router()

@router.message(Command("start"))
async def start(message: types.Message):
    welcome = (
        "Прикинь, я Альфин! Твой финансовый бро от Альфа-Банка 💸\n\n"
        "Чем могу помочь?\n"
        "• Скинь трату — разберу по косточкам\n"
        "• Спроси про деньги — отвечу без заморочек\n"
        "• Хочешь копить? Легко! 💰\n\n"
        "Давай дружить, бро!"
    )
    await safe_reply(message, welcome, reply_markup=get_main_keyboard())

@router.message(F.text == "📊 Анализ трат")
async def expense_analysis(message: types.Message):
    await safe_reply(message, "Кидай свою трату, брат! Любой формат — я все съем 🍽️")

@router.message(F.text == "🎯 Цели накоплений")
async def savings_goal(message: types.Message):
    await safe_reply(message, "Чё копим? Айфон? Тачку? Домик в Сочи? Скидывай цифры — составим план! ✨")

@router.message(lambda message: message.text and re.search(r'(трат|потратил|купил|покуп|счет|деньги|рубл|тенг)', message.text.lower()))
async def handle_expense(message: types.Message):
    prompt = expense_analysis_prompt(message.text)
    response = await get_ai_response(prompt, SYSTEM_PROMPT)
    await safe_reply(message, f"🔍 Разбор полётов:\n\n{response}")

@router.message(lambda message: message.text and re.search(r'(\?|почему|как|стоит|экономи|совет|копить)', message.text.lower()))
async def handle_money_question(message: types.Message):
    prompt = money_question_prompt(message.text)
    response = await get_ai_response(prompt, SYSTEM_PROMPT)
    await safe_reply(message, f"💡 Мой вердикт:\n\n{response}")

@router.message()
async def generic_handler(message: types.Message):
    if message.text:
        # Для коротких сообщений используем общий промпт
        if len(message.text) < 50:
            response = await get_ai_response(message.text, SYSTEM_PROMPT)
            await safe_reply(message, response)
        else:
            # Для длинных - обработка как траты
            prompt = expense_analysis_prompt(message.text)
            response = await get_ai_response(prompt, SYSTEM_PROMPT)
            await safe_reply(message, f"🔍 Разбор полётов:\n\n{response}")
    else:
        await message.answer("Братан, я пока только текст понимаю 😅")