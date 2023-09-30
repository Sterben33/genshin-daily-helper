from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

menu = [
    [KeyboardButton(text="resin"), KeyboardButton(text="daily"), ]
]
unauth_menu = [
    [KeyboardButton(text="Authorize"), ]
]
menu = ReplyKeyboardMarkup(keyboard=menu, resize_keyboard=True)
unauth_menu = ReplyKeyboardMarkup(keyboard=unauth_menu, resize_keyboard=True)
