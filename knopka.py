from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btnNach = KeyboardButton('Начнем')
faq = KeyboardButton('Правила')
mainMenu = ReplyKeyboardMarkup(resize_keyboard= True).add(btnNach, faq)