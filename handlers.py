import random

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, Command
from aiogram.types import Message, ContentType
from asyncpg import Connection, Record
from asyncpg.exceptions import UniqueViolationError
from pip._internal.utils import datetime

from load_all import bot, dp, db
from back import back
from subj import subj

from menu import menu
from test import Test


class DBCommands:
    pool: Connection = db
    ADD_NEW_USER_REFERRAL = "INSERT INTO users(chat_id, username, full_name, referral) " \
                            "VALUES ($1, $2, $3, $4) RETURNING id"
    ADD_NEW_USER = "INSERT INTO users(chat_id, username, full_name) VALUES ($1, $2, $3) RETURNING id"
    COUNT_USERS = "SELECT COUNT(*) FROM users"
    GET_ID = "SELECT id FROM users WHERE chat_id = $1"
    CHECK_REFERRALS = "SELECT chat_id FROM users WHERE referral=" \
                      "(SELECT id FROM users WHERE chat_id=$1)"
    CHECK_BALANCE = "SELECT balance FROM users WHERE chat_id = $1"
    ADD_MONEY = "UPDATE users SET balance=balance+$1 WHERE chat_id = $2"

    async def add_new_user(self, referral=None):
        user = types.User.get_current()

        chat_id = user.id
        username = user.username
        full_name = user.full_name
        args = chat_id, username, full_name

        if referral:
            args += (int(referral),)
            command = self.ADD_NEW_USER_REFERRAL
        else:
            command = self.ADD_NEW_USER

        try:
            record_id = await self.pool.fetchval(command, *args)
            return record_id
        except UniqueViolationError:
            pass

    async def count_users(self):
        record: Record = await self.pool.fetchval(self.COUNT_USERS)
        return record

    async def get_id(self):
        command = self.GET_ID
        user_id = types.User.get_current().id
        return await self.pool.fetchval(command, user_id)

    async def check_referrals(self):
        user_id = types.User.get_current().id
        command = self.CHECK_REFERRALS
        rows = await self.pool.fetch(command, user_id)
        return ", ".join([
            f"{num + 1}. " + (await bot.get_chat(user["chat_id"])).get_mention(as_html=True)
            for num, user in enumerate(rows)
        ])

    async def check_balance(self):
        command = self.CHECK_BALANCE
        user_id = types.User.get_current().id
        return await self.pool.fetchval(command, user_id)

    async def add_money(self, money):
        command = self.ADD_MONEY
        user_id = types.User.get_current().id
        return await self.pool.fetchval(command, money, user_id)


db = DBCommands()


@dp.message_handler(commands=["test_start"])
async def register_user(message: types.Message):
    chat_id = message.from_user.id
    referral = message.get_args()
    id = await db.add_new_user(referral=referral)
    count_users = await db.count_users()

    text = ""
    if not id:
        id = await db.get_id()
    else:
        text += "Записал в базу! "

    bot_username = (await bot.me).username
    bot_link = f"https://t.me/{bot_username}?start={id}"
    balance = await db.check_balance()
    text += f"""
в базе {count_users} человек!

реферальная ссылка: {bot_link}
проверить рефералов: /test_ref

баланс: {balance} монет.

добавить монет: /test_add_money
"""

    await bot.send_message(chat_id, text)


@dp.message_handler(commands=["test_ref"])
async def check_referrals(message: types.Message):
    referrals = await db.check_referrals()
    text = f"рефералы:\n{referrals}"

    await message.answer(text)


@dp.message_handler(commands=["test_add_money"])
async def add_money(message: types.Message):
    random_amount = random.randint(1, 100)
    await db.add_money(random_amount)
    balance = await db.check_balance()

    text = f"""
добавлено {random_amount} монет.
баланс: {balance}
    """
    await message.answer(text)

@dp.message_handler(Command("menu"))
async def show_menu(message: Message):
    await message.answer("Перейти в", reply_markup=menu)


@dp.message_handler(Text("Список группы"))
async def show_list(message: Message):
    await message.answer("Список группы", reply_markup=menu)

    handle=open("list.txt","r", encoding='utf-8')
    data=handle.readlines()
    new_data=""
    for i in range(len(data)):
        new_data=new_data+data[i]
    await message.answer(new_data, reply_markup=back)
    handle.close()

@dp.message_handler(Text("Расписание (преп.)"))
async def show_list(message: Message):
    await message.answer("Soon...", reply_markup=back)

@dp.message_handler(Text("Расписание (студ.)"))
async def show_list(message: Message):
    await message.answer("Soon...", reply_markup=back)
    await bot.sendPhoto("studshed.jpg", reply_markup=back)

@dp.message_handler(Text("Контакты (преп.)"))
async def show_list(message: Message):
    await message.answer("Контакты (преп.)", reply_markup=menu)

    handle=open("Contacts.txt","r", encoding='utf-8')
    data=handle.readlines()
    new_data=""
    for i in range(len(data)):
        new_data=new_data+data[i]
    await message.answer(new_data, reply_markup=back)
    handle.close()

@dp.message_handler(Text("Др. инф-ия"))
async def show_list(message: Message):
    await message.answer("Др. инф-ия", reply_markup=menu)

    handle=open("addit.txt","r", encoding='utf-8')
    data=handle.readlines()
    new_data=""
    for i in range(len(data)):
        new_data=new_data+data[i]
    await message.answer(new_data, reply_markup=back)
    handle.close()


#reply_markup=ReplyKeyboardRemove()

@dp.message_handler(Text("Предметы"), state=None)
async def get_food(message: Message):
    await message.answer("Выберите предмет:", reply_markup=subj)

    await Test.Q1.set()


@dp.message_handler(state=Test.Q1)
async def answer_q1(message: Message, state: FSMContext):
    answer = message.text

    try:
        handle = open(f"{answer}.txt", "r", encoding='utf-8')
    except FileNotFoundError:
        await message.answer("Предмет не найден", reply_markup=back)
    else:
        data = handle.readlines()
        new_data = ""
        for i in range(len(data)):
            new_data = new_data + data[i]
        handle.close()
        await message.answer(new_data,parse_mode="HTML", reply_markup=back)
    finally:
        await state.finish()


@dp.message_handler(Text("Куда идти"), state=None)
async def get_food(message: Message):
    await message.answer("Soon...", reply_markup=back)

@dp.message_handler(content_types=ContentType.ANY)
async def unknown_message(message: Message):
    await message.answer("Вводи команду /menu", reply_markup=back)

