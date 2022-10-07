import configparser

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8-sig')

irk_ru_url = "https://www.irk.ru/news/"

token = config['tg']['token']
token_test = config['tg']['token_test']
user_id = config['tg']['user_id']
