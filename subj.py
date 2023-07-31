from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

subj = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Вычи"),
            KeyboardButton(text="МОиВИ")
        ],
        [
            KeyboardButton(text="Русcкий"),
            KeyboardButton(text="Тервер")
        ],
        [
            KeyboardButton(text="Физика"),
            KeyboardButton(text="Терупр")
        ],
        [
            KeyboardButton(text="Практика"),
            KeyboardButton(text="КуР")
        ],
    ],
    resize_keyboard=True
)