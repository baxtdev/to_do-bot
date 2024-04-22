from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.types import Message


from core import keybords as kb
from core import texts as text
from core import utils

from . import keybords

router = Router()

@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer("Привет! Я помогу тебе узнать твой ID, просто отправь мне любое сообщение")


@router.message()
async def message_handler(msg: Message):
    await msg.answer(f"Твой ID: {msg.from_user.id}",reply_markup=keybords.menu)