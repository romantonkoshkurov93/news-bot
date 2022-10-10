import asyncio
import json
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink

from bot_settings import kb_markup as nav
from bot_settings.bot_config import token, token_test, user_id, irk_ru_url, habr_news_url

from scripts.irk_news import check_irk_news_update
from scripts.habr_news import check_habr_news_update

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

logging.basicConfig(
    level=logging.DEBUG,
    filename="news_bot.log",
    format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt='%H:%M:%S',
)


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Привет {0.first_name}'.format(message.from_user),
                           reply_markup=nav.mainMenu)


# --- Irk all news ---
@dp.message_handler(Text(equals="Последние новости Иркутска"))
async def get_last_five_irk_news(message: types.Message):
    logging.info('[INFO] | Get last 5 irk news.')
    with open('dicts/irk_news.json') as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items())[-5:]:
        news = f"{hbold(v['dict_id'])}\n\n" \
               f"{hbold(v['date_time'])}\n" \
               f"{hlink(v['news_title'], v['news_url'])}"

        await message.answer(news)


# --- Irk fresh news ---
@dp.message_handler(Text(equals="Свежие новости Иркутска"))
async def get_fresh_irk_news(message: types.Message):
    logging.info('[INFO] | Check fresh irk news')
    fresh_irk_news = check_irk_news_update(irk_ru_url)

    if len(fresh_irk_news) >= 1:
        for k, v in sorted(fresh_irk_news.items()):
            news = f"{hbold(v['dict_id'])}\n\n" \
                   f"{hbold(v['date_time'])}\n" \
                   f"{hlink(v['news_title'], v['news_url'])}"
            await message.answer(news)
    else:
        await message.answer("Пока нет свежих новостей")


# --- Habr all news ---
@dp.message_handler(Text(equals="Последние новости Habr"))
async def get_last_five_habr_news(message: types.Message):
    logging.info('[INFO] | Get last 5 habr news.')
    with open('dicts/habr_news.json') as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items())[-5:]:
        news = f"{hbold(v['dict_id'])}\n\n" \
               f"{hbold(v['date_time'])}\n" \
               f"{hlink(v['news_title'], v['news_url'])}"

        await message.answer(news)


@dp.message_handler(Text(equals="Свежие новости Habr"))
async def get_fresh_habr_news(message: types.Message):
    logging.info('[INFO] | Check fresh habr news')
    fresh_habr_news = check_habr_news_update(habr_news_url)

    if len(fresh_habr_news) >= 1:
        for k, v in sorted(fresh_habr_news.items()):
            news = f"{hbold(v['dict_id'])}\n\n" \
                   f"{hbold(v['date_time'])}\n" \
                   f"{hlink(v['news_title'], v['news_url'])}"
            await message.answer(news)
    else:
        await message.answer("Пока нет свежих новостей")


async def irk_news_every_hour():
    while True:
        irk_fresh_news = check_irk_news_update(irk_ru_url)

        if len(irk_fresh_news) >= 1:
            for k, v in sorted(irk_fresh_news.items()):
                irk_news = f"{hbold(v['dict_id'])}\n\n" \
                           f"{hbold(v['date_time'])}\n" \
                           f"{hlink(v['news_title'], v['news_url'])}"
                await bot.send_message(user_id, irk_news)

        await asyncio.sleep(3600)


async def habr_news_every_hour():
    while True:
        habr_fresh_news = check_habr_news_update(habr_news_url)

        if len(habr_fresh_news) >= 1:
            for k, v in sorted(habr_fresh_news.items()):
                habr_news = f"{hbold(v['dict_id'])}\n\n" \
                            f"{hbold(v['date_time'])}\n" \
                            f"{hlink(v['news_title'], v['news_url'])}"
                await bot.send_message(user_id, habr_news)

        await asyncio.sleep(3600)


@dp.message_handler()
async def bot_message(message: types.Message):
    if message.text == '⬅ Главное меню':
        await bot.send_message(message.from_user.id, '⬅ Главное меню', reply_markup=nav.mainMenu)
    elif message.text == 'Новости Иркутска':
        await bot.send_message(message.from_user.id, 'Новости Иркутска', reply_markup=nav.irkMenu)
    elif message.text == 'Habr':
        await bot.send_message(message.from_user.id, 'Habr', reply_markup=nav.habrMenu)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [
        loop.create_task(irk_news_every_hour()),
        loop.create_task(habr_news_every_hour())
    ]
    executor.start_polling(dp)
