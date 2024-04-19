import datetime
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types.input_file import FSInputFile
from aiogram.types import KeyboardButton, CallbackQuery
from aiogram import F
from scripts import univer
global course
import json

logging.basicConfig(level=logging.INFO)
bot = Bot(token="5911348337:AAHd13DDH51IEDLChbi6GcgnByx0ZTORCxQ")
dp = Dispatcher()
course = ''
log = ''
passw = ''

def kb_menu():
    buttons = [
        [KeyboardButton(text='Расписание', callback_data= "scheduler")], 
        [KeyboardButton(text='Выбор курса', callback_data= "course")]
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard

def kb_course():
    buttons = [
        [types.KeyboardButton(text="1 курс")],
        [types.KeyboardButton(text="2 курс")],
        [types.KeyboardButton(text="3 курс")],
        [types.KeyboardButton(text="4 курс")]
    ]

    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard

@dp.message(Command("start"))
async def cmd_start(message: types.Message):

    await bot.send_photo(chat_id=message.chat.id, photo=FSInputFile('photos/logo.png', 'rb'))
    await message.answer("<b>Привет!🎉</b> Добро пожаловать в бота по упрощению учебной жизни в Финансовом Университете при Правительстве РФ КФ\n\n"
                        "Здесь ты можешь посмотреть свое расписание нажатием кнопки <i><b>Расписание</b></i>, выбрать свой курс кнопкой <i><b>Выбор курса</b></i>.\n\n"
                        "На данном этапе это не итоговая версия, некоторые функции будут дополняться, следите за обновлениями 🚀", reply_markup= kb_menu(), parse_mode='HTML')

@dp.message(F.text == 'Выбор курса')
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

@dp.message(F.text == 'Расписание')
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

@dp.message(F.text == 'Авторизация')
async def kn(message):
    await bot.send_message(message.chat.id, f'Введите логин и пароль! \n Образец: \n Логин:пароль')

@dp.message(F.text.lower()[3:6] == 'dot' )
async def logpass(message):
    logpassw = message.text.split(':')
    with open('logpass_data.txt', 'a') as file:
        file.write(f'{message.chat.id}/{logpassw}\n')
    await bot.send_message(message.chat.id, 'Отлично! Я записал ✅', reply_markup= kb_menu())

@dp.message(F.text == 'Зачетная книжка')
async def grades(message:types.Message):
    global log, passw
    with open('logpass_data.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if str(message.chat.id) in line:
                l1, l2 = line.strip().split('/')
                print(l2[1:-1])
                log, passw = l2.split(', ')
                log = log[2:-1]
                passw = passw[1:-2]
                print(log, passw)
                break
    if log != '' and passw != '':
        response = univer(course, log, passw).parsing()
        log = ''
        passw = ''
        await message.answer(response, reply_markup= kb_menu())
    else:
        await message.answer('Для начала авторизуйтесь!')

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())