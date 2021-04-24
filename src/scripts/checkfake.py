import joblib
from utils import cleanString


def predictFake(check_fake_df, helper_path):
    model = joblib.load(f"{helper_path}/src/models/fake_news/model.joblib")

    return model.predict_proba(check_fake_df["text"])


def procDataFake(check_fake_df, helper_path):
    check_fake_df["text"] = check_fake_df["text"].apply(cleanString)
    check_fake_df["title"] = check_fake_df["title"].apply(cleanString)

    return predictFake(check_fake_df, helper_path)
