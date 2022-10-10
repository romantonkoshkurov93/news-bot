import json
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from bot_settings.bot_config import habr_articles_url as root_url

ua = UserAgent()


def get_all_habr_articles(url):
    headers = {
        "User-Agent": f"{ua.random}",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    articles_cards = soup.find_all("div", class_="tm-article-snippet")

    articles_dict = {}
    for articles in articles_cards:
        dict_id = '#habr_articles'
        article_title = articles.select_one("h2:nth-child(2) > a:nth-child(1) > span:nth-child(1)").text
        article_url = f'https://habr.com{articles.find("a", class_="tm-article-snippet__title-link").get("href")}'

        article_date = articles.find("time").get("datetime")
        d2 = datetime.strptime(article_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        date_from_iso = datetime.fromisoformat(str(d2))
        date_time = datetime.strftime(date_from_iso, "%Y-%m-%d %H:%M:%S")

        article_id = "".join(
            [article_date[i] for i in range(len(article_date)) if article_date[i] in '0123456789'][3:12]
        )
        articles_dict[article_id] = {
            "dict_id": dict_id,
            "date_time": date_time,
            "article_title": article_title,
            "article_url": article_url
        }

    with open('dicts/habr_articles.json', 'w') as file:
        json.dump(articles_dict, file, indent=4, ensure_ascii=False)


def check_habr_fresh_articles(url):
    with open('dicts/habr_articles.json') as file:
        articles_dict = json.load(file)

    headers = {
        "User-Agent": f"{ua.random}",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')

    articles_cards = soup.find_all("div", class_="tm-article-snippet")

    fresh_articles = {}
    for articles in articles_cards:
        article_date = articles.find("time").get("datetime")
        d2 = datetime.strptime(article_date, "%Y-%m-%dT%H:%M:%S.%fZ")
        date_from_iso = datetime.fromisoformat(str(d2))
        date_time = datetime.strftime(date_from_iso, "%Y-%m-%d %H:%M:%S")

        article_id = "".join(
            [article_date[i] for i in range(len(article_date)) if article_date[i] in '0123456789'][3:12]
        )

        if article_id in articles_dict:
            continue
        else:

            dict_id = '#habr_articles'
            article_title = articles.select_one("h2:nth-child(2) > a:nth-child(1) > span:nth-child(1)").text
            article_url = f'https://habr.com{articles.find("a", class_="tm-article-snippet__title-link").get("href")}'

            articles_dict[article_id] = {
                "dict_id": dict_id,
                "date_time": date_time,
                "article_title": article_title,
                "article_url": article_url
            }

            fresh_articles[article_id] = {
                "dict_id": dict_id,
                "date_time": date_time,
                "article_title": article_title,
                "article_url": article_url
            }

    with open('dicts/habr_articles.json', 'w') as file:
        json.dump(articles_dict, file, indent=4, ensure_ascii=False)

    return fresh_articles


def main():
    # get_all_habr_articles(root_url)
    print(check_habr_fresh_articles(root_url))


if __name__ == '__main__':
    main()
