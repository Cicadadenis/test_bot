from threading import Timer
from threading import *
from aiogram import Dispatcher, executor
from aiogram.dispatcher.filters import ChatTypeFilter
from aiogram.types import (ChatType, ContentTypes, InlineKeyboardButton,
                        InlineKeyboardMarkup, Message)


from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import Bot, types
from aiogram.utils.markdown import hbold, hlink
from aiogram.utils.exceptions import BadRequest
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from rich.logging import RichHandler
import sqlite3
import random
from pathlib import Path
from os.path import exists
import requests, os

import asyncio, time
from aiogram.types import User
import time
from threading import Timer
import asyncio
import sys
import re
from aiogram.types import ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, inline_keyboard
import requests



menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.row("ℹ️ Создать Бота ℹ️", "ℹ️ Мои Боты ℹ️")
class cicada(StatesGroup):
    sms = State()
    boti = State()
    boti2 = State()



token = input("\n     Введи Токен Бота: ")
bot = Bot(token=token, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=['start'], state="*")
async def show_contact(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    name = message.chat.first_name
    await message.answer(f"<b>Привет {name} !</b>", reply_markup=menu)


    
@dp.message_handler(text="ℹ️ Мои Боты ℹ️", state="*")
async def bot_add(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    username = message.chat.username
    bb = 'mur_site_edit_bot'
    boti = get_bots(username)
    if boti == False:
        await message.answer("<b>У Тебя Нет Еще Созданных Ботов</b>")
    else:
        # print(boti)
        # if bb in boti:
        #     print("est")
        # else:
        #     print("net")
        if len(boti) >= 1:
            klava = InlineKeyboardMarkup()
            for x in boti:
                klava.add(InlineKeyboardButton(x, callback_data=x))
            await message.answer('<b>Твои Боты</b>', reply_markup=klava)
            await cicada.boti.set()
        else:
            await message.answer("<b>У Тебя Нет Еще Созданных Ботов</b>")





@dp.message_handler(text="ℹ️ Создать Бота ℹ️", state="*")
async def bot_add(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    username = message.chat.username
    # get_files_user(username)
    await message.answer("<b>Отправь Мне Токен Бота</b>")
    await cicada.sms.set()



def check_db(username):
    databaseFile = ("data.db")
    db = sqlite3.connect(databaseFile, check_same_thread=False)
    cursor = db.cursor()
    try:
        cursor.execute(f"SELECT * FROM {username}")
    except sqlite3.OperationalError:
        cursor.execute(f"CREATE TABLE {username}(username TEXT, id TEXT, token TEXT)")

def get_bots(username):
    db = sqlite3.connect('data.db', check_same_thread=False)
    cursor = db.cursor()
    try:
        cursor.execute(f"SELECT username FROM {username}")
        fileIDs = cursor.fetchall()
        bott = []
        for x in fileIDs:
            bott.append(x[0])
        return bott
    except:
        return False

def get_files_user(name, username):
    db = sqlite3.connect('data.db', check_same_thread=False)
    cursor = db.cursor()
    cursor.execute(f"SELECT username FROM {name}")
    fileIDs = cursor.fetchall()
    bott = []
    for x in fileIDs:
        bott.append(x[0])
    if username in bott:
        return False
    if username not in bott:
        return True


def add_bot(name, username, id_us, tkk):
    db = sqlite3.connect('data.db', check_same_thread=False)
    cursor = db.cursor()
    data = [username, id_us, tkk]
    cursor.execute(f'''INSERT INTO {name}(username, id, token) VALUES(?,?,?)''', data)
    db.commit()

@dp.message_handler(state=cicada.sms)
async def input_text_for_ad(message: types.Message, state: FSMContext):
    name = message.chat.username
    tkk = message.text
    await state.finish()
    
    MethodGetMe = (f'''https://api.telegram.org/bot{tkk}/GetMe''')
    response = requests.post(MethodGetMe)
    tttm = response.json()
    tk = tttm['ok']
    bt = 5739769545
    if tk == True:
        username = (tttm['result']['username'])
        id_us = (tttm['result']['id'])
        print(id_us)
        os.system(f"mkdir {name}")
        with open(f"{name}/{username}.py", "w") as f:
            f.write(f"token = '{tkk}'\n")

        url = "https://raw.githubusercontent.com/Cicadadenis/REFERAL_BOT_TELEGRAM/main/main.py"

        r = requests.get(url)
        ma = r.text
        with open(f"{name}/{username}.py", "a") as h:
            h.write(str(ma))

        check_db(name)
        pro = get_files_user(name, username)
        if pro == True:
            add_bot(name, username, id_us, tkk)
            os.system(f"cd {name} && setsid -f  python3 {username}.py")
            await message.answer(f"<b>Бот @{username} Запущен !</b>\n"
                                 f"<b>Зайди В Него И Введи Команду //admin </b>")
        if pro == False:
            await message.answer("<b>Этот Токен Уже Используеться</b>")
        
        
    else:
        await message.answer(f"<b>Токен Не Валидный !</b>")
def bbboot(name, bo):
    db = sqlite3.connect('data.db', check_same_thread=False)
    cursor = db.cursor()
    cursor.execute(f"SELECT *  FROM {name} ")
    fileIDs = cursor.fetchall()
    for x in fileIDs:
        if bo in x:
            return x[1]
def dead_bot(name, bo):
    db = sqlite3.connect('data.db', check_same_thread=False)
    cursor = db.cursor()
    cursor.execute(f"DELETE FROM {name} WHERE username= '{bo}' ")
    db.commit()

@dp.callback_query_handler(state=cicada.boti2)
async def b2(call: CallbackQuery, state: FSMContext):
    name = call.message.chat.username
    bo = call.data
    username = bo.split(':')[0]
    if bo.split(':')[1] == "stop":
        os.system("ps -x > ps.txt")
        ps = open("ps.txt", "r").readlines()
        for x in ps:
            if username in x:
                dead_bot(name, username)
                xx = x.split()
                dead = int(xx[0])
                os.system(f"kill {dead}")
                await call.message.answer("<b>Бот Успешно Остановлен</b>")
    if bo.split(':')[1] == "reset":
        os.system("ps -x > ps.txt")
        ps = open("ps.txt", "r").readlines()
        for x in ps:
            if username in x:
                xx = x.split()
                dead = int(xx[0])
                os.system(f"kill {dead}")
                os.system(f"cd {name} && setsid -w  python3 {username}.py")
                await call.message.answer("<b>Бот Успешно Перезапущен</b>")

@dp.callback_query_handler(state=cicada.boti)
async def ref(call: CallbackQuery, state: FSMContext):
    name = call.message.chat.username
    bo = call.data
    await state.finish()
    kla = InlineKeyboardMarkup()
    kla.add(
        InlineKeyboardButton("Остановить", callback_data=f"{bo}:stop"),
        InlineKeyboardButton("Перезагрузить", callback_data=f"{bo}:reset")
    )
    

    await call.message.answer(f"<b>Управление Ботом @{bo}</b>", reply_markup=kla)
    await cicada.boti2.set()

if __name__ == '__main__':
    os.system("clear")
    print("\n\n\n\n             Бот Запущен !!!!")
    executor.start_polling(dp, skip_updates=True)
