import datetime
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types.input_file import FSInputFile
from aiogram.types import InputFile
from aiogram import F
from scripts import parse
global course

logging.basicConfig(level=logging.INFO)
bot = Bot(token="5927699959:AAHAltTvMZRd1pRfAULj6L6J8YQP4ch96lk")
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await bot.send_photo(chat_id=message.chat.id, photo=FSInputFile('photos/logo.png', 'rb'))
    await message.answer("Привет! Добро пожаловать в бота по упрощению учебной жизни в Финансовом Университете при Правительстве РФ КФ\nЗдесь ты можешь посмотреть свое расписание командой /scheduler," 
                         "выбрать свой курс командой /course. \nНа данном этапе это не итоговая версия, некоторые функции будут дополняться, следите за обновлениями")
course = ''


@dp.message(Command("course"))
async def cmd_course(message: types.Message):
    kb = [
        [types.KeyboardButton(text="1 курс")],
        [types.KeyboardButton(text="2 курс")],
        [types.KeyboardButton(text="3 курс")],
        [types.KeyboardButton(text="4 курс")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer("Выбери свой курс", reply_markup=keyboard)

@dp.message(F.text.lower() == "1 курс")
async def course1(message: types.Message):
    global course 
    course = '1'
    await message.answer('Отлично, я записал!')
@dp.message(F.text.lower() == "2 курс")
async def course2(message: types.Message):
    global course 
    course = '2'
    await message.answer('Отлично, я записал!')
@dp.message(F.text.lower() == "3 курс")
async def course3(message: types.Message):
    global course 
    course = '3'
    await message.answer('Отлично, я записал!')
@dp.message(F.text.lower() == "4 курс")
async def course4(message: types.Message):
    global course 
    course = '4'
    await message.answer('Отлично, я записал!')

@dp.message(Command("scheduler"))
async def cmd_sheduler(message: types.Message):
    now = datetime.datetime.now()
    global course
    response = parse(course).schedule(course)
    print(response)


    document = FSInputFile('расписание.pdf')
    await bot.send_document(message.chat.id, document)
@dp.message(Command("whatcourse"))
async def start(message: types.Message):
    await message.answer("Ты учишься на: " + course)
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())