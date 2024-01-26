# 最后编辑：
# 晋晨曦 2024.1.26 15.46
# qq：2950171570
# email：Jin0714@outlook.com  回复随缘
import matplotlib.pyplot as plt
import pandas as pd
import stylecloud as sc
import os
import seaborn as sns
import calendar
from PIL import Image
import math


class draw_data:
    def __init__(self, name1, name2):
        """
        构造函数，初始化一些可能需要的属性。
        """
        self.name1 = name1
        self.name2 = name2
        pass

    def __str__(self):
        """
        字符串表示，用于打印对象时提供有用的信息。
        """
        return "draw_data类实例，用于可视化数据"
        pass

    # 绘制emoji

    def split_dict(self, original_dict, size):
        """
        划分字典
        :param original_dict: 初始字典
        :param size: 划分数量
        :return: 一个列表，包含划分后的字典
        """
        keys = list(original_dict.keys())
        split_dicts = []

        for i in range(0, len(keys), size):
            subset_keys = keys[i : i + size]
            new_dict = {key: original_dict[key] for key in subset_keys}
            split_dicts.append(new_dict)

        return split_dicts

    def draw_emoji(self, dict1, dict2, max_count):
        """
        批量画emoji图的驱动函数
        :param dict1:name1emoji字典
        :param dict2:name2emoji字典
        :return:无
        """
        length = len(dict1)
        num_20 = length // 20
        if length % 20 != 0:
            num_20 += 1
        j = self.split_dict(dict1, 20)
        n = self.split_dict(dict2, 20)
        for x in range(num_20):
            self.draw_emoji_tool(j[x], n[x], x, max_count)

    def draw_emoji_tool(self, dict1, dict2, num, max_count):
        """
        画emoji图的工作函数
        :param dict1:name1emoji字典
        :param dict2:name2emoji字典
        :param num:第几个图
        :return:无
        """
        # 提取键和值

        keys = list(dict1.keys())
        values1 = list(dict1.values())
        values2 = list(dict2.values())

        plt.figure(figsize=(10, 6))

        x = range(len(keys))
        width = 0.35

        plt.ylim(0, max_count)
        plt.bar(
            [i - width / 2 for i in x],
            values1,
            width=width,
            label=self.name1,
            color="orange",
            edgecolor="black",
        )
        plt.bar(
            [i + width / 2 for i in x],
            values2,
            width=width,
            label=self.name2,
            color="yellow",
            edgecolor="black",
        )

        title = "emoji统计！num " + str(num + 1) + " !"
        plt.xlabel("emoji类型")
        plt.ylabel("频率")
        plt.title(title)
        plt.xticks(x, keys)
        plt.legend()

        filepath = "./用户数据/data/src/emoji/" + title + ".png"
        plt.savefig(filepath, format="png")

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
        part_size = len(df) // n_parts

        split_dfs = [df[i * part_size : (i + 1) * part_size] for i in range(n_parts)]

        return split_dfs

    def draw_bqb(self, bqb_j, bqb_n, max_count):
        """
        画表情包的图
        :param bqb_j: name1表情包df
        :param bqb_n: name2表情包df
        :return: 无
        """
        # 画种类
        self.draw_bqb_kinds(bqb_j, bqb_n)
        # 画数量
        self.draw_bqb_count(bqb_j, bqb_n, max_count)
        # 细分画
        bqb_j, bqb_n = self.union_bqb(bqb_j, bqb_n)
        count = len(bqb_n) // 28
        if len(bqb_n) % 28 != 0:
            count += 1
        dfs_j = self.split_dataframe(bqb_j, count)
        dfs_l = self.split_dataframe(bqb_n, count)
        for i in range(count):
            self.draw_bqb_details(dfs_j[i], dfs_l[i], i, max_count)

    def draw_bqb_kinds(self, df1, df2):
        """
        画图表情包种类
        :param df1:name1df
        :param df2:name2df
        :return:无
        """
        unique_count_df1 = df1["data"].nunique()
        unique_count_df2 = df2["data"].nunique()

        labels = [self.name1, self.name2]
        counts = [unique_count_df1, unique_count_df2]

        plt.figure(figsize=(10, 6))

        plt.bar(labels, counts, color=["orange", "yellow"], edgecolor="black")

        title = "表情包种数统计!"
        plt.title(title)
        plt.xlabel("对象")
        plt.ylabel("用的表情包种数")
        filepath = "./用户数据/data/src/表情包/" + title + ".png"
        plt.savefig(filepath, format="png")

        plt.show()

    def draw_bqb_count(self, df1, df2, max_count):
        """
        表情包数目
        :param df1:name1数目
        :param df2:name2数目
        :return:
        """
        total_count_df1 = df1["count"].sum()
        total_count_df2 = df2["count"].sum()

        labels = [self.name1, self.name2]
        counts = [total_count_df1, total_count_df2]

        plt.figure(figsize=(10, 6))

        plt.bar(labels, counts, color=["orange", "yellow"], edgecolor="black")

        title = "表情包数量统计!"
        plt.title(title)
        plt.xlabel("对象")
        plt.ylabel("用的表情包数量")
        filepath = "./用户数据/data/src/表情包/" + title + ".png"
        plt.savefig(filepath, format="png")
        plt.show()

    def draw_bqb_details(self, df1, df2, num, max_count):
        """
        画表情包图
        :param df1: name1df子集
        :param df2: name2df子集
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

        x_labels = range(1, len(index_data) + 1)

        counts1 = [counts_df1.get(data, 0) for data in index_data]
        counts2 = [counts_df2.get(data, 0) for data in index_data]

        plt.figure(figsize=(20, 6))

        plt.ylim(0, max_count)

        plt.bar(
            [x + 0.05 for x in x_labels],
            counts1,
            color="orange",
            width=0.3,
            label=self.name1,
            edgecolor="black",
        )
        plt.bar(
            [x + 0.35 for x in x_labels],
            counts2,
            color="yellow",
            width=0.3,
            label=self.name2,
            edgecolor="black",
        )

        title = "不同表情包使用频率 num " + str(num + 1) + " !"
        plt.title(title)
        plt.xlabel("表情包编号")
        plt.ylabel("频率")

        plt.xticks([x + 0.2 for x in x_labels], [str(x) for x in x_labels])

        plt.legend()

        filepath = "./用户数据/data/src/表情包/" + title + ".png"
        plt.savefig(filepath, format="png")

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
        if len(df) >= 200:
            df_using = df.head(200)
        else:
            df_using = df
        path = "temp.csv"
        df_using.to_csv(path, index=False)
        output_path = "./用户数据/data/src/word/" + mode + "词云.png"
        sc.gen_stylecloud(
            file_path=path,
            size=1920,
            icon_name=shape,
            palette="colorbrewer.diverging.Spectral_11",
            background_color="black",
            max_words=len(df_using),
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

    def draw_heatmap_all(self, rili_dfs, title, masks, length, months, max_count):
        """
        统调子图函数
        :param rili_dfs: 日历df
        :param title: 标题
        :param masks: 遮罩
        :return: 无
        """
        for i in range(0, length):
            self.draw_heatmap_small(
                rili_dfs[i - 1], title, masks[i - 1], months[i], max_count
            )
            pass

    def draw_heatmap_small(self, rili_df, title, mask, month, max_count):
        """
        画小图像
        :param rili_df:日历
        :param title:标题
        :param mask:遮罩
        :param month:月份
        :return:
        """
        year = month[0]
        time = month[1]
        plt.figure(figsize=(5, 5))
        plt.title(title + "的聊天热力图 " + str(year) + " " + str(time) + "月 版!!")
        data = rili_df
        data = data.fillna(0)
        data = data.astype(int)
        sns.heatmap(
            data=data,
            mask=mask,
            vmax=max_count,
            vmin=0,
            cmap="YlOrRd",
            linewidths=0.5,
            linecolor="white",
            cbar=True,
            cbar_kws={"label": "信息条数"},
        )
        counter = 1
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
            "./用户数据/data/src/热力图/"
            + title
            + "的聊天热力图 "
            + str(year)
            + str(time)
            + "月 版!!.png"
        )
        plt.savefig(filepath, format="png")
        plt.show()
        pass

    def draw_heatmap_big(self, rili_dfs, title, masks, length, months, max_count):
        """
        画热力图总览
        :param rili_dfs: 日历
        :param title: 标题
        :param masks: 遮罩
        :param length: 数量
        :param months: 月份
        :param max_count: 最大计数
        """
        rows = math.ceil(length / 4)
        cols = 4
        fig, axes = plt.subplots(rows, cols, figsize=(10, 5 * rows))

        if rows == 1 or cols == 1:
            axes = axes.reshape(rows, cols)

        for i in range(rows * cols):
            row = i // cols
            col = i % cols
            ax = axes[row, col]

            # 如果 i 小于 length，则绘制子图，否则隐藏该子图
            if i < length:
                data = rili_dfs[i]
                data = data.fillna(0)
                data = data.astype(int)
                sns.heatmap(
                    data=data,
                    mask=masks[i],
                    vmax=max_count,
                    vmin=0,
                    cmap="YlOrRd",
                    linewidths=0.5,
                    linecolor="white",
                    ax=ax,
                    cbar=False,
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
                ax.set_title(f"{months[i][0]} 年 {months[i][1]} 月")
                ax.set_yticklabels([])
                ax.set_aspect("equal")
            else:
                ax.axis('off')

        fig.text(0.5, 0.01, title + " 的聊天热力图总览！！", ha="center", fontsize=15)
        cbar_ax = fig.add_axes([0.2, 0.90, 0.6, 0.07])
        norm = plt.Normalize(vmin=0, vmax=max_count)
        sm = plt.cm.ScalarMappable(cmap="YlOrRd", norm=norm)
        fig.colorbar(sm, cax=cbar_ax, orientation="horizontal", label="信息条数")
        plt.subplots_adjust(bottom=0.1)
        filepath = "./用户数据/data/src/热力图/" + title + "聊天热力图总览.png"
        plt.savefig(filepath, format="png")
        plt.show()

    def draw_heat_how(self, df, title, max_count):
        """
        热度变化趋势
        :param df: 数据
        :param title: 标题
        :return: 无
        """
        plt.figure(figsize=(15, 6))
        plt.ylim(0, max_count)
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
