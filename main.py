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

logging.basicConfig(level=logging.INFO)
bot = Bot(token="5927699959:AAHAltTvMZRd1pRfAULj6L6J8YQP4ch96lk")
dp = Dispatcher()
course = ''

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
                        "Здесь ты можешь посмотреть свое расписание командой <code>/scheduler</code>, выбрать свой курс командой <code>/course</code>.\n\n"
                        "На данном этапе это не итоговая версия, некоторые функции будут дополняться, следите за обновлениями 🚀", reply_markup= kb_menu())

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

@dp.message(Command('rofls'))
async def start(message:types.Message):
    response = univer(course).parsing()
    await message.answer(response, reply_markup= kb_menu())

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())