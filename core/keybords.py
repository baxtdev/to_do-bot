from aiogram.types import InlineKeyboardButton, \
    InlineKeyboardMarkup, KeyboardButton,\
    ReplyKeyboardMarkup, ReplyKeyboardRemove


menu = [
    [InlineKeyboardButton(text="📝 Добавит Задачу", callback_data="add_task"),InlineKeyboardButton(text="📝 Мои Задачи", callback_data="my_task"),]
]

menu_task = [
    [InlineKeyboardButton(text="📝 Изменить Задачу", callback_data="edit_task"),InlineKeyboardButton(text="📝 Удалить Задачу", callback_data="del_task"),]
]


def create_task_menu(task_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Изменить Задачу", callback_data=f"edit_task:{task_id}"),
        InlineKeyboardButton(text="📝 Удалить Задачу", callback_data=f"del_task:{task_id}")]
    ])

menu = InlineKeyboardMarkup(inline_keyboard=menu)
menu_task = InlineKeyboardMarkup(inline_keyboard=menu_task)

exit_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="◀️ Выйти в меню")]], resize_keyboard=True)

iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню", callback_data="menu")]])
