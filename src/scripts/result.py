import numpy as np


def calcResult(main_df, preds):
    agree, disagree = 0, 0
    agree_idx, disagree_idx = [], []

    for count, pred in enumerate(preds):
        if np.amax(pred) == pred[1] or np.amax(pred) == pred[2]:
            disagree_idx.append(count)
            disagree += 1

        elif np.amax(pred) == pred[0] or np.amax(pred) == pred[3]:
            agree_idx.append(count)
            agree += 1

    return agree / (agree + disagree), agree_idx, disagree_idx
