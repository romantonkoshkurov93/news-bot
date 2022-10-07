from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


btnMain = KeyboardButton('⬅ Главное меню')

# --- Main menu ---
btnIrkRuNews = KeyboardButton('Новости Иркутска')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnIrkRuNews)

# --- irk.ru menu ---
btnIrkNews = KeyboardButton('Последние новости Иркутска')
btnIrkFreshNews = KeyboardButton('Свежие новости Иркутска')
irkMenu = ReplyKeyboardMarkup(resize_keyboard=True) \
    .add(btnIrkNews, btnIrkFreshNews) \
    .row(btnMain)