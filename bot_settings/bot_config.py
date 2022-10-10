import configparser

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8-sig')

irk_ru_url = "https://www.irk.ru/news/"
habr_news_url = "https://habr.com/ru/news/"
habr_articles_url = "https://habr.com/ru/all/"

token = config['tg']['token']
token_test = config['tg']['token_test']
user_id = config['tg']['user_id']
