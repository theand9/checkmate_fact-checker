import json
import os

import newspaper
import requests
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


def saveData(articles_data):
    with open(
        os.path.join(
            os.path.dirname(os.path.dirname(os.getcwd())),
            "data/query/query_result.json",
        ),
        "w+",
    ) as json_file:
        json.dump(articles_data, json_file, ensure_ascii=False, indent=4)


def genArticleData(articles):
    articles_data = []
    for article_data in enumerate(articles):
        article_author = article_data["author"]
        article_title = article_data["title"]
        article_website = article_data["source"]["name"]
        article_url = article_data["url"]
        article_date = article_data["publishedAt"]

        article = requests.get(article_url).text
        article_text = newspaper.fulltext(article)
        article_text = article_text.replace("\n", "")
        article_text = article_text.replace("\t", "")

        article_data = {
            "url": article_url,
            "website": article_website,
            "date": article_date,
            "title": article_title,
            "author": article_author,
            "text": article_text,
        }

        articles_data.append(article_data)

    saveData(articles_data)


def delExisting():
    dir_name = os.path.join(
        os.path.dirname(os.path.dirname(os.getcwd())), "data/query/"
    )

    for file in os.listdir(dir_name):
        if file.endswith(".txt") or file.endswith(".json"):
            os.remove(os.path.join(dir_name, file))


if __name__ == "__main__":
    delExisting()

    ip_fact = input("Enter the fact that you wish to scrape articles for: ")

    url = f"https://newsapi.org/v2/everything?q={ip_fact}&apiKey="
    json_dump = webRequest(url)

    genArticleData(json_dump["articles"])
