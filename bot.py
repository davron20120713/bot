from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

import logic  
import os
from config import TOKEN
from states import ProjectStates

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Клавиатура
menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Обо мне")],
        [KeyboardButton(text="Проекты")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer(
        f"👋 Привет, {message.from_user.first_name}!\n\n"
    "Я — твой персональный бот-портфолио. Вот что я умею:\n\n"
    "📁 /projects — Показать список проектов\n"
    "➕ /add_project — Добавить новый проект\n"
    "📸 /add_photo — Добавить фото к проекту\n"
    "ℹ️ /info — Подробности обо мне 😊",
    reply_markup=menu_keyboard
    parse_mode="HTML"
)


    await message.answer(text, parse_mode="HTML")

@dp.message_handler(commands=["add_photo"])
async def cmd_add_photo(message: types.Message):
    await message.answer("📸 Пришлите фото проекта:")
    await ProjectStates.waiting_for_photo.set()

@dp.message_handler(content_types=types.ContentType.PHOTO, state=ProjectStates.waiting_for_photo)
async def handle_project_photo(message: types.Message, state: FSMContext):
    photo = message.photo[-1]
    file_id = photo.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    file_name = f"{file_id}.jpg"
    await photo.download(destination_file=f"photos/{file_name}")
    await message.answer("✅ Фото добавлено!")
    await state.finish()

@dp.message_handler(commands=["update_status"])
async def update_status_handler(message: types.Message):
    await message.answer("Введите ID проекта и новый статус (через запятую):")
    await ProjectStates.waiting_for_status.set()

@dp.message_handler(state=ProjectStates.waiting_for_status)
async def receive_status_update(message: types.Message, state: FSMContext):
    try:
        project_id, status = message.text.split(",")
        logic.update_project_status(int(project_id.strip()), status.strip())
        await message.answer("✅ Статус проекта обновлён.")
    except:
        await message.answer("⚠️ Ошибка. Попробуйте снова.")
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
