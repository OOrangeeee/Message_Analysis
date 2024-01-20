# 最后编辑：
# 晋晨曦 2024.1.20 20:28
# qq：2950171570
# email：Jin0714@outlook.com  回复随缘
import matplotlib.pyplot as plt
import pandas as pd
import stylecloud as sc
import os
import seaborn as sns
import calendar
from PIL import Image


class draw_data:
    def __init__(self):
        """
        构造函数，初始化一些可能需要的属性。
        """
        pass

    def __str__(self):
        """
        字符串表示，用于打印对象时提供有用的信息。
        """
        return "draw_data类实例，用于可视化数据"
        pass

    # 绘制emoji

    def split_dict(self, original_dict, size=21):
        """
        划分字典
        :param original_dict:初始字典
        :param size:划分数量
        :return:无
        """
        keys = list(original_dict.keys())
        split_dicts = []

        for i in range(0, len(keys), size):
            # 提取键的子集
            subset_keys = keys[i : i + size]
            # 使用字典推导式创建新的字典，包含子集键值对
            new_dict = {key: original_dict[key] for key in subset_keys}
            split_dicts.append(new_dict)

        return split_dicts

    def draw_emoji(self, dict1, dict2):
        """
        批量画emoji图的驱动函数
        :param dict1:晋晨曦emoji字典
        :param dict2:宁静emoji字典
        :return:无
        """
        j = self.split_dict(dict1)
        n = self.split_dict(dict2)
        for x in range(4):
            self.draw_emoji_tool(j[x], n[x], x)

    def draw_emoji_tool(self, dict1, dict2, num):
        """
        画emoji图的工作函数
        :param dict1:晋晨曦emoji字典
        :param dict2:宁静emoji字典
        :param num:第几个图
        :return:无
        """
        # 提取键和值

        keys = list(dict1.keys())
        values1 = list(dict1.values())
        values2 = list(dict2.values())

        plt.figure(figsize=(10, 6))

        # 设置柱状图的位置
        x = range(len(keys))
        width = 0.35  # 柱状图的宽度

        plt.ylim(0, 500)
        # 绘制柱状图
        plt.bar(
            [i - width / 2 for i in x],
            values1,
            width=width,
            label="橙子先生",
            color="orange",
            edgecolor="black",
        )
        plt.bar(
            [i + width / 2 for i in x],
            values2,
            width=width,
            label="柠檬女士",
            color="yellow",
            edgecolor="black",
        )

        # 添加图例、标签和标题
        title = "emoji统计！num " + str(num + 1) + " !"
        plt.xlabel("emoji类型")
        plt.ylabel("频率")
        plt.title(title)
        plt.xticks(x, keys)
        plt.legend()

        filepath = "./用户数据/data/src/emoji/" + title + ".png"
        plt.savefig(filepath, format="png")

        # 显示图表
        plt.tight_layout()
        plt.show()

    # 绘制表情包

    def union_bqb(self, j_df, n_df):
        """
        扩写df
        :param j_df: 晋晨曦df
        :param n_df: 宁静df
        :return: 返回结果
        """
        data_union = pd.Series(list(set(j_df["data"]).union(set(n_df["data"]))))

        df1_extended = data_union.to_frame(name="data").merge(
            j_df, on="data", how="left"
        )
        df2_extended = data_union.to_frame(name="data").merge(
            n_df, on="data", how="left"
        )

        df1_extended["count"].fillna(0, inplace=True)
        df2_extended["count"].fillna(0, inplace=True)

        df1_extended.sort_values(by="data", inplace=True)
        df2_extended.sort_values(by="data", inplace=True)
        return df1_extended, df2_extended

    def split_dataframe(self, df, n_parts):
        """
        划分表情包
        :param df:划分对象
        :param n_parts:划分几部分
        :return:划分后的df列表
        """
        # 确定每个部分的大小
        part_size = len(df) // n_parts

        # 创建包含分割后的DataFrames的列表
        split_dfs = [df[i * part_size : (i + 1) * part_size] for i in range(n_parts)]

        return split_dfs

    def draw_bqb(self, bqb_j, bqb_n):
        """
        画表情包的图
        :param bqb_j: 晋晨曦表情包df
        :param bqb_n: 宁静表情包df
        :return: 无
        """
        # 画种类
        self.draw_bqb_kinds(bqb_j, bqb_n)
        # 画数量
        self.draw_bqb_count(bqb_j, bqb_n)
        # 细分画
        bqb_j, bqb_n = self.union_bqb(bqb_j, bqb_n)
        dfs_j = self.split_dataframe(bqb_j, 6)
        dfs_l = self.split_dataframe(bqb_n, 6)
        for i in range(6):
            self.draw_bqb_details(dfs_j[i], dfs_l[i], i)

    def draw_bqb_kinds(self, df1, df2):
        """
        画图表情包种类
        :param df1:晋晨曦df
        :param df2:宁静df
        :return:无
        """
        # 计算每个df的data列的唯一值数量
        unique_count_df1 = df1["data"].nunique()
        unique_count_df2 = df2["data"].nunique()

        # 数据准备用于绘图
        labels = ["橙子先生", "柠檬女士"]
        counts = [unique_count_df1, unique_count_df2]

        plt.figure(figsize=(10, 6))

        # 绘制柱状图
        plt.bar(labels, counts, color=["orange", "yellow"], edgecolor="black")

        # 添加标题和标签
        title = "表情包种数统计!"
        plt.title(title)
        plt.xlabel("水果！")
        plt.ylabel("用的表情包种数")
        filepath = "./用户数据/data/src/表情包/" + title + ".png"
        plt.savefig(filepath, format="png")

        # 显示图表
        plt.show()

    def draw_bqb_count(self, df1, df2):
        """
        表情包数目
        :param df1:晋晨曦数目
        :param df2:宁静数目
        :return:
        """
        # 计算每个df的count列的总和
        total_count_df1 = df1["count"].sum()
        total_count_df2 = df2["count"].sum()

        # 数据准备用于绘图
        labels = ["橙子先生", "柠檬女士"]
        counts = [total_count_df1, total_count_df2]

        plt.figure(figsize=(10, 6))

        # 绘制柱状图
        plt.bar(labels, counts, color=["orange", "yellow"], edgecolor="black")

        # 添加标题和标签
        title = "表情包数量统计!"
        plt.title(title)
        plt.xlabel("水果！")
        plt.ylabel("用的表情包数量")
        filepath = "./用户数据/data/src/表情包/" + title + ".png"
        plt.savefig(filepath, format="png")
        # 显示图表
        plt.show()

    def draw_bqb_details(self, df1, df2, num):
        """
        画表情包图
        :param df1: 晋晨曦df子集
        :param df2: 宁静df子集
        :param num: 第几个
        :return: 无
        """
        index_data = list(df1["data"])

        counts_df1 = {
            data: df1[df1["data"] == data]["count"].sum() for data in index_data
        }
        counts_df2 = {
            data: df2[df2["data"] == data]["count"].sum() for data in index_data
        }

        # 从1开始编号
        x_labels = range(1, len(index_data) + 1)

        # 数据准备用于绘图
        counts1 = [counts_df1.get(data, 0) for data in index_data]
        counts2 = [counts_df2.get(data, 0) for data in index_data]

        plt.figure(figsize=(20, 6))

        # 绘制柱状图
        plt.bar(
            [x + 0.05 for x in x_labels],
            counts1,
            color="orange",
            width=0.3,
            label="橙子先生",
            edgecolor="black",
        )
        plt.bar(
            [x + 0.35 for x in x_labels],
            counts2,
            color="yellow",
            width=0.3,
            label="柠檬女士",
            edgecolor="black",
        )

        # 添加标题和标签
        title = "不同表情包使用频率 num " + str(num + 1) + " !"
        plt.title(title)
        plt.xlabel("表情包编号")
        plt.ylabel("频率")

        # 将x轴的标签从数字转换为字符串
        plt.xticks([x + 0.2 for x in x_labels], [str(x) for x in x_labels])

        plt.legend()

        filepath = "./用户数据/data/src/表情包/" + title + ".png"
        plt.savefig(filepath, format="png")

        # 显示图表
        plt.show()

    # 绘制词云

    def draw_word_cloud(self, df, shape, mode):
        """
        画词云
        :param df: 数据
        :param shape: 形状
        :param mode: 模式
        :return: 无
        """
        df_using = df.head(200)
        path = "temp.csv"
        df_using.to_csv(path, index=False)
        output_path = "./用户数据/data/src/word/" + mode + "词云.png"
        sc.gen_stylecloud(
            file_path=path,
            size=1920,
            icon_name=shape,
            palette="colorbrewer.diverging.Spectral_11",
            background_color="black",
            max_words=200,
            max_font_size=120,
            font_path="仓耳与墨 W03.TTF",
            output_name=output_path,
        )
        if os.path.exists(path):
            os.remove(path)
        else:
            print("完蛋")
        img = Image.open(output_path)
        plt.figure(figsize=(15, 15))
        plt.imshow(img)
        plt.axis("off")  # 不显示坐标轴
        plt.show()

    # 绘制热力图和变化趋势

    def draw_heatmap_all(self, rili_dfs, title, masks):
        """
        统调子图函数
        :param rili_dfs: 日历df
        :param title: 标题
        :param masks: 遮罩
        :return: 无
        """
        for i in range(1, 5):
            self.draw_heatmap_small(rili_dfs[i - 1], title, masks[i - 1], i)
            pass

    def draw_heatmap_small(self, rili_df, title, mask, num):
        """
        画热力子图
        :param rili_df: 子图数据
        :param title: 标题
        :param mask: 遮罩
        :param num: 编号
        :return: 无
        """
        if title == "晋晨曦":
            title = "橙子"
        elif title == "宁静":
            title = "柠檬"
        elif title == "全部记录":
            title = "两个人"
        if num < 4:
            time = num + 9
            year = "2023 "
        else:
            time = 1
            year = "2024 "
        plt.figure(figsize=(5, 5))
        plt.title(title + "的聊天热力图 " + year + str(time) + "月 版!!")
        data = rili_df
        data = data.fillna(0)
        data = data.astype(int)
        sns.heatmap(
            data=data,
            mask=mask,
            vmax=1050,
            vmin=0,
            cmap="YlOrRd",
            linewidths=0.5,
            linecolor="white",
            cbar=True,
            cbar_kws={"label": "信息条数"},
        )
        counter = 1  # 初始化计数器
        for y in range(data.shape[0]):
            for x in range(data.shape[1]):
                if not mask[y, x]:  # 如果格子未被遮罩
                    plt.text(
                        x + 0.5,
                        y + 0.5,
                        str(counter),
                        ha="center",
                        va="center",
                        color="black",
                    )
                    counter += 1
        plt.yticks([])
        plt.tight_layout()
        filepath = (
            "./用户数据/data/src/热力图/" + title + "的聊天热力图 " + year + str(time) + "月 版!!.png"
        )
        plt.savefig(filepath, format="png")
        plt.show()
        pass

    def draw_heatmap_big(self, rili_dfs, title, masks):
        """
        绘制聊天热度图
        :param date_range: 日期范围
        :param date_counts: 每天的条数
        :return: 无
        """
        fig, axes = plt.subplots(2, 2, figsize=(10, 10))
        if title == "晋晨曦":
            title = "橙子"
        elif title == "宁静":
            title = "柠檬"
        elif title == "全部记录":
            title = "两个人"
        fig.suptitle(title + " 的聊天热力图总览！！")

        for i, month in enumerate(range(10, 14)):
            row = i // 2
            col = i % 2
            ax = axes[row, col]
            data = rili_dfs[i]
            data = data.fillna(0)
            data = data.astype(int)
            sns.heatmap(
                data=data,
                mask=masks[i],
                vmax=1050,
                vmin=0,
                cmap="YlOrRd",
                linewidths=0.5,
                linecolor="white",
                ax=ax,
                cbar=True,
                cbar_kws={"label": "信息条数"},
            )
            counter = 1
            for y in range(data.shape[0]):
                for x in range(data.shape[1]):
                    if not masks[i][y, x]:  # 如果格子未被遮罩
                        ax.text(
                            x + 0.5,
                            y + 0.5,
                            str(counter),
                            ha="center",
                            va="center",
                            color="black",
                        )
                        counter += 1
            ax.set_title(
                f"2023 {calendar.month_name[month if month<13 else month-12]}"
                if month != 13
                else f"2024 {calendar.month_name[month if month<13 else month-12]}"
            )
            ax.set_yticklabels([])
            ax.set_aspect("equal")
        plt.tight_layout()
        filepath = "./用户数据/data/src/热力图/" + title + "聊天热力图.png"
        plt.savefig(filepath, format="png")
        plt.show()

    def draw_heat_how(self, df, title):
        """
        热度变化趋势
        :param df: 数据
        :param title: 标题
        :return: 无
        """
        if title == "晋晨曦":
            title = "橙子"
        elif title == "宁静":
            title = "柠檬"
        elif title == "全部记录":
            title = "两个人"
        plt.figure(figsize=(15, 6))
        plt.ylim(0, 1050)
        plt.plot(df.index, df["counts"], marker="o")

        plt.title(title + "聊天热度变化趋势")
        plt.xlabel("时间")
        plt.ylabel("热度")

        # plt.grid(True)
        filepath = "./用户数据/data/src/热力图/" + title + "聊天热度变化趋势.png"
        plt.savefig(filepath, format="png")
        plt.show()

    def draw_time_heat(self, time_df, title):
        """
        画时间热力图
        :param time_df: 图数据
        :param title: 标题
        :return: 无
        """
        if title == "晋晨曦":
            title = "橙子"
        elif title == "宁静":
            title = "柠檬"
        elif title == "全部记录":
            title = "两个人"
        plt.figure(figsize=(10, 3))
        plt.title(title + "的聊天时间分布热力图!!")
        data = time_df
        data = data.fillna(0)
        data = data.astype(int)
        sns.heatmap(
            data=data,
            vmax=1600,
            vmin=0,
            cmap="YlOrRd",
            linewidths=0.5,
            linecolor="white",
            cbar=True,
            cbar_kws={"label": "信息条数", "orientation": "horizontal"},
        )
        # counter = 0  # 初始化计数器
        # for y in range(data.shape[0]):
        #     for x in range(data.shape[1]):
        #         plt.text(
        #             x + 0.5,
        #             y + 0.5,
        #             str(counter),
        #             ha="center",
        #             va="center",
        #             color="black",
        #         )
        #         counter += 1
        plt.yticks([])
        plt.tight_layout()
        filepath = "./用户数据/data/src/time/" + title + "的聊天时间分布热力图!!.png"
        plt.savefig(filepath, format="png")
        plt.show()

    # 情绪分析

    def draw_emo(self, df, mode):
        """
        绘制饼图
        :param df: 数据
        :param mode: 模式
        :return: 无
        """
        df["percentage"] = df["counts"] / df["counts"].sum() * 100
        colors = {0: "#CFE3C8", 1: "#FFD686", 2: "#E59069"}
        fig, ax = plt.subplots(figsize=(10, 10))
        wedges, texts, autotexts = ax.pie(
            df["percentage"],
            startangle=140,
            autopct="%1.1f%%",
            colors=[colors[rank] for rank in df["rank"]],
        )

        legend_labels = ["负面", "中立", "正面"]
        ax.legend(
            wedges,
            legend_labels,
            title="情绪的颜色对应",
            loc="center left",
            bbox_to_anchor=(0, 0),
        )

        plt.title(mode + "情绪占比")
        plt.axis("equal")
        filepath = "./用户数据/data/src/emo/" + mode + "的情绪分析图!!.png"
        plt.savefig(filepath, format="png")
        plt.show()
