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


if __name__ == "__main__":
    ip_fact = input("Enter the fact that you wish to scrape articles for: ")

    url = f"https://newsapi.org/v2/everything?q={ip_fact}&apiKey="
    json_dump = webRequest(url)

    url_list = [i[j] for i in json_dump["articles"] for j in i if j == "url"]

    for i in url_list:
        article = requests.get(i).text
        print(newspaper.fulltext(article))
