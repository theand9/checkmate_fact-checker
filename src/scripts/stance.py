import nltk
import numpy as np
from keras.models import load_model
from keras.preprocessing.text import Tokenizer, text_to_word_sequence


def predictStance(data_text, data_heading, helper_path):
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

    return predictStance(data_text, data_heading, helper_path)
