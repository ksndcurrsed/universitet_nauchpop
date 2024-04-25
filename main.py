import datetime
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types.input_file import FSInputFile
from aiogram.types import KeyboardButton
from aiogram import F
from scripts import univer
global course
import json
import secrets

logging.basicConfig(level=logging.INFO)
bot = Bot(token="5927699959:AAHAltTvMZRd1pRfAULj6L6J8YQP4ch96lk")
dp = Dispatcher()
course = ''
chat_id = ''

def kb_menu():
    buttons = [
        [KeyboardButton(text='Расписание📅'), 
        KeyboardButton(text='Выбор курса📎'),
        KeyboardButton(text='Зачетная книжка📂')],
        [KeyboardButton(text='Авторизация👤')]
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard

def kb_course():
    buttons = [
        [types.KeyboardButton(text="1 курс"),
        types.KeyboardButton(text="2 курс")],
        [types.KeyboardButton(text="3 курс"),
        types.KeyboardButton(text="4 курс")]
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    global chat_id
    chat_id = message.chat.id
    await bot.send_photo(chat_id=message.chat.id, photo=FSInputFile('photos/logo.png', 'rb'))
    await message.answer("<b>Привет!🎉</b> Добро пожаловать в бота по упрощению учебной жизни в Финансовом Университете при Правительстве РФ КФ\n\n"
                        "Здесь ты можешь посмотреть свое расписание нажатием кнопки <i><b>Расписание</b></i>, выбрать свой курс кнопкой <i><b>Выбор курса</b></i>.\n\n"
                        "На данном этапе это не итоговая версия, некоторые функции будут дополняться, следите за обновлениями 🚀", reply_markup= kb_menu(), parse_mode='HTML')

@dp.message(F.text == 'Выбор курса📎')
async def cmd_course(message: types.Message):
    await message.answer("Выбери свой курс", reply_markup=kb_course())

@dp.message(F.text.lower() == "1 курс")
async def course1(message: types.Message):
    global course 
    course = '1'
    await message.answer('Отлично, я записал!', reply_markup= kb_menu())

@dp.message(F.text.lower() == "2 курс")
async def course2(message: types.Message):
    global course 
    course = '2'
    await message.answer('Отлично, я записал!', reply_markup= kb_menu())

@dp.message(F.text.lower() == "3 курс")
async def course3(message: types.Message):
    global course 
    course = '3'
    await message.answer('Отлично, я записал!', reply_markup= kb_menu())

@dp.message(F.text.lower() == "4 курс")
async def course4(message: types.Message):
    global course 
    course = '4'
    await message.answer('Отлично, я записал!', reply_markup= kb_menu())

@dp.message(F.text == 'Расписание📅')
async def cmd_sheduler(message: types.Message):
    global course
    if course != '':
        response = univer(course).schedule(course)
        print(response)
        document = FSInputFile('расписание.pdf')
        await bot.send_document(message.chat.id, document, reply_markup= kb_menu())
    else:
        await message.answer('Ошибка! Для начала укажите свой курс!', reply_markup= kb_menu())

@dp.message(Command("whatcourse"))
async def start(message: types.Message):
    await message.answer("Ты учишься на: " + course)

@dp.message(F.text == 'Авторизация👤')
async def kn(message):
    await bot.send_message(message.chat.id, f'Введите логин и пароль! \n\nОбразец: \nЛогин:пароль')

@dp.message(F.text.lower()[3:6] == 'dot' )
async def logpass(message):
    logpassw = message.text.split(':')
    chat_id = message.chat.id
    await bot.send_message(chat_id=chat_id, text=univer(course).database_auth(logpassw, chat_id), reply_markup= kb_menu())

@dp.message(F.text == 'Зачетная книжка📂')
async def grades(message:types.Message):
    chat_id = message.chat.id
    if univer(course).check_user_id_to_parsing(chat_id) is False:
        await message.answer('Для начала авторизуйтесь!')
    else:
        try:
            response = univer(course).parsing(univer(course).check_user_id_to_parsing(chat_id))
            await message.answer(response, reply_markup= kb_menu())
        except Exception as e:
            await message.answer(f'Произошла ошибка: {e}', reply_markup= kb_menu())


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())