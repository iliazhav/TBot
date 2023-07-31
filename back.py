from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

back = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="/menu")
        ],
    ],
    resize_keyboard=True
)