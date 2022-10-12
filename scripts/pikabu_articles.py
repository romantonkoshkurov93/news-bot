import json
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from bot_settings.bot_config import pikabu_mobilization_url, pikabu_best_url


def get_response(url):
    ua = UserAgent()

    headers = {
        'User-Agent': f'{ua.random}',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9 '
    }
    
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    return soup


def save_file(dict):
    with open('dicts/pikabu_articles.json', 'w') as file:
        json.dump(dict, file, indent=4, ensure_ascii=False)


def open_file():
    with open('dicts/pikabu_articles.json') as file:
        return json.load(file)


def get_all_pikabu_articles(url):
    soup = get_response(url)
    articles_cards = soup.find_all('article', class_='story')

    pikabu_dict = {}
    for articles in articles_cards:
        articles_script = articles.find('script').text
        articles_json = json.loads(articles_script)

        dict_id = '#pikabu'
        article_title = articles_json['name']
        article_url = articles_json['url']
        article_id = article_url.split('_')[-1]
        article_date = articles_json['datePublished']
        date_from_iso = datetime.fromisoformat(article_date)
        date_time = datetime.strftime(date_from_iso, '%Y-%m-%d %H:%M:%S')

        pikabu_dict[article_id] = {
            'dict_id': dict_id,
            'date_time': date_time,
            'article_title': article_title,
            'article_url': article_url
        }

    save_file(pikabu_dict)


def check_pikabu_update(url):
    pikabu_dict = open_file()
    soup = get_response(url)

    articles_cards = soup.find_all('article', class_='story')
    fresh_articles = {}
    for articles in articles_cards:
        articles_script = articles.find('script').text
        articles_json = json.loads(articles_script)

        article_url = articles_json['url']
        article_id = article_url.split('_')[-1]

        if article_id in pikabu_dict:
            continue
        else:
            dict_id = '#pikabu'
            article_title = articles_json['name']
            article_date = articles_json['datePublished']
            date_from_iso = datetime.fromisoformat(article_date)
            date_time = datetime.strftime(date_from_iso, '%Y-%m-%d %H:%M:%S')

            pikabu_dict[article_id] = {
                'dict_id': dict_id,
                'date_time': date_time,
                'article_title': article_title,
                'article_url': article_url
            }

            fresh_articles[article_id] = {
                'dict_id': dict_id,
                'date_time': date_time,
                'article_title': article_title,
                'article_url': article_url
            }

    save_file(pikabu_dict)

    return fresh_articles


def pikabu_articles_main():
    get_all_pikabu_articles(pikabu_mobilization_url)
    get_all_pikabu_articles(pikabu_best_url)
    print(check_pikabu_update(pikabu_mobilization_url))
    print(check_pikabu_update(pikabu_best_url))


if __name__ == '__main__':
    pikabu_articles_main()
