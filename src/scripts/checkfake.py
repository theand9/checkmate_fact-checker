import dill
from utils import cleanString


def predictFake(check_fake_df, helper_path):
    with open(f"{helper_path}/src/models/fake_news/model.pkl", "rb") as fptr:
        model = dill.load(fptr)

    return model.predict_proba(check_fake_df.values.tolist())


def procDataFake(check_fake_df, helper_path):
    check_fake_df["text"] = check_fake_df["text"].apply(cleanString)
    check_fake_df["title"] = check_fake_df["title"].apply(cleanString)
    temp = check_fake_df[["title", "author", "text"]].copy()

    return predictFake(temp, helper_path)
