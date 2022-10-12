import asyncio
import json
import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink

from bot_settings import kb_markup as nav
from bot_settings.bot_config import token, user_id, habr_articles_url, habr_news_url, irk_ru_url, pikabu_best_url, \
    pikabu_mobilization_url

from scripts.habr_articles import check_habr_articles_update
from scripts.habr_news import check_habr_news_update
from scripts.irk_news import check_irk_news_update
from scripts.pikabu_articles import check_pikabu_update

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

logging.basicConfig(
    level=logging.DEBUG,
    filename='news_bot.log',
    format='%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s',
    datefmt='%H:%M:%S',
)


def return_article_dict(k, v):
    articles = f'{hbold(v["dict_id"])}\n\n' \
               f'{hbold(v["date_time"])}\n' \
               f'{hlink(v["article_title"], v["article_url"])}'
    return articles


def return_news_dict(k, v):
    news = f'{hbold(v["dict_id"])}\n\n' \
           f'{hbold(v["date_time"])}\n' \
           f'{hlink(v["news_title"], v["news_url"])}'
    return news


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Привет {0.first_name}'.format(message.from_user),
                           reply_markup=nav.mainMenu)


# Habr all articles script
@dp.message_handler(Text(equals='Последние статьи Habr'))
async def get_last_five_habr_articles(message: types.Message):
    logging.info('Get last 5 HABR articles')
    with open('dicts/habr_articles.json') as file:
        articles_dict = json.load(file)

    for k, v in sorted(articles_dict.items())[-5:]:
        articles = return_article_dict(k, v)
        await message.answer(articles)


# Habr fresh articles script
@dp.message_handler(Text(equals='Свежие статьи Habr'))
async def get_fresh_habr_articles(message: types.Message):
    logging.info('Check fresh HABR articles')
    fresh_habr_articles = check_habr_articles_update(habr_articles_url)

    if len(fresh_habr_articles) >= 1:
        for k, v in sorted(fresh_habr_articles.items()):
            articles = return_article_dict(k, v)
            await message.answer(articles)
    else:
        await message.answer('Пока нет свежих статей')


# Habr all news script
@dp.message_handler(Text(equals='Последние новости Habr'))
async def get_all_habr_news(message: types.Message):
    logging.info('Get last 5 HABR news')
    with open('dicts/habr_news.json') as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items())[-5:]:
        news = return_news_dict(k, v)
        await message.answer(news)


# Habr fresh news script
@dp.message_handler(Text(equals='Свежие новости Habr'))
async def get_fresh_habr_news(message: types.Message):
    logging.info('Check fresh HABR news')
    fresh_news = check_habr_news_update(habr_news_url)

    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items()):
            news = return_news_dict(k, v)
            await message.answer(news)
    else:
        await message.answer('Пока нет свежих новостей')


# Irk all news script
@dp.message_handler(Text(equals='Последние новости Иркутска'))
async def get_all_irk_news(message: types.Message):
    logging.info('Get last 5 IRK news')
    with open('dicts/irk_news.json') as file:
        news_dict = json.load(file)

    for k, v in sorted(news_dict.items())[-5:]:
        news = return_news_dict(k, v)
        await message.answer(news)


# Irk fresh news script
@dp.message_handler(Text(equals='Свежие новости Иркутска'))
async def get_fresh_irk_news(message: types.Message):
    logging.info('Check fresh IRK news')
    fresh_news = check_irk_news_update(irk_ru_url)

    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items()):
            news = return_news_dict(k, v)
            await message.answer(news)
    else:
        await message.answer('Пока нет свежих новостей')


# Pikabu fresh articles script [BEST]
@dp.message_handler(Text(equals='Лучшее Pikabu'))
async def get_fresh_pikabu_best_articles(message: types.Message):
    logging.info('Check fresh PIKABU BEST articles')
    fresh_articles = check_pikabu_update(pikabu_best_url)

    if len(fresh_articles) >= 1:
        for k, v in sorted(fresh_articles.items()):
            articles = return_article_dict(k, v)
            await message.answer(articles)
    else:
        await message.answer('Пока нет свежих статей')


# Pikabu fresh articles script [Mobilization]
@dp.message_handler(Text(equals='Мобилизация Pikabu'))
async def check_fresh_pikabu_mobilization_articles(message: types.Message):
    logging.info('Check fresh PIKABU MOBILIZATION articles')
    fresh_articles = check_pikabu_update(pikabu_mobilization_url)

    if len(fresh_articles) >= 1:
        for k, v in sorted(fresh_articles.items()):
            articles = return_article_dict(k, v)
            await message.answer(articles)
    else:
        await message.answer('Пока нет свежих статей')


async def habr_articles_every_hour():
    while True:
        habr_articles = check_habr_articles_update(habr_articles_url)

        if len(habr_articles) >= 1:
            for k, v in sorted(habr_articles.items()):
                articles = return_article_dict(k, v)
                await bot.send_message(user_id, articles)
        await asyncio.sleep(3600)


async def habr_news_every_hour():
    while True:
        habr_news = check_habr_news_update(habr_news_url)

        if len(habr_news) >= 1:
            for k, v in sorted(habr_news.items()):
                news = return_news_dict(k, v)
                await bot.send_message(user_id, news)
        await asyncio.sleep(3600)


async def irk_news_every_hour():
    while True:
        irk_news = check_irk_news_update(irk_ru_url)

        if len(irk_news) >= 1:
            for k, v in sorted(irk_news.items()):
                news = return_news_dict(k, v)
                await bot.send_message(user_id, news)
        await asyncio.sleep(3600)


async def pikabu_best_articles_every_hour():
    while True:
        fresh_articles = check_pikabu_update(pikabu_best_url)

        if len(fresh_articles) >= 1:
            for k, v in sorted(fresh_articles.items()):
                articles = return_article_dict(k, v)
                await bot.send_message(user_id, articles)
        await asyncio.sleep(3600)


async def pikabu_mobilization_articles_every_hour():
    while True:
        fresh_articles = check_pikabu_update(pikabu_mobilization_url)

        if len(fresh_articles) >= 1:
            for k, v in sorted(fresh_articles.items()):
                articles = return_article_dict(k, v)
                await bot.send_message(user_id, articles)
        await asyncio.sleep(3600)


@dp.message_handler()
async def bot_message(message: types.Message):
    if message.text == '⬅ Главное меню':
        await bot.send_message(message.from_user.id, '⬅ Главное меню', reply_markup=nav.mainMenu)
    elif message.text == 'Новости Иркутска':
        await bot.send_message(message.from_user.id, 'Новости Иркутска', reply_markup=nav.irkMenu)
    elif message.text == 'Habr':
        await bot.send_message(message.from_user.id, 'Habr', reply_markup=nav.habrMenu)
    elif message.text == 'Pikabu':
        await bot.send_message(message.from_user.id, 'Pikabu', reply_markup=nav.pikabuMenu)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    tasks = [
        loop.create_task(habr_articles_every_hour()),
        loop.create_task(habr_news_every_hour()),
        loop.create_task(irk_news_every_hour()),
        loop.create_task(pikabu_best_articles_every_hour()),
        loop.create_task(pikabu_mobilization_articles_every_hour())
    ]
    executor.start_polling(dp)
