import json
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from bot_settings.bot_config import habr_news_url


def get_response(url):
    ua = UserAgent()

    headers = {
        'User-Agent': f'{ua.random}',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    return soup


def save_file(dict):
    with open('dicts/habr_news.json', 'w') as file:
        json.dump(dict, file, indent=4, ensure_ascii=False)


def open_file():
    with open('dicts/habr_news.json') as file:
        return json.load(file)


def get_all_habr_news(url):
    soup = get_response(url)

    news_cards = soup.find_all('div', class_='tm-article-snippet')
    news_dict = {}
    for news in news_cards:
        dict_id = '#habr_news'
        news_title = news.find('h2', class_='tm-article-snippet__title_h2').text.strip()
        news_url = f'https://habr.com{news.find("a", class_="tm-article-snippet__title-link").get("href")}'

        news_datetime = news.find('time').get('datetime')
        d2 = datetime.strptime(news_datetime, '%Y-%m-%dT%H:%M:%S.%fZ')
        date_from_iso = datetime.fromisoformat(str(d2))
        date_time = datetime.strftime(date_from_iso, '%Y-%m-%d %H:%M:%S')

        news_id = news_url.split('/')[-2]

        news_dict[news_id] = {
            'dict_id': dict_id,
            'date_time': date_time,
            'news_title': news_title,
            'news_url': news_url
        }

    save_file(news_dict)


def check_habr_news_update(url):
    news_dict = open_file()
    soup = get_response(url)

    news_cards = soup.find_all('div', class_='tm-article-snippet')
    fresh_news = {}
    for news in news_cards:
        news_url = f'https://habr.com{news.find("a", class_="tm-article-snippet__title-link").get("href")}'
        news_id = news_url.split('/')[-2]

        if news_id in news_dict:
            continue
        else:
            dict_id = '#habr_news'
            news_title = news.find('h2', class_='tm-article-snippet__title_h2').text.strip()

            news_datetime = news.find('time').get('datetime')
            d2 = datetime.strptime(news_datetime, '%Y-%m-%dT%H:%M:%S.%fZ')
            date_from_iso = datetime.fromisoformat(str(d2))
            date_time = datetime.strftime(date_from_iso, '%Y-%m-%d %H:%M:%S')

            news_dict[news_id] = {
                'dict_id': dict_id,
                'date_time': date_time,
                'news_title': news_title,
                'news_url': news_url
            }

            fresh_news[news_id] = {
                'dict_id': dict_id,
                'date_time': date_time,
                'news_title': news_title,
                'news_url': news_url
            }

    save_file(news_dict)

    return fresh_news


def habr_news_main():
    get_all_habr_news(habr_news_url)
    print(check_habr_news_update(habr_news_url))


if __name__ == '__main__':
    habr_news_main()
