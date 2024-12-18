import asyncio
from aiogram import Bot, Dispatcher

from app.handlers import router
from app.database.models import async_main

async def main():
    await async_main()
    bot_token = Bot(token='7363260726:AAF0jMgIaY3axkBqZXT1-JOT6RYaDyboeZg')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot_token)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
      
