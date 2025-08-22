from aiogram.types import Message
from aiogram import Router, F
from Registration_functions.functions import return_tdh,fetch_language
from aiogram.enums import ParseMode

router = Router()

@router.message(F.text.startswith("🚗"))
async def tdh(message: Message):
    user_info = return_tdh(message.chat.id)
    
    reply = {"EN" : "Your test drive history requests:\n",
             "RU" : "Ваши запросы по истории тест-драйвов:\n",
             "TJ" : "Дархостҳои таърихи драйви санҷишии шумо:\n"}
    
    lang = fetch_language(message.chat.id)
    content = reply[lang] + '<b>'
    for i in user_info:
        content += f"{i[4]} {i[6]} (VIN - {i[3]})\n"
    content += "</b>"
    await message.answer(
        text= content,
        parse_mode=ParseMode.HTML
    )
    