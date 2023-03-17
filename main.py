import asyncio
import time
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from State import StateGroupExample
from PIL import Image
import knopka as nav

def start():
    empty = Image.open("photo/empty.png")
    temp = empty.copy()
    temp.save('photo/temp.png')

def paste(lx, ly, orientation, length):
    if orientation == "v":
        ry = ly + length
        rx = lx + 1
    else:
        rx = lx + length
        ry = ly + 1
    full = Image.open("photo/full.png")
    temp = Image.open("photo/temp.png")
    x, y = full.size
    x, y = x // 10, y // 12
    temp.paste(full.crop((x * lx, y * ly, x * rx, y * ry)), (x * lx, y * ly))
    temp.save('photo/temp.png')
    full.close()
    temp.close()
t = [(1, 0, "v", 6), (3, 0, "v", 5), (7, 0, "v", 7), (5, 2, "v", 10), (0, 4, "g", 10), (2, 6, "g", 6), (2, 8, "g", 7)]
loop = asyncio.get_event_loop()
TOKEN = "6167204611:AAFxhQCrrUVZFC4GDbOSRv_8sw_lrcksdhQ"
CHANNEL_ID = 1

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, loop=loop, storage=MemoryStorage())

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    logging.info(f'{user_id} {user_full_name} {time.asctime()}')
    await message.reply(f"Привет, сейчас я выдам тебе кроссворд, попробуй решить", reply_markup=nav.mainMenu)
    start()
    await bot.send_photo(user_id,open('photo\\temp.png', 'rb'))
    await message.answer(f"По горизонтали \n5.В религиозно-философском смысле: присутствие божественного в человеке, "
                         f"свойство души человека быть образом божественного Духа.\n "
                         f"6. Нравственность, один из способов нормативной регуляции поведения людей в обществе.\n "
                         f"7.Одна из форм общественного сознания — совокупность представлений, основанных на вере в "
                         f"существование высших сил и существ (Бога и богов), которые являются предметом поклонения "
                         f"\n По вертикали \n 1. Множество людей, характеризующийся общностью социальной, "
                         f"экономической и культурной жизни \n "
                         f"2. Регулятор общественных отношений, совокупность законодательных норм, юридическая "
                         f"составляющая жизни общества \n "
                         f"3.Чувство и сознание моральной ответственности за своё поведение и моральности своих "
                         f"поступков перед самим собой и перед другими \n "
                         f"4.Образ мышления, мировосприятия, присущие индивиду или группе ")

number_of_answer = 0
answers = ['1. Социум', '2. Право', '3. Совесть', '4. Менталитет', '5. Духовность', '6. Мораль', '7. Религия']

@dp.message_handler()
async def help(message: types.Message, state: FSMContext):
    if message.text == 'Правила':
        await bot.send_message(message.from_user.id, '1. Чтобы начать решать кроссворд, напишите слово "Начнем"\n'
                                                     '2. Пишите слова с большой буквы и указывайте номер слова, например: "1. Философия"\n'
                                                     '3. Наслаждайтесь')
    if message.text == 'Начнем':
        await message.answer(text='Начнем')
        await StateGroupExample.wait_for_answer.set()

@dp.message_handler(state=StateGroupExample.wait_for_answer, text=answers)
async def help(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    for i in answers:
        if message.text == i:
            await message.answer(text='Верно')
            f = int(message.text.split()[0][:-1]) - 1
            paste(t[f][0], t[f][1], t[f][2], t[f][3])
            await bot.send_photo(user_id, open('photo\\temp.png', 'rb'))
    #await state.finish()
if __name__ == '__main__':
    executor.start_polling(dp)
