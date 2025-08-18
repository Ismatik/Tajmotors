# =================================================================================
# 1. IMPORTS
# =================================================================================
import asyncio
import logging
import sys
import os

from aiogram import Bot, Dispatcher

from config_reader import config
from config_reader import USER_ACTIVITY_LOG_FILE

#File containing function to register
from Registration_functions import functions

#Routers import
from handlers.service import router as service_router
from handlers.registration import router as registration_router
from handlers.testdrive import router as testdrive_router
from handlers.edit_profile import router as editprofile_router

# =================================================================================
# 21. CONFIGURATION AND INITIALIZATION
# =================================================================================


# Initialize bot, dispatcher
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()


# =================================================================================
# MAIN EXECUTION BLOCK
# =================================================================================

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        handlers={
            logging.FileHandler(USER_ACTIVITY_LOG_FILE , mode = "a"),
            logging.StreamHandler()
        }
    )
    dp.include_router(service_router)
    dp.include_router(registration_router)
    dp.include_router(testdrive_router)
    dp.include_router(editprofile_router)
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO , stream=sys.stdout)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt , SystemExit):
        logging.info("Bot was stopped.")
