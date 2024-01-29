from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, BotCommand

# Кнопки
show_current_jobs = KeyboardButton(text="Show Current")
start_btn = KeyboardButton(text="Start Parsing")
stop_btn = KeyboardButton(text="Stop Parsing")

# Инициализация клавиатуры
kb = [[start_btn, stop_btn], [show_current_jobs]]
kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

# Команды
