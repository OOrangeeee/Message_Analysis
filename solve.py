import jieba as jb
import re
from collections import defaultdict
import pandas as pd
import numpy as np

import draw
import save


class solve:
    def __init__(self, j_df, n_df, all_df):
        """
        构造函数
        :param j_df: 晋晨曦数据
        :param n_df: 宁静数据
        """
        self.emoji_j = defaultdict(int)
        self.emoji_l = defaultdict(int)
        self.d = draw.draw_data()
        self.sa = save.save_data()
        self.j_df = j_df
        self.n_df = n_df
        self.all_df = all_df
        self.words = pd.DataFrame()
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

    def process_biaoqingbao(self):
        """
        分析表情包
        :return: 处理后的数据和结果
        """
        # 分离表情包
        j_df_bqb = self.j_df[self.j_df["data"].apply(self.start_with_msg)]
        n_df_bqb = self.n_df[self.n_df["data"].apply(self.start_with_msg)]
        self.j_df = self.j_df[self.j_df["data"].apply(self.not_start_with_msg)]
        self.n_df = self.n_df[self.n_df["data"].apply(self.not_start_with_msg)]

        # 处理数据
        j_df_bqb = j_df_bqb.copy()
        j_df_bqb["data"] = j_df_bqb["data"].apply(self.extract_androidmd5)

        n_df_bqb = n_df_bqb.copy()
        n_df_bqb["data"] = n_df_bqb["data"].apply(self.extract_androidmd5)

        # 统计表情包
        value_counts = j_df_bqb["data"].value_counts()
        j_df_bqb = value_counts.reset_index()
        j_df_bqb.columns = ["data", "count"]
        value_counts = n_df_bqb["data"].value_counts()
        n_df_bqb = value_counts.reset_index()
        n_df_bqb.columns = ["data", "count"]

        j_df_bqb = j_df_bqb.sort_values(by="count", ascending=False)
        n_df_bqb = n_df_bqb.sort_values(by="count", ascending=False)

        save_data = [j_df_bqb, n_df_bqb]
        save_path = ["data/bqb/bqb_j.xlsx", "data/bqb/bqb_l.xlsx"]
        self.sa.save_data_all(save_data, save_path)

        self.d.draw_bqb(j_df_bqb, n_df_bqb)

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

    def process_emoji(self):
        """
        统计两个人的emoji使用情况
        :return: 返回处理好的聊天记录和得到的分析数据
        """
        # 统计和删除emoji
        self.j_df.loc[:, "data"] = self.j_df["data"].apply(
            self.remove_bracketed_text_and_count_j
        )
        self.n_df.loc[:, "data"] = self.n_df["data"].apply(
            self.remove_bracketed_text_and_count_l
        )

        # 清洗数据
        self.j_df = self.j_df[self.j_df["data"].apply(len) > 0]
        self.n_df = self.n_df[self.n_df["data"].apply(len) > 0]

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

    # 词语分析

    def not_start_with_msg_words(self, value):
        """
        判断是否不以<开头
        :param value: 文本
        :return: 不以<开头为true，否则flase
        """
        return not value.startswith("<")

    def remove_bracketed_text_and_count_words(self, s):
        """
        删除所有聊天记录[]中文字
        :param s:语句
        :return:删除后的语句
        """
        return re.sub(r"\[.*?\]", "", s)

    def process_words(self, mode):
        """
        分析语句
        :param mode: 分析模式
        :return: 无
        """
        self.j_df = self.j_df[self.j_df["data"].apply(self.not_start_with_msg_words)]
        self.j_df.loc[:, "data"] = self.j_df["data"].apply(
            self.remove_bracketed_text_and_count_words
        )
        self.j_df = self.j_df[self.j_df["data"].apply(len) > 0]

        self.n_df = self.n_df[self.n_df["data"].apply(self.not_start_with_msg_words)]
        self.n_df.loc[:, "data"] = self.n_df["data"].apply(
            self.remove_bracketed_text_and_count_words
        )
        self.n_df = self.n_df[self.n_df["data"].apply(len) > 0]

        if mode == "全部文字":
            data_words = self.all_df["data"]
            shape = "fas fa-dog"
            pass
        elif mode == "宁静":
            data_words = self.n_df["data"]
            shape = "far fa-lemon"
            pass
        elif mode == "晋晨曦":
            data_words = self.j_df["data"]
            shape = "fas fa-paw"
            pass
        else:
            print("参数错误，退出")
            return
        ans = {}
        for d in data_words:
            words = jb.cut(d, cut_all=False)
            for w in words:
                if w in ans and len(w) > 1:
                    ans[w] += 1
                elif len(w) > 1:
                    ans[w] = 1
        sorted_ans = sorted(ans.items(), key=lambda x: x[1], reverse=True)
        ans.clear()
        for data in sorted_ans:
            ans[data[0]] = data[1]
        self.words = pd.DataFrame(list(ans.items()), columns=["data", "counts"])
        self.words = self.words[self.words["data"].apply(lambda s: s != "主人")]
        self.words.dropna(subset=["data"])
        self.words = self.words[self.words["data"].apply(len) > 1]
        sava_data = [self.words.copy()]
        sava_path = ["data/word/words_counts.xlsx"]
        self.sa.save_data_all(sava_data, sava_path)
        self.d.draw_word_cloud(self.words.copy(), shape, mode)

    # 分析热度

    def make_date_df(self, date_counts):
        """
        生成日历df
        :param date_counts: 每天的count
        :return: 结果
        """
        days = ["0", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        columns_date_df = [days[i] for i in range(1, 8)]
        df_new = pd.DataFrame(columns=columns_date_df)
        temp_row = [0] * 7
        is_has = False
        for _, row_old in date_counts.iterrows():
            time = row_old["week_day"] - 1  # 将时间1-7转换为索引0-6
            count = row_old["counts"]
            temp_row[time] = count
            is_has = True
            if time == 6:  # 如果填充到了星期日，添加行到df_new
                df_new = pd.concat(
                    [df_new, pd.DataFrame([temp_row], columns=columns_date_df)],
                    ignore_index=True,
                )
                temp_row = [0] * 7
                is_has = False
        # 处理最后一行
        if is_has:  # 如果最后一行不是全0
            df_new = pd.concat(
                [df_new, pd.DataFrame([temp_row], columns=columns_date_df)],
                ignore_index=True,
            )
        # 输出新的DataFrame
        return df_new

    def make_masks(self, data):
        """
        制作遮罩
        :return: 结果
        """
        ans = []
        array = np.zeros_like(data[0].to_numpy(), dtype=bool)
        array[0, :6] = True
        array[5, 2:] = True
        ans.append(array)
        array = np.zeros_like(data[1].to_numpy(), dtype=bool)
        array[0, :2] = True
        array[4, 4:] = True
        ans.append(array)
        array = np.zeros_like(data[2].to_numpy(), dtype=bool)
        array[0, :4] = True
        ans.append(array)
        array = np.zeros_like(data[3].to_numpy(), dtype=bool)
        array[4, 3:] = True
        ans.append(array)
        return ans

    def process_heat(self, mode):
        """
        分析聊天热度
        :param mode: 分析模式
        :return: 无
        """
        if mode == "全部记录":
            date_df = self.all_df.copy()
            pass
        elif mode == "晋晨曦":
            date_df = self.j_df.copy()
            pass
        elif mode == "宁静":
            date_df = self.n_df.copy()
            pass
        else:
            print("参数错误，退出")
            return
        date_df["time"] = pd.to_datetime(date_df["time"])
        date_df["date"] = date_df["time"].dt.date

        date_range = pd.date_range(start="2023-10-01", end="2024-1-31")
        date_counts = date_df.groupby("date").size().reindex(date_range, fill_value=0)
        date_counts = date_counts.to_frame()
        date_counts = date_counts.reset_index()
        date_counts.columns = ["time", "counts"]
        date_counts["week_day"] = date_counts["time"].apply(lambda s: s.weekday() + 1)

        date_counts.sort_values(by="time")
        date_counts["month"] = date_counts["time"].dt.month
        date_counts["year"] = date_counts["time"].dt.year
        date_dfs = [group for _, group in date_counts.groupby(["year", "month"])]
        rili_dfs = [self.make_date_df(df) for df in date_dfs]
        # for df in rili_dfs:
        #     print(df)
        # print(date_counts)
        # print(date_counts)
        mask = self.make_masks(rili_dfs)
        self.d.draw_heatmap_big(
            rili_dfs,
            mode,
            mask,
        )
        self.d.draw_heatmap_all(
            rili_dfs,
            mode,
            mask,
        )

    # 保存数据
    def save_kinds_of_data(self):
        """
        保存数据
        :return:无
        """
        d_data = [self.n_df.copy(), self.j_df.copy(), self.all_df.copy()]
        d_path = ["data/柠檬.xlsx", "data/橙子.xlsx", "data/all.xlsx"]
        self.sa.save_data_all(d_data, d_path)
