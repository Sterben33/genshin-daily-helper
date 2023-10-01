# import genshin
import genshin
from aiogram import Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.utils.markdown import hbold
import sqlite3
import menu

connection = sqlite3.connect('db/sqlite.db')
cursor = connection.cursor()
# ltoken = "TLp1IgNFX705TN6YtUvV9UQ1dgwNBOxiOq91008R"
# ltuid = 305779919
# client = genshin.Client({"ltuid": ltuid, "ltoken": ltoken}, game=genshin.Game.GENSHIN)
# notes = await client.get_notes()
# reward = await client.claim_daily_reward()
# realm_coins = notes.current_realm_currency
# realm_recover_time = notes.remaining_realm_currency_recovery_time
# claimed_commission_reward = notes.claimed_commission_reward
# resin = notes.current_resin
# resin_recovery_time = notes.remaining_resin_recovery_time
#
# await message.answer(f"Hello,  {hbold(message.chat.id)}!")
# await message.answer(f"Hello,  {hbold(message.from_user.id)}!")
# await message.answer(f"Hello,  {hbold(reward)}!")

dp = Dispatcher(storage=MemoryStorage())


class Auth(StatesGroup):
    entering_ltuid = State()
    entering_itoken = State()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    auth_data = cursor.execute(f"SELECT ltuid, itoken FROM users WHERE tg_id={message.from_user.id}").fetchone()
    if not auth_data:
        auth_data = cursor.execute(f"INSERT INTO users (tg_id, name, ltuid, itoken) VALUES ({message.from_user.id}, '{message.from_user.full_name}', NULL, NULL) RETURNING ltuid, itoken").fetchone()
        connection.commit()
    print(auth_data)
    if not auth_data[0] or not auth_data[1]:
        await message.answer(f"Hello,  {hbold(message.from_user.full_name)}!\n\
Your have not provided auth data or its expired, set ltuid and itoken", reply_markup=menu.unauth_menu)
    else:
        await message.answer(f"Hello,  {hbold(message.from_user.full_name)}!", reply_markup=menu.menu)


@dp.message(F.text.lower() == "authorize")
async def echo_handler(message: types.Message, state: FSMContext) -> None:
    await message.answer(f"Go to hoyolab.com.\n\
Login to your account.\n\
Press F12 to open Inspect Mode (ie. Developer Tools).\n\
Go to Application, Cookies, https://www.hoyolab.com.\n\
Copy ltuid and ltoken.", reply_markup=types.ReplyKeyboardRemove())
    await message.answer(f"Enter ltuid:")
    await state.set_state(Auth.entering_ltuid)


@dp.message(Auth.entering_ltuid)
async def echo_handler(message: types.Message, state: FSMContext) -> None:
    msg = message.text
    try:
        msg = int(msg)
    except ValueError:
        await message.answer("Value is not a number! Try again.", reply_markup=types.ReplyKeyboardRemove())
        return
    cursor.execute(f"UPDATE users SET ltuid={int(msg)} WHERE tg_id={message.from_user.id}")
    connection.commit()
    await message.answer(f"Enter itoken:", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(Auth.entering_itoken)


@dp.message(Auth.entering_itoken)
async def echo_handler(message: types.Message, state: FSMContext) -> None:
    msg = message.text
    cursor.execute(f"UPDATE users SET itoken='{msg}' WHERE tg_id={message.from_user.id}")
    connection.commit()
    await message.answer(f"Authorized!", reply_markup=menu.menu)
    await state.set_state(None)


@dp.message(F.text.lower() == "resin")
async def echo_handler(message: types.Message) -> None:
    user = cursor.execute(f"SELECT ltuid, itoken FROM users WHERE tg_id={message.from_user.id}").fetchone()
    if not user:
        await message.answer(f"Hello,  {hbold(message.from_user.full_name)}!\n\
    Your have not provided auth data or its expired, set ltuid and ltoken", reply_markup=menu.unauth_menu)
        return
    client = genshin.Client({"ltuid": user[0], "ltoken": user[1]}, game=genshin.Game.GENSHIN)
    notes = await client.get_notes()
    resin = notes.current_resin
    await message.answer(f"resin = {resin}", reply_markup=menu.menu)


@dp.message(F.text.lower() == "daily")
async def echo_handler(message: types.Message) -> None:
    user = cursor.execute(f"SELECT ltuid, itoken FROM users WHERE tg_id={message.from_user.id}").fetchone()
    if not user:
        await message.answer(f"Hello,  {hbold(message.from_user.full_name)}!\n\
Your have not provided auth data or its expired, set ltuid and ltoken", reply_markup=menu.unauth_menu)
        return
    client = genshin.Client({"ltuid": user[0], "ltoken": user[1]}, game=genshin.Game.GENSHIN)
    try:
        a = await client.claim_daily_reward()
        await message.answer(f"check your ingame mail for {a.name} x{a.amount}!", reply_markup=menu.menu)
    except genshin.errors.AlreadyClaimed:
        await message.answer(f"daily reward already collected", reply_markup=menu.menu)



@dp.message(Command(commands=["menu"]))
async def echo_handler(message: types.Message) -> None:
    user = cursor.execute(f"SELECT ltuid, itoken FROM users WHERE tg_id={message.from_user.id}").fetchone()
    if not user or not user[0] or not user[1]:
        await message.answer(f"Hello,  {hbold(message.from_user.full_name)}!\n\
Your have not provided auth data or its expired, set ltuid and itoken", reply_markup=menu.unauth_menu)
        return

    await message.answer(f"Menu", reply_markup=menu.menu)