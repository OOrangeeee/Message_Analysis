# 最后编辑：
# 晋晨曦 2024.1.20 1:58
# qq：2950171570
# email：Jin0714@outlook.com  回复随缘
import re


def process_data(df):
    """
    处理数据
    :param df:原始数据
    :return:处理好的数据
    """

    # 提取数据
    columns = ["StrTime", "StrContent", "IsSender"]
    df = df[columns].copy()
    df.rename(columns={"StrTime": "time", "StrContent": "data"}, inplace=True)

    # 清洗数据
    df = df.dropna(subset=["data"])
    df_x = df.copy()
    df["data"] = df["data"].astype(str)

    # 分类数据
    is_sender_1 = df["IsSender"] == 1
    is_sender_0 = df["IsSender"] == 0
    j_df = df[is_sender_1].copy()
    n_df = df[is_sender_0].copy()
    j_df = j_df.drop("IsSender", axis=1)
    n_df = n_df.drop("IsSender", axis=1)
    df_x = df_x.drop("IsSender", axis=1)

    df_x = df_x[df_x["data"].apply(not_start_with_msg)]
    df_x["data"] = df_x["data"].apply(remove_bracketed_text_and_count_all)
    df_x = df_x[df_x["data"].apply(len) > 0]

    return j_df, n_df, df_x


def not_start_with_msg(value):
    """
    判断是否不以<开头
    :param value: 文本
    :return: 不以<开头为true，否则flase
    """
    return not value.startswith("<")


def remove_bracketed_text_and_count_all(s):
    """
    删除所有聊天记录[]中文字
    :param s:语句
    :return:删除后的语句
    """
    return re.sub(r"\[.*?\]", "", s)
