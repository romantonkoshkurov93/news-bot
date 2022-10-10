from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


btnMain = KeyboardButton('⬅ Главное меню')
btnHabrNews = KeyboardButton('Habr')

# --- Main menu ---
btnIrkRuNews = KeyboardButton('Новости Иркутска')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnIrkRuNews, btnHabrNews)

# --- irk.ru menu ---
btnIrkNews = KeyboardButton('Последние новости Иркутска')
btnIrkFreshNews = KeyboardButton('Свежие новости Иркутска')
irkMenu = ReplyKeyboardMarkup(resize_keyboard=True) \
    .add(btnIrkNews, btnIrkFreshNews) \
    .row(btnMain)

# --- Habr menu ---
btnHabrNews = KeyboardButton('Последние новости Habr')
btnHabrFreshNews = KeyboardButton('Свежие новости Habr')
btnHabrArticles = KeyboardButton('Последние статьи Habr')
btnHabrFreshArticles = KeyboardButton('Свежие статьи Habr')
habrMenu = ReplyKeyboardMarkup(resize_keyboard=True) \
    .add(btnHabrNews, btnHabrFreshNews) \
    .add(btnHabrArticles, btnHabrFreshArticles) \
    .row(btnMain)
