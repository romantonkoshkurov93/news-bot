import json

import requests

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from datetime import datetime

from bot_settings.bot_config import irk_ru_url as root_url


ua = UserAgent()


def get_all_irk_news(url):

    headers = {
        'Host': 'www.irk.ru',
        'User-Agent': f'{ua.random}',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
    }

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    news_cards = soup.find_all('li', class_='b-news-article-list-item')

    news_dict = {}
    for news in news_cards:
        dict_id = '#irk_news'
        news_title = news.findNext('h2').text.strip()
        news_url = f'https://www.irk.ru{news.findNext("a").get("href")}'

        news_date_time = news.find("time").get("datetime")
        date_from_iso = datetime.fromisoformat(news_date_time)
        date_time = datetime.strftime(date_from_iso, "%Y-%m-%d %H:%M:%S")

        news_id = "".join(
            [news_date_time[i] for i in range(len(news_date_time)) if news_date_time[i] in '0123456789'][3:]
        )

        news_dict[news_id] = {
            "dict_id": dict_id,
            "date_time": date_time,
            "news_title": news_title,
            "news_url": news_url
        }

    with open("dicts/irk_news.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)


def check_irk_news_update(url):
    with open("dicts/irk_news.json") as file:
        news_dict = json.load(file)

    headers = {
        'Host': 'www.irk.ru',
        'User-Agent': f'{ua.random}',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
    }

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    news_cards = soup.find_all('li', class_='b-news-article-list-item')

    fresh_news = {}
    for news in news_cards:
        news_date_time = news.find("time").get("datetime")
        date_from_iso = datetime.fromisoformat(news_date_time)
        date_time = datetime.strftime(date_from_iso, "%Y-%m-%d %H:%M:%S")

        news_id = "".join(
            [news_date_time[i] for i in range(len(news_date_time)) if news_date_time[i] in '0123456789'][3:]
        )

        if news_id in news_dict:
            continue
        else:
            dict_id = '#irk_news'
            news_title = news.findNext('h2').text.strip()
            news_url = f'https://www.irk.ru{news.findNext("a").get("href")}'

            news_dict[news_id] = {
                "dict_id": dict_id,
                "date_time": date_time,
                "news_title": news_title,
                "news_url": news_url
            }

            fresh_news[news_id] = {
                "dict_id": dict_id,
                "date_time": date_time,
                "news_title": news_title,
                "news_url": news_url
            }

    with open("dicts/irk_news.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return fresh_news


def main():
    # get_all_irk_news(root_url)
    print(check_irk_news_update(root_url))


if __name__ == '__main__':
    main()
