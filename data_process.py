import re
from collections import defaultdict
import pandas as pd

deleted_text_counter_j = defaultdict(int)
deleted_text_counter_l = defaultdict(int)


# 自定义函数，用于删除被 "[]" 包围的文字并更新统计字典
def remove_bracketed_text_and_count_j(s):
    # 使用正则表达式找到所有被 "[]" 包围的文字
    bracketed_texts = re.findall(r"\[(.*?)\]", s)

    # 更新统计字典
    for text in bracketed_texts:
        deleted_text_counter_j[text] += 1

    # 删除被 "[]" 包围的文字
    return re.sub(r"\[.*?\]", "", s)


def remove_bracketed_text_and_count_l(s):
    # 使用正则表达式找到所有被 "[]" 包围的文字
    bracketed_texts = re.findall(r"\[(.*?)\]", s)

    # 更新统计字典
    for text in bracketed_texts:
        deleted_text_counter_l[text] += 1

    # 删除被 "[]" 包围的文字
    return re.sub(r"\[.*?\]", "", s)


def not_start_with_msg(value):
    return not value.startswith("<")


def sort_dicts(dict1, dict2):
    # 合并两个字典的键并去重
    all_keys = set(dict1.keys()) | set(dict2.keys())
    # 对键进行排序
    sorted_keys = sorted(all_keys)
    # 创建两个新字典，按排序后的键存放键对
    sorted_dict1 = {key: dict1.get(key, None) for key in sorted_keys}
    sorted_dict2 = {key: dict2.get(key, None) for key in sorted_keys}

    return sorted_dict1, sorted_dict2


def process_data(df):
    columns = ["StrTime", "StrContent", "IsSender"]
    df = df[columns].copy()
    df.rename(columns={"StrTime": "time", "StrContent": "data"}, inplace=True)
    df = df.dropna(subset=["data"])
    df["data"] = df["data"].astype(str)
    df = df[df["data"].apply(not_start_with_msg)]
    is_sender_1 = df["IsSender"] == 1
    is_sender_0 = df["IsSender"] == 0
    j_df = df[is_sender_1].copy()
    l_df = df[is_sender_0].copy()
    j_df = j_df.drop("IsSender", axis=1)
    l_df = l_df.drop("IsSender", axis=1)

    j_df["data"] = j_df["data"].apply(remove_bracketed_text_and_count_j)
    l_df["data"] = l_df["data"].apply(remove_bracketed_text_and_count_l)

    j_df = j_df[j_df["data"].apply(len) > 0]
    l_df = l_df[l_df["data"].apply(len) > 0]

    all_keys = set(deleted_text_counter_j.keys()).union(
        set(deleted_text_counter_l.keys())
    )
    for key in all_keys:
        deleted_text_counter_j.setdefault(key, 0)
        deleted_text_counter_l.setdefault(key, 0)

    l_df.to_excel("data/柠檬.xlsx", index=False)
    j_df.to_excel("data/橙子.xlsx", index=False)

    emoji_df_j = pd.DataFrame(
        list(deleted_text_counter_j.items()), columns=["data", "count"]
    )
    emoji_df_l = pd.DataFrame(
        list(deleted_text_counter_l.items()), columns=["data", "count"]
    )
    emoji_df_j = emoji_df_j.sort_values(by="count", ascending=False)
    emoji_df_l = emoji_df_l.sort_values(by="count", ascending=False)
    emoji_df_j.to_excel("data/emoji_j.xlsx", index=False)
    emoji_df_l.to_excel("data/emoji_l.xlsx", index=False)
    j, l = sort_dicts(deleted_text_counter_j, deleted_text_counter_l)
    return l_df, j, l
