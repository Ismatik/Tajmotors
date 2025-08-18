import asyncio
import pandas as pd
from Registration_functions import functions
from contextlib import asynccontextmanager
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError,TelegramBadRequest
from aiogram.methods import SendPhoto
from config_reader import EXCEL_FILE, config

bot = Bot(token=config.bot_token.get_secret_value())


#Lifespan manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manages the start and end of FastAPI application"""

    print("API Server started work")
    
    yield # API Runs here
    
    print("API server is shutting down, closing the bot session...")
    
    await bot.session.close()

#API Setup
app = FastAPI(lifespan=lifespan)

# --- Pydantic Model for Request Body ---
# This ensures the incoming request has the correct data format.
class BroadcastMessage(BaseModel):
    message: str

    
@app.post("/broadcast")
async def send_broadcast(bc_message: BroadcastMessage):
    
    try:
        bc_message = bc_message.__str__().split("=")[-1].replace("'" , "")
        # pic = pic.__str__().split("=")
        df = pd.read_excel(EXCEL_FILE)
        user_ids = df['User_ID'].tolist()
        asyncio.create_task(broadcast_loop(user_ids , bc_message))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read user database:{e}")

    if not user_ids:
        return {"status":"warning" , 
                "message":f"Broadcast started to {len(user_ids)}"}
    
async def broadcast_loop(user_ids: list, message: str):
    """The actual loop to send messages to avoid blocking the API response.

    Args:
        user_ids (list): list of users to send message
        message (str): what message to send
    """
    successful_sends = 0
    failed_sends = 0
    for user in user_ids:
        try:
            await bot.send_message(chat_id=user ,
                                   text=message)
            
            successful_sends += 1
            await bot(SendPhoto(chat_id=user,photo="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRZZPJ_PB7TTJq68vx0M4j-9Q2CtFiIwxp02w&s"))
        except (TelegramForbiddenError, TelegramBadRequest):
            failed_sends +=1 
        await asyncio.sleep(0.1)
        
    print(f"Broadcast task finished. Successful: {successful_sends}, Failed: {failed_sends}")
    
    #uvicorn broadcast_api:app --reload   -> to run your server and ping with postman