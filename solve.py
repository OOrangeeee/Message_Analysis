import draw
import re
from collections import defaultdict
import pandas as pd
import save


class solve:
    def __init__(self):
        """
        构造函数，初始化一些可能需要的属性。
        """
        self.emoji_j = defaultdict(int)
        self.emoji_l = defaultdict(int)
        self.d = draw.draw_data()
        self.sa = save.save_data()
        pass

    def __str__(self):
        """
        字符串表示，用于打印对象时提供有用的信息。
        """
        return "solve类实例，用于分析数据"
        pass

    # 表情包分析

    def not_start_with_msg(self, value):
        """
        判断是否不以<开头
        :param value: 文本
        :return: 不以<开头为true，否则flase
        """
        return not value.startswith("<")

    def start_with_msg(self, value):
        """
        判断是否以<开头
        :param value: 文本
        :return: 不以<开头为true，否则flase
        """
        return value.startswith("<")

    def extract_androidmd5(self, text):
        """
        提取图片文件的androidmd5码用于分析图片种类
        :param text:图片文件
        :return:提取结果
        """
        match = re.search(r'androidmd5="([^"]*)"', text)
        return match.group(1) if match else None

    def process_biaoqingbao(self, j_df, l_df):
        """
        分析表情包
        :param j_df: 晋晨曦数据
        :param l_df: 宁静数据
        :return: 处理后的数据和结果
        """
        # 分离表情包
        j_df_bqb = j_df[j_df["data"].apply(self.start_with_msg)]
        l_df_bqb = l_df[l_df["data"].apply(self.start_with_msg)]
        j_df = j_df[j_df["data"].apply(self.not_start_with_msg)]
        l_df = l_df[l_df["data"].apply(self.not_start_with_msg)]

        # 处理数据
        j_df_bqb = j_df_bqb.copy()
        j_df_bqb["data"] = j_df_bqb["data"].apply(self.extract_androidmd5)

        l_df_bqb = l_df_bqb.copy()
        l_df_bqb["data"] = l_df_bqb["data"].apply(self.extract_androidmd5)

        # 统计表情包
        value_counts = j_df_bqb["data"].value_counts()
        j_df_bqb = value_counts.reset_index()
        j_df_bqb.columns = ["data", "count"]
        value_counts = l_df_bqb["data"].value_counts()
        l_df_bqb = value_counts.reset_index()
        l_df_bqb.columns = ["data", "count"]

        j_df_bqb = j_df_bqb.sort_values(by="count", ascending=False)
        l_df_bqb = l_df_bqb.sort_values(by="count", ascending=False)

        save_data = [j_df_bqb, l_df_bqb]
        save_path = ["data/bqb/bqb_j.xlsx", "data/bqb/bqb_l.xlsx"]
        self.sa.save_data_all(save_data, save_path)

        self.d.draw_bqb(j_df_bqb, l_df_bqb)
        return j_df, l_df

    # emoji分析

    def remove_bracketed_text_and_count_j(self, s):
        """
        删除所有晋晨曦聊天记录[]中文字，统计emoji
        :param s:语句
        :return:删除后的语句
        """
        # 使用正则表达式找到所有被 "[]" 包围的文字
        bracketed_texts = re.findall(r"\[(.*?)\]", s)

        # 更新统计字典
        for text in bracketed_texts:
            self.emoji_j[text] += 1

        # 删除被 "[]" 包围的文字
        return re.sub(r"\[.*?\]", "", s)

    def remove_bracketed_text_and_count_l(self, s):
        """
        删除所有宁静聊天记录[]中文字，统计emoji
        :param s:语句
        :return:删除后的语句
        """
        # 使用正则表达式找到所有被 "[]" 包围的文字
        bracketed_texts = re.findall(r"\[(.*?)\]", s)

        # 更新统计字典
        for text in bracketed_texts:
            self.emoji_l[text] += 1

        # 删除被 "[]" 包围的文字
        return re.sub(r"\[.*?\]", "", s)

    def sort_dicts(self, dict1, dict2):
        """
        将量字典归为并集，并排序
        :param dict1: 字典一
        :param dict2: 字典二
        :return:每个字典的全集并排序
        """
        # 合并两个字典的键并去重
        all_keys = set(dict1.keys()) | set(dict2.keys())
        # 对键进行排序
        sorted_keys = sorted(all_keys)
        # 创建两个新字典，按排序后的键存放键对
        sorted_dict1 = {key: dict1.get(key, None) for key in sorted_keys}
        sorted_dict2 = {key: dict2.get(key, None) for key in sorted_keys}

        return sorted_dict1, sorted_dict2

    def process_emoji(self, j_df, l_df):
        """
        统计两个人的emoji使用情况
        :param j_df: 晋晨曦的聊天记录
        :param l_df: 宁静的聊天记录
        :return: 返回处理好的聊天记录和得到的分析数据
        """
        # 统计和删除emoji
        j_df["data"] = j_df["data"].apply(self.remove_bracketed_text_and_count_j)
        l_df["data"] = l_df["data"].apply(self.remove_bracketed_text_and_count_l)

        # 清洗数据
        j_df = j_df[j_df["data"].apply(len) > 0]
        l_df = l_df[l_df["data"].apply(len) > 0]

        # 合并两个字典的键并去重
        all_keys = set(self.emoji_j.keys()).union(set(self.emoji_l.keys()))
        for key in all_keys:
            self.emoji_j.setdefault(key, 0)
            self.emoji_l.setdefault(key, 0)

        # 转化为df
        emoji_df_j = pd.DataFrame(list(self.emoji_j.items()), columns=["data", "count"])
        emoji_df_l = pd.DataFrame(list(self.emoji_l.items()), columns=["data", "count"])

        # 排序
        emoji_df_j = emoji_df_j.sort_values(by="count", ascending=False)
        emoji_df_l = emoji_df_l.sort_values(by="count", ascending=False)

        # 按照一个顺序排列
        emoji_j_sorted, emoji_l_sorted = self.sort_dicts(self.emoji_j, self.emoji_l)

        # 保存
        save_data = [emoji_df_j, emoji_df_l]
        save_path = ["data/emoji/emoji_j.xlsx", "data/emoji/emoji_l.xlsx"]
        self.sa.save_data_all(save_data, save_path)

        self.d.draw_emoji(emoji_j_sorted, emoji_l_sorted)
        return j_df, l_df

    # 词语分析
