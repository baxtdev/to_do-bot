from datetime import date
from aiogram import F, Router, types,html
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import logging
from typing import Any, Dict
from pydantic import ValidationError
from aiogram_calendar import SimpleCalendar,SimpleCalendarCallback


from core.models import TaskModel
from core import keybords as kb
from core import texts as text
from core import utils
from core.states import TaskStates
from core.db import create_task,get_tasks,delete_task


router = Router()

@router.message(Command("start"))
async def start_handler(msg: Message):   
    await msg.answer(f"Привет! {msg.from_user.username} я бот задачик могу сохранить твои задачи и напоминать тебе об этом",reply_markup=kb.menu,)



@router.callback_query(F.data=="my_task")
async def my_task_handler(clbck: types.CallbackQuery):
    data = await get_tasks(clbck.from_user.id)
    for data in data:
        text = f"""Название Задачи:{html.quote(data['waiting_for_task_name'])},
        Дата началы {html.quote(data['waiting_for_start_date'])},
        Дата окончание {html.quote(data['waiting_for_end_date'])}
        """
        await clbck.message.answer(text=text,reply_markup=kb.create_task_menu(data['id']))
    
    await clbck.answer("Это все")

@router.callback_query(F.data.startswith("del_task:"))
async def delete_task_handler(clbck: types.CallbackQuery):
    task_id = (clbck.data.split(":")[1])
    await delete_task(task_id)
    await clbck.answer("Задача удалена")
    await clbck.message.delete()

@router.callback_query(F.data=="add_task")
async def add_task_handler(clbck: types.CallbackQuery, state: FSMContext):
        await state.set_state(TaskStates.waiting_for_task_name)
        await clbck.answer(
            "Введите название Задачи",
        )
        await clbck.message.answer(
            "Введите название Задачи",
            reply_markup=kb.ReplyKeyboardMarkup(
            keyboard=[
                [
                    kb.KeyboardButton(text="cancel"),
                ]
            ],
            resize_keyboard=True,
        ),
        )



@router.message(Command("cancel"))
@router.message(F.text.casefold() == "cancel")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Cancelled.",
        reply_markup=kb.ReplyKeyboardRemove()
    )



@router.message(TaskStates.waiting_for_task_name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(waiting_for_task_name=message.text)
    await state.set_state(TaskStates.waiting_for_start_date)
    data = await state.get_data()
    await message.reply(
        f"Имя Задачи сохранено {html.quote(data['waiting_for_task_name'])}\nВведите Дата началы",
        reply_markup= await SimpleCalendar().start_calendar()
    )



@router.callback_query(SimpleCalendarCallback.filter())
async def process_calendar(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    selected, selected_date = await SimpleCalendar().process_selection(callback_query, callback_data)
    if selected:
        if await state.get_state() == TaskStates.waiting_for_start_date.state:
            await state.update_data(waiting_for_start_date=selected_date.isoformat())
            await callback_query.message.answer("Выберите дату окончания задачи:", reply_markup=await SimpleCalendar().start_calendar())
            await state.set_state(TaskStates.waiting_for_end_date)
        
        elif await state.get_state() == TaskStates.waiting_for_end_date:
            await state.update_data(waiting_for_end_date=selected_date.isoformat())
            user_data = await state.get_data()
            task_name = user_data.get("waiting_for_task_name")
            start_date = user_data.get("waiting_for_start_date")
            end_date = user_data.get("waiting_for_end_date")
            task_name = user_data.get("waiting_for_task_name")

        try:
            task = TaskModel(task_name=task_name, start_date=start_date, end_date=end_date)
        except ValidationError as e:
            await callback_query.message.answer(f"Ошибка валидации:Дата окончание должен быть позже даты начала ")
            return

        await callback_query.message.answer(
            f"Задача '{task_name}' добавлена. Дата начала: {start_date}, дата окончания: {end_date}")

        user_data["user_id"]=callback_query.from_user.id
        print(user_data)
        await create_task(user_data) 
        await state.clear()
        await show_summary(message=callback_query.message, data=user_data)


   
async def show_summary(message: Message, data: Dict[str, Any], positive: bool = True) -> None:
    name = data["waiting_for_task_name"]
    start_date = data.get("waiting_for_start_date", None)
    end_date = data.get("waiting_for_end_date", None)
    text = f"Назвние Задачи {html.quote(name)},\nДата начало {html.quote(start_date)}\nДата окончание {html.quote(end_date)}"

    await message.answer(text=text,reply_markup=kb.menu)

