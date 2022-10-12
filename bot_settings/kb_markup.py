from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btnMain = KeyboardButton('⬅ Главное меню')
btnHabrNews = KeyboardButton('Habr')
btnPikabu = KeyboardButton('Pikabu')

# --- Main menu ---
btnIrkRuNews = KeyboardButton('Новости Иркутска')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnIrkRuNews, btnHabrNews, btnPikabu)

# --- irk.ru menu ---
btnIrkNews = KeyboardButton('Последние новости Иркутска')
btnIrkFreshNews = KeyboardButton('Свежие новости Иркутска')
irkMenu = ReplyKeyboardMarkup(resize_keyboard=True) \
    .add(btnIrkNews, btnIrkFreshNews) \
    .row(btnMain)

# --- Habr menu ---
btnHabrArticles = KeyboardButton('Последние статьи Habr')
btnHabrFreshArticles = KeyboardButton('Свежие статьи Habr')
btnHabrNews = KeyboardButton('Последние новости Habr')
btnHabrFreshNews = KeyboardButton('Свежие новости Habr')
habrMenu = ReplyKeyboardMarkup(resize_keyboard=True) \
    .add(btnHabrArticles, btnHabrFreshArticles) \
    .add(btnHabrNews, btnHabrFreshNews) \
    .row(btnMain)

# --- Pikabu menu ---
btnPikabuBest = KeyboardButton('Лучшее Pikabu')
btnPikabuMobilization = KeyboardButton('Мобилизация Pikabu')
pikabuMenu = ReplyKeyboardMarkup(resize_keyboard=True) \
    .add(btnPikabuBest, btnPikabuMobilization) \
    .row(btnMain)
