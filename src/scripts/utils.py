import json
import os
import string

import numpy as np
import pandas as pd
import requests
from dotenv import load_dotenv
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
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


def delExisting():
    dir_name = os.path.join(
        os.path.dirname(os.path.dirname(os.getcwd())), "data/operational"
    )

    for file in os.listdir(dir_name):
        if file.endswith(".txt") or file.endswith(".json"):
            os.remove(os.path.join(dir_name, file))


def saveData(articles_data, save_path):
    with open(save_path, "w+") as json_file:
        json.dump(articles_data, json_file, ensure_ascii=False, indent=4)


def loadData(save_path):
    main_df = pd.read_json(save_path)
    stance_df = main_df.loc[:, ["text", "title"]]

    return main_df, stance_df


def discardStanceArticle(df, preds):
    for count, pred in enumerate(preds):
        # ['unrelated' 'agree' 'discuss' 'disagree']
        if np.amax(pred) == pred[0] or np.amax(pred) == pred[3]:
            df = df.drop(count)

    return df


def discardFakeArticle(df, preds):
    for count, pred in enumerate(preds):
        # ['real', 'fake']
        if pred[0] < pred[1]:
            df = df.drop(count)

    return df


def cleanString(ip_str):
    ip_str = ip_str.translate(str.maketrans("", "", string.punctuation))
    str_tokens = word_tokenize(ip_str)

    return " ".join(
        [word for word in str_tokens if word not in stopwords.words("english")]
    )
