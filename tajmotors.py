# =================================================================================
# 1. IMPORTS
# =================================================================================
import asyncio
import logging
import re


from aiogram import Bot, Dispatcher

from config_reader import config

#File containing function to register
from Registration_functions import functions

#Routers import
from handlers.service import router as service_router
from handlers.registration import router as registration_router
from handlers.testdrive import router as testdrive_router

# =================================================================================
# 21. CONFIGURATION AND INITIALIZATION
# =================================================================================

logging.basicConfig(level=logging.INFO)
    
# Initialize bot, dispatcher
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()


# =================================================================================
# MAIN EXECUTION BLOCK
# =================================================================================

async def main():
    dp.include_router(service_router)
    dp.include_router(registration_router)
    dp.include_router(testdrive_router)
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    asyncio.run(main())
        
