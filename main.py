import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from config import BOT_TOKEN
from database import init_db
from handlers import router
from admin import admin_router

async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Asosiy menyuga qaytish va qayta boshlash")
    ]
    await bot.set_my_commands(commands)

async def main():
    # Initialize Database
    init_db()
    
    # Initialize Bot and Dispatcher
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Set bot commands
    await set_commands(bot)
    
    # Include routers
    dp.include_router(admin_router)
    dp.include_router(router)
    
    print("Bot is starting...")
    # Polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Setup logging to console
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
