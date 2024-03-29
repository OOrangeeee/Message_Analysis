# 最后编辑：
# 晋晨曦 2024.2.2 17.13
# qq：2950171570
# email：Jin0714@outlook.com  回复随缘
from jieba import cut
from re import findall
from re import sub
from re import search
from collections import defaultdict
import pandas as pd
from aip import AipNlp
from time import sleep

import draw
import save
import calenda as ca


class solve:
    def __init__(self, j_df, n_df, all_df, name1, name2):
        """
        构造函数
        :param j_df: name1聊天记录
        :param n_df: name2聊天记录
        :param all_df: 全部聊天记录
        :param name1: 主分析人
        :param name2: 聊天对象
        """
        self.emoji_j = defaultdict(int)
        self.emoji_l = defaultdict(int)
        self.d = draw.draw_data(name1, name2)
        self.sa = save.save_data()
        self.j_df = j_df
        self.n_df = n_df
        self.all_df = all_df
        self.j_df_clean = pd.DataFrame()
        self.n_df_clean = pd.DataFrame()
        self.all_df_clean = pd.DataFrame()
        self.words = pd.DataFrame()
        self.client = AipNlp("None", "None", "None")
        self.clean_data()
        self.name1 = name1
        self.name2 = name2
        self.shape1 = "fas fa-dog"
        self.shape2 = "fas fa-dog"
        self.shape3 = "fas fa-paw"
        self.s_year, self.s_month, self.e_year, self.e_month = self.find_time(
            self.all_df
        )
        self.months = self.find_month()
        self.months_size = len(self.months)
        pass

    def __str__(self):
        """
        字符串表示，用于打印对象时提供有用的信息。
        """
        return "solve类实例，用于分析数据"
        pass

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
        return sub(r"\[.*?\]", "", s)

    def clean_data(self):
        """
        清洗数据
        :return:无
        """
        self.j_df_clean = self.j_df[
            self.j_df["data"].apply(self.not_start_with_msg_words)
        ].copy()
        self.j_df_clean.loc[:, "data"] = self.j_df_clean["data"].apply(
            self.remove_bracketed_text_and_count_words
        )
        self.j_df_clean = self.j_df_clean[self.j_df_clean["data"].apply(len) > 0]

        self.n_df_clean = self.n_df[
            self.n_df["data"].apply(self.not_start_with_msg_words)
        ].copy()
        self.n_df_clean.loc[:, "data"] = self.n_df_clean["data"].apply(
            self.remove_bracketed_text_and_count_words
        )
        self.n_df_clean = self.n_df_clean[self.n_df_clean["data"].apply(len) > 0]

        self.all_df_clean = self.all_df.copy()

    def find_time(self, df):
        """
        找出时间范围的年月
        :param df: 数据
        :return: 年月
        """
        earliest_time = df.iloc[0]["time"]
        latest_time = df.iloc[-1]["time"]
        earliest_year, earliest_month, _ = earliest_time.split("-")
        latest_year, latest_month, _ = latest_time.split("-")
        return (
            int(earliest_year),
            int(earliest_month),
            int(latest_year),
            int(latest_month),
        )

    def find_month(self):
        """
        找到分析的月份列表
        :return: 月份列表
        """
        months = []

        # 当前的年份和月份
        current_year, current_month = self.s_year, self.s_month

        # 循环直到当前年月等于结束年月
        while (current_year, current_month) <= (self.e_year, self.e_month):
            # 将当前年月添加到列表中
            months.append((current_year, current_month))

            # 如果当前月份是12月，则进入下一年的1月
            if current_month == 12:
                current_year += 1
                current_month = 1
            else:
                # 否则，月份增加1
                current_month += 1

        return months

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
        match = search(r'androidmd5="([^"]*)"', text)
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
        save_path = [
            "./用户数据/data/bqb/" + self.name1 + "_bqb.xlsx",
            "./用户数据/data/bqb/" + self.name2 + "_bqb.xlsx",
        ]
        self.sa.save_data_all(save_data, save_path)

        max_count_j = max(j_df_bqb["count"])
        max_count_n = max(n_df_bqb["count"])
        max_count = max(max_count_j, max_count_n)

        self.d.draw_bqb(j_df_bqb, n_df_bqb, int(max_count + 5))

    # emoji分析

    def remove_bracketed_text_and_count_j(self, s):
        """
        删除所有name1聊天记录[]中文字，统计emoji
        :param s:语句
        :return:删除后的语句
        """
        # 使用正则表达式找到所有被 "[]" 包围的文字
        bracketed_texts = findall(r"\[(.*?)\]", s)

        # 更新统计字典
        for text in bracketed_texts:
            self.emoji_j[text] += 1

        # 删除被 "[]" 包围的文字
        return sub(r"\[.*?\]", "", s)

    def remove_bracketed_text_and_count_l(self, s):
        """
        删除所有name2聊天记录[]中文字，统计emoji
        :param s:语句
        :return:删除后的语句
        """
        # 使用正则表达式找到所有被 "[]" 包围的文字
        bracketed_texts = findall(r"\[(.*?)\]", s)

        # 更新统计字典
        for text in bracketed_texts:
            self.emoji_l[text] += 1

        # 删除被 "[]" 包围的文字
        return sub(r"\[.*?\]", "", s)

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
        save_path = [
            "./用户数据/data/emoji/" + self.name1 + "_emoji.xlsx",
            "./用户数据/data/emoji/" + self.name2 + "_emoji.xlsx",
        ]
        self.sa.save_data_all(save_data, save_path)

        max_count = max(max(emoji_df_j["count"]), max(emoji_df_l["count"]))

        self.d.draw_emoji(emoji_j_sorted, emoji_l_sorted, int(max_count + 5))

    # 词语分析

    def change_shape(self, shape1, shape2, shape3):
        self.shape1 = shape1
        self.shape2 = shape2
        self.shape3 = shape3

    def process_words(self, mode):
        """
        分析语句
        :param mode: 分析模式
        :return: 无
        """

        if mode == self.name1 + self.name2:
            data_words = self.all_df_clean["data"].copy()
            shape = self.shape3
            title = "两个人"
            pass
        elif mode == self.name2:
            data_words = self.n_df_clean["data"].copy()
            shape = self.shape2
            title = mode
            pass
        elif mode == self.name1:
            data_words = self.j_df_clean["data"].copy()
            shape = self.shape1
            title = mode
            pass
        else:
            print("参数错误，退出")
            return
        ans = {}
        for d in data_words:
            words = cut(d, cut_all=False)
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
        # self.words = self.words[self.words["data"].apply(lambda s: s != "主人")]
        self.words.dropna(subset=["data"])
        self.words = self.words[self.words["data"].apply(len) > 1]
        sava_data = [self.words.copy()]
        sava_path = ["./用户数据/data/word/" + title + "_words_counts.xlsx"]
        self.sa.save_data_all(sava_data, sava_path)
        self.d.draw_word_cloud(self.words.copy(), shape, title)

    # 分析热度

    def get_max_count_date(self):
        date_df = self.all_df.copy()
        date_df["time"] = pd.to_datetime(date_df["time"])
        date_df["date"] = date_df["time"].dt.date
        s_date, e_date = ca.get_month_dates(
            self.s_year, self.s_month, self.e_year, self.e_month
        )
        date_range = pd.date_range(start=s_date, end=e_date)
        date_counts = date_df.groupby("date").size().reindex(date_range, fill_value=0)
        date_counts = date_counts.to_frame()
        date_counts = date_counts.reset_index()
        date_counts.columns = ["time", "counts"]
        date_counts["week_day"] = date_counts["time"].apply(lambda s: s.weekday() + 1)
        date_counts.sort_values(by="time")
        date_counts["month"] = date_counts["time"].dt.month
        date_counts["year"] = date_counts["time"].dt.year
        date_dfs = [group for _, group in date_counts.groupby(["year", "month"])]
        max_count = max(date_counts["counts"]) + 50
        self.max_heat_date = max_count

    def make_rili_df(self, date_counts):
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

    def make_masks(
        self,
    ):
        """
        制作遮罩
        :return: 结果
        """
        ans = []
        for year, month in self.months:
            now_rili = ca.generate_calendar(year, month)
            ans.append(now_rili)
        return ans

    def process_heat(self, mode):
        """
        分析聊天热度
        :param mode: 分析模式
        :return: 无
        """
        if mode == self.name1 + self.name2:
            date_df = self.all_df.copy()
            title = "两个人"
            pass
        elif mode == self.name1:
            date_df = self.j_df.copy()
            title = mode
            pass
        elif mode == self.name2:
            date_df = self.n_df.copy()
            title = mode
            pass
        else:
            print("参数错误，退出")
            return
        date_df["time"] = pd.to_datetime(date_df["time"])
        date_df["date"] = date_df["time"].dt.date
        s_date, e_date = ca.get_month_dates(
            self.s_year, self.s_month, self.e_year, self.e_month
        )
        date_range = pd.date_range(start=s_date, end=e_date)
        date_counts = date_df.groupby("date").size().reindex(date_range, fill_value=0)
        date_counts = date_counts.to_frame()
        date_counts = date_counts.reset_index()
        date_counts.columns = ["time", "counts"]
        date_counts["week_day"] = date_counts["time"].apply(lambda s: s.weekday() + 1)

        date_counts.sort_values(by="time")
        date_counts["month"] = date_counts["time"].dt.month
        date_counts["year"] = date_counts["time"].dt.year
        date_dfs = [group for _, group in date_counts.groupby(["year", "month"])]
        rili_dfs = [self.make_rili_df(df) for df in date_dfs]
        mask = self.make_masks()

        date_counts_no_zeros = date_counts[
            date_counts["counts"].apply(lambda s: s != 0)
        ]

        self.d.draw_heat_how(date_counts_no_zeros, title, self.max_heat_date)

        self.d.draw_heatmap_big(
            rili_dfs,
            title,
            mask,
            self.months_size,
            self.months,
            self.max_heat_date,
        )
        self.d.draw_heatmap_all(
            rili_dfs,
            title,
            mask,
            self.months_size,
            self.months,
            self.max_heat_date,
        )

    # 分析聊天时间

    def get_max_count_time(self):
        hour_df = self.all_df.copy()
        hour_df["time"] = pd.to_datetime(hour_df["time"])
        hour_df["hour"] = hour_df["time"].dt.hour
        hour_counts = hour_df.groupby("hour").size().reindex(range(0, 24), fill_value=0)
        hour_counts = hour_counts.to_frame()
        hour_counts = hour_counts.reset_index()
        hour_counts.columns = ["hour", "counts"]
        hour_counts.sort_values(by="hour")
        columns_date_df = [str(i) for i in range(0, 24)]
        hour_df_image = pd.DataFrame(columns=columns_date_df)
        temp_row = [0] * 24
        for index, row in hour_counts.iterrows():
            temp_row[index] = row["counts"]
        hour_df_image = pd.concat(
            [hour_df_image, pd.DataFrame([temp_row], columns=columns_date_df)],
            ignore_index=True,
        )
        max_count = hour_df_image.max(axis=1).values[0]
        self.max_count_time = max_count

    def process_time(self, mode):
        """
        分析聊天热度时间
        :param mode: 分析模式
        :return: 无
        """
        if mode == self.name1 + self.name2:
            hour_df = self.all_df.copy()
            title = "两个人"
            pass
        elif mode == self.name1:
            hour_df = self.j_df.copy()
            title = mode
            pass
        elif mode == self.name2:
            hour_df = self.n_df.copy()
            title = mode
            pass
        else:
            print("参数错误，退出")
            return
        hour_df["time"] = pd.to_datetime(hour_df["time"])
        hour_df["hour"] = hour_df["time"].dt.hour
        hour_counts = hour_df.groupby("hour").size().reindex(range(0, 24), fill_value=0)
        hour_counts = hour_counts.to_frame()
        hour_counts = hour_counts.reset_index()
        hour_counts.columns = ["hour", "counts"]
        hour_counts.sort_values(by="hour")
        columns_date_df = [str(i) for i in range(0, 24)]
        hour_df_image = pd.DataFrame(columns=columns_date_df)
        temp_row = [0] * 24
        for index, row in hour_counts.iterrows():
            temp_row[index] = row["counts"]
        hour_df_image = pd.concat(
            [hour_df_image, pd.DataFrame([temp_row], columns=columns_date_df)],
            ignore_index=True,
        )
        self.d.draw_time_heat(hour_df_image, title, self.max_count_time)

    # 分析情感

    def analyse_word(self, s):
        """
        分析情感
        :param s:
        :return:
        """
        # print("-------")
        # print(s)
        sleep(self.QPS)
        result = self.client.sentimentClassify(s)  # 调用api
        # print("-------")
        return result

    def save_emotion(self, mode):
        """
        生成情感分析文件
        :return: 无
        """
        if mode == self.name1 + self.name2:
            emo_df = self.all_df_clean.copy()
            title = "全部"
            pass
        elif mode == self.name1:
            emo_df = self.j_df_clean.copy()
            title = mode
            pass
        elif mode == self.name2:
            emo_df = self.n_df_clean.copy()
            title = mode
            pass
        else:
            print("参数错误，退出")
            return
        emo_df["emo"] = emo_df["data"].apply(self.analyse_word)
        path = "./用户数据/data/" + title + "情感分析.xlsx"
        emo_df.to_excel(path, index=False)

    def is_items(self, s):
        """
        清洗错误数据
        :param s: 文本
        :return: 是否正确
        """
        return "items" in s

    def get_sentiment(self, s):
        """
        获取倾向
        :param s:结论
        :return: 倾向
        """
        match = search(r"'sentiment': (\d+)", s)
        return int(match.group(1)) if match else None

    def get_api(self, q, a1, a2, a3):
        QPS = int(q)
        if QPS >= 20:
            self.QPS = 0
        else:
            self.QPS = 1.0 / QPS
        self.a1 = a1
        self.a2 = a2
        self.a3 = a3

    def process_emo(self, mode):
        """
        分析情感
        :param mode: 分析模式
        :return: 无
        """
        if mode == self.name1 + self.name2:
            title = "全部"
            pass
        elif mode == self.name1:
            title = self.name1
            pass
        elif mode == self.name2:
            title = self.name2
            pass
        else:
            print("参数错误，退出")
            return
        App_ID = self.a1
        API_KEY = self.a2
        SECRET_KEY = self.a3
        api_path = "./用户数据/api/api.txt"
        text = App_ID + "\n" + API_KEY + "\n" + SECRET_KEY + "\n"
        with open(api_path, "w") as file:
            file.write(text)
        self.client = AipNlp(App_ID, API_KEY, SECRET_KEY)
        print(App_ID)
        print(API_KEY)
        print(SECRET_KEY)
        self.save_emotion(mode)
        path = "./用户数据/data/" + title + "情感分析.xlsx"
        emo_df = pd.read_excel(path)
        emo_df = emo_df[emo_df["emo"].apply(self.is_items)]
        emo_df["emo_rank"] = emo_df["emo"].apply(self.get_sentiment)
        emo_rank_counts = (
            emo_df.groupby("emo_rank").size().reindex(range(0, 3), fill_value=0)
        )
        emo_rank_counts = emo_rank_counts.to_frame()
        emo_rank_counts = emo_rank_counts.reset_index()
        emo_rank_counts.columns = ["rank", "counts"]
        emo_rank_counts.sort_values(by="rank")
        self.d.draw_emo(emo_rank_counts, title)

    # 保存数据
    def save_kinds_of_data(self):
        """
        保存数据
        :return:无
        """
        d_data = [self.n_df.copy(), self.j_df.copy(), self.all_df.copy()]
        d_path = [
            "./用户数据/data/" + self.name2 + ".xlsx",
            "./用户数据/data/" + self.name1 + ".xlsx",
            "./用户数据/data/all.xlsx",
        ]
        self.sa.save_data_all(d_data, d_path)
