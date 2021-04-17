import os

import nltk
import numpy as np
import pandas as pd
from keras.models import load_model
from keras.preprocessing.text import Tokenizer, text_to_word_sequence


def discardArticle(main_df, preds):
    for count, pred in enumerate(preds):
        # ['unrelated' 'agree' 'discuss' 'disagree']
        if np.amax(pred) == pred[0] or np.amax(pred) == pred[3]:
            main_df = main_df.drop(count)

    return main_df


def predictStance(data_text, data_heading):
    model = load_model(f"{helper_path}/src/models/stance/")

    return model.predict([data_text, data_heading])


def procDataStance(stance_df, helper_path):
    t = Tokenizer(num_words=20000, filters='!"#$%&()*+,-./:;<=>?@[]^_`{|}\n\t"~\\')
    t.fit_on_texts(stance_df["text"])
    t.fit_on_texts(stance_df["title"])

    texts, articles_text, articles_heading = [], [], []

    for idx in range(stance_df["text"].shape[0]):
        text = stance_df["text"][idx]
        texts.append(text)
        sentences_text = nltk.tokenize.sent_tokenize(text)
        articles_text.append(sentences_text)

        heading = stance_df["title"][idx]
        sentences_heading = nltk.tokenize.sent_tokenize(heading)
        articles_heading.append(sentences_heading)

    data_text = np.zeros((len(texts), 20, 20), dtype="int32")
    data_heading = np.zeros((len(texts), 1, 20), dtype="int32")

    for i, sentences_text in enumerate(articles_text):
        for j, sent in enumerate(sentences_text):
            if j < 20:
                wordTokens = text_to_word_sequence(sent)
                k = 0
            for word in wordTokens:
                try:
                    if k < 20 and t.word_index[word] < 20000:
                        data_text[i, j, k] = t.word_index[word]
                        k += 1
                except Exception:
                    pass

    for i, sentences_heading in enumerate(articles_heading):
        for j, sent in enumerate(sentences_heading):
            if j < 1:
                wordTokens = text_to_word_sequence(sent)
                k = 0
                for word in wordTokens:
                    try:
                        if k < 20 and t.word_index[word] < 20000:
                            data_heading[i, j, k] = t.word_index[word]
                            k += 1
                    except Exception:
                        pass

    return predictStance(data_text, data_heading)


def loadData(data_path):
    main_df = pd.read_json(f"{helper_path}/data/query/query_result.json")
    stance_df = main_df.loc[:, ["text", "title"]]

    return main_df, stance_df


if __name__ == "__main__":
    helper_path = os.path.dirname(os.path.dirname(os.getcwd()))

    main_df, stance_df = loadData(helper_path)
    preds = procDataStance(stance_df, helper_path)

    main_df = discardArticle(main_df, preds)
