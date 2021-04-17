import newspaper
import requests


def genArticleData(articles):
    articles_data = []

    for article_data in articles:
        article_author = article_data["author"]
        article_title = article_data["title"]
        article_website = article_data["source"]["name"]
        article_url = article_data["url"]
        article_date = article_data["publishedAt"]

        try:
            article_text = requests.get(article_url).text
            article_text = newspaper.fulltext(article_text)
            article_text = article_text.replace("\n", "")
            article_text = article_text.replace("\t", "")
        except Exception:
            continue

        article_data = {
            "url": article_url,
            "website": article_website,
            "date": article_date,
            "title": article_title,
            "author": article_author,
            "text": article_text,
        }

        articles_data.append(article_data)

    return articles_data
