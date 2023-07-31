from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Предметы"),
            KeyboardButton(text="Список группы")
        ],
        [
            KeyboardButton(text="Расписание (преп.)"),
            KeyboardButton(text="Расписание (студ.)")
        ],
        [
            KeyboardButton(text="Контакты (преп.)"),
            KeyboardButton(text="Др. инф-ия"),
        ],
        [
            KeyboardButton(text="Куда идти")
        ]
    ],
    resize_keyboard=True
)


