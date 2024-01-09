import re
from collections import defaultdict
import pandas as pd

# 字典初始化
emoji_j = defaultdict(int)
emoji_l = defaultdict(int)
bqb_j = defaultdict(int)
bqb_l = defaultdict(int)


# 自定义函数，用于删除被 "[]" 包围的文字并更新统计字典
def remove_bracketed_text_and_count_j(s):
    # 使用正则表达式找到所有被 "[]" 包围的文字
    bracketed_texts = re.findall(r"\[(.*?)\]", s)

    # 更新统计字典
    for text in bracketed_texts:
        emoji_j[text] += 1

    # 删除被 "[]" 包围的文字
    return re.sub(r"\[.*?\]", "", s)


def remove_bracketed_text_and_count_l(s):
    # 使用正则表达式找到所有被 "[]" 包围的文字
    bracketed_texts = re.findall(r"\[(.*?)\]", s)

    # 更新统计字典
    for text in bracketed_texts:
        emoji_l[text] += 1

    # 删除被 "[]" 包围的文字
    return re.sub(r"\[.*?\]", "", s)


def not_start_with_msg(value):
    return not value.startswith("<")


def start_with_msg(value):
    return value.startswith("<")


def sort_dicts(dict1, dict2):
    # 合并两个字典的键并去重
    all_keys = set(dict1.keys()) | set(dict2.keys())
    # 对键进行排序
    sorted_keys = sorted(all_keys)
    # 创建两个新字典，按排序后的键存放键对
    sorted_dict1 = {key: dict1.get(key, None) for key in sorted_keys}
    sorted_dict2 = {key: dict2.get(key, None) for key in sorted_keys}

    return sorted_dict1, sorted_dict2


def process_emoji(j_df, l_df):
    # 统计和删除emoji
    j_df["data"] = j_df["data"].apply(remove_bracketed_text_and_count_j)
    l_df["data"] = l_df["data"].apply(remove_bracketed_text_and_count_l)

    # 清洗数据
    j_df = j_df[j_df["data"].apply(len) > 0]
    l_df = l_df[l_df["data"].apply(len) > 0]

    # 合并两个字典的键并去重
    all_keys = set(emoji_j.keys()).union(set(emoji_l.keys()))
    for key in all_keys:
        emoji_j.setdefault(key, 0)
        emoji_l.setdefault(key, 0)

    # 转化为df
    emoji_df_j = pd.DataFrame(list(emoji_j.items()), columns=["data", "count"])
    emoji_df_l = pd.DataFrame(list(emoji_l.items()), columns=["data", "count"])

    # 排序
    emoji_df_j = emoji_df_j.sort_values(by="count", ascending=False)
    emoji_df_l = emoji_df_l.sort_values(by="count", ascending=False)

    # 保存
    emoji_df_j.to_excel("data/emoji/emoji_j.xlsx", index=False)
    emoji_df_l.to_excel("data/emoji/emoji_l.xlsx", index=False)

    # 按照一个顺序排列
    emoji_j_sorted, emoji_l_sorted = sort_dicts(emoji_j, emoji_l)
    return j_df, l_df, emoji_j_sorted, emoji_l_sorted


def extract_androidmd5(text):
    match = re.search(r'androidmd5="([^"]*)"', text)
    return match.group(1) if match else None


def process_biaoqingbao(j_df, l_df):
    # 分离表情包
    j_df_bqb = j_df[j_df["data"].apply(start_with_msg)]
    l_df_bqb = l_df[l_df["data"].apply(start_with_msg)]
    j_df = j_df[j_df["data"].apply(not_start_with_msg)]
    l_df = l_df[l_df["data"].apply(not_start_with_msg)]

    # 处理数据
    j_df_bqb = j_df_bqb.copy()
    j_df_bqb["data"] = j_df_bqb["data"].apply(extract_androidmd5)

    l_df_bqb = l_df_bqb.copy()
    l_df_bqb["data"] = l_df_bqb["data"].apply(extract_androidmd5)

    # 统计表情包
    value_counts = j_df_bqb["data"].value_counts()
    j_df_bqb = value_counts.reset_index()
    j_df_bqb.columns = ["data", "count"]
    value_counts = l_df_bqb["data"].value_counts()
    l_df_bqb = value_counts.reset_index()
    l_df_bqb.columns = ["data", "count"]

    j_df_bqb = j_df_bqb.sort_values(by="count", ascending=False)
    l_df_bqb = l_df_bqb.sort_values(by="count", ascending=False)

    j_df_bqb.to_excel("data/bqb/bqb_j.xlsx", index=False)
    l_df_bqb.to_excel("data/bqb/bqb_l.xlsx", index=False)
    return j_df, l_df, j_df_bqb, l_df_bqb


def process_data(df):
    # 提取数据
    columns = ["StrTime", "StrContent", "IsSender"]
    df = df[columns].copy()
    df.rename(columns={"StrTime": "time", "StrContent": "data"}, inplace=True)

    # 清洗数据
    df = df.dropna(subset=["data"])
    df["data"] = df["data"].astype(str)

    # 分类数据
    is_sender_1 = df["IsSender"] == 1
    is_sender_0 = df["IsSender"] == 0
    j_df = df[is_sender_1].copy()
    l_df = df[is_sender_0].copy()
    j_df = j_df.drop("IsSender", axis=1)
    l_df = l_df.drop("IsSender", axis=1)

    # 分离表情包
    j_df, l_df, j_df_bqb, l_df_bqb = process_biaoqingbao(j_df, l_df)

    # 分离emoji
    j_df, l_df, emoji_j, emoji_l = process_emoji(j_df, l_df)

    l_df.to_excel("data/柠檬.xlsx", index=False)
    j_df.to_excel("data/橙子.xlsx", index=False)

    return j_df, l_df, emoji_j, emoji_l, j_df_bqb, l_df_bqb
