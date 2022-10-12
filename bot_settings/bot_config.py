import configparser

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8-sig')
# config.read('../config.ini', encoding='utf-8-sig')

irk_ru_url = "https://www.irk.ru/news/"
habr_news_url = "https://habr.com/ru/news/"
habr_articles_url = "https://habr.com/ru/all/"
pikabu_mobilization_url = 'https://pikabu.ru/tag/Мобилизация'
pikabu_best_url = 'https://pikabu.ru/best'

token = config['tg']['token']
user_id = config['tg']['user_id']
