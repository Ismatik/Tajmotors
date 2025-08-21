from aiogram.types import Message
from aiogram import Router, F
from Registration_functions.functions import return_sh,fetch_language
from aiogram.enums import ParseMode

router = Router()

@router.message(F.text.startswith("⚙️"))
async def tdh(message: Message):
    user_info = return_sh(message.chat.id)
    
    reply = {"EN" : "Your service history requests:\n",
             "RU" : "Ваши запросы по истории обслуживания:\n",
             "TJ" : "Дархостҳои таърихи хидматрасонии шумо:\n"}
    
    lang = fetch_language(message.chat.id)
    content = reply[lang] + '<b>'
    for i in user_info:
        content += f"{i[5]} {i[6]} {i[8]} {i[4]} {i[3]}\n"
    content += "</b>"
    await message.answer(
        text= content,
        parse_mode=ParseMode.HTML
    )
    