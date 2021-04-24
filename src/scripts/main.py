import os

from checkfake import procDataFake
from result import calcResult
from retrieve import genArticleData
from stance import procDataStance
from utils import (
    cleanString,
    delExisting,
    discardFakeArticle,
    loadData,
    saveData,
    webRequest,
)

if __name__ == "__main__":
    # Base
    delExisting()
    helper_path = os.path.dirname(os.path.dirname(os.getcwd()))
    print("Base Completed")

    # Fact Data Retrieval and Save
    fact_query = input("Enter the fact that you wish to scrape articles for: ")
    clean_query = cleanString(fact_query)

    url = f"https://newsapi.org/v2/everything?q={clean_query}&apiKey="
    json_dump = webRequest(url)

    save_path = os.path.join(helper_path, "data/operational/query_result.json")
    articles_data = genArticleData(json_dump["articles"])
    saveData(articles_data, save_path)
    print("Data Saved")

    # Stance Prediction 1
    main_df, model_df = loadData(save_path)
    preds = procDataStance(model_df, helper_path)

    print("Stance Detection 1 Complete")

    # Fake News Detection
    main_df, model_df = loadData(save_path)
    preds = procDataFake(model_df, helper_path)

    model_df = discardFakeArticle(model_df, preds)
    main_df = discardFakeArticle(main_df, preds)
    print("Fake News Detection Complete")

    # Stance Detection 2
    stance_df = main_df.loc[:, ["text"]]
    stance_df["title"] = [fact_query] * len(stance_df.index)

    preds = procDataStance(stance_df, helper_path)

    # Final Result
    conf_score, agree_idx, disagree_idx = calcResult(main_df, preds)
    print(
        f"\nThe fact '{fact_query}' can be said to be true with {round(conf_score, 4)*100}% confidence."
    )

    agree_df = main_df.iloc[agree_idx]
    save_path = os.path.join(helper_path, "data/operational/agree.json")
    agree_df.to_json(save_path, orient="records", force_ascii=False, indent=4)

    disagree_df = main_df.iloc[disagree_idx]
    save_path = os.path.join(helper_path, "data/operational/disagree.json")
    disagree_df.to_json(save_path, orient="records", force_ascii=False, indent=4)

    print("Program Execution Complete. Please check agree.json and disagree.json")
