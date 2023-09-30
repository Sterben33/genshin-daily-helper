import asyncio
import logging
import sqlite3
import sys

import genshin
from aiogram import Bot
from aiogram.enums.parse_mode import ParseMode
from roter import dp

TOKEN = "6623864316:AAE7W45MGBnNYaI99TNhCL9pLOszHQ-7Hh8"


async def scheduled(wait_for, bot: Bot):
  while True:
    await asyncio.sleep(wait_for)
    connection = sqlite3.connect('db/sqlite.db')
    cursor = connection.cursor()
    users = cursor.execute("SELECT ltuid, itoken, tg_id FROM users").fetchall()
    for user in users:
        ltuid, ltoken, tg_id = user[0], user[1], user[2]
        client = genshin.Client({"ltuid": user[0], "ltoken": user[1]}, game=genshin.Game.GENSHIN)
        notes = await client.get_notes()
        remaining_resin_recovery_time = notes.remaining_resin_recovery_time
        resin = notes.current_resin
        if resin == 160:
            await bot.send_message(tg_id, f"ALARM! RESIN IS FULL!")
        elif resin > 0:
            await bot.send_message(tg_id, f"Your resin = {resin} and will recover after {remaining_resin_recovery_time}, go to work nigga!")
    connection.close()

async def main():
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(60*60, bot))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
