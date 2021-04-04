import json
import os

import newspaper
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from requests.exceptions import HTTPError


def webRequest(url):
    """
    Basic Web Request and url builder.

    Returns:
        response object -- output of webpage
        None -- if error occurs
    """
    load_dotenv()
    url += os.environ.get("API_KEY")

    try:
        response = requests.get(url)
        response.raise_for_status()

        return response.json()

    except HTTPError as HttpError:
        print(f"An HTTP error has occurred: {HttpError}")

    except Exception as OtherError:
        print(f"Some Other Error has occurred: {OtherError}")

    return None


def saveData(article_data):
    with open(
        os.path.join(
            os.path.dirname(os.path.dirname(os.getcwd())),
            f"data/query/{article_data['headline']}.json",
        ),
        "w+",
    ) as json_file:
        json.dump(article_data, json_file, ensure_ascii=False, indent=4)


def genArticleData(url_list):
    for url in url_list:
        article = requests.get(url).text

        soup = BeautifulSoup(article, features="lxml")
        meta = json.loads(soup.find("script", type="application/ld+json").string)

        article_url = meta["url"]
        article_website = article_url.split("//")[-1].split("/")[0].split("?")[0]
        article_headline = meta["headline"]
        try:
            article_author = meta["author"][0]["name"]
        except KeyError:
            article_author = None
        article_date = meta["datePublished"]
        article_text = newspaper.fulltext(article)

        article_data = {
            "url": article_url,
            "website": article_website,
            "date": article_date,
            "headline": article_headline,
            "author": article_author,
            "text": article_text,
        }

        saveData(article_data)


def delExisting():
    dir_name = os.path.join(
        os.path.dirname(os.path.dirname(os.getcwd())), "data/query/"
    )

    for file in os.listdir(dir_name):
        if file.endswith(".txt"):
            os.remove(os.path.join(dir_name, file))


if __name__ == "__main__":
    delExisting()

    ip_fact = input("Enter the fact that you wish to scrape articles for: ")

    url = f"https://newsapi.org/v2/everything?q={ip_fact}&apiKey="
    json_dump = webRequest(url)
    url_list = [i[j] for i in json_dump["articles"] for j in i if j == "url"]

    genArticleData(url_list)
