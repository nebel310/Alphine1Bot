from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="📊 Анализ трат")
    builder.button(text="🎯 Цели накоплений")
    builder.button(text="💡 Финансовые советы")
    builder.button(text="🤖 О боте")
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)