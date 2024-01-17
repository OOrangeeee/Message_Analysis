import matplotlib.pyplot as plt
import pandas as pd


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

    def split_dict(self, original_dict, size=21):
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
        j = self.split_dict(dict1)
        l = self.split_dict(dict2)
        for x in range(4):
            self.draw_emoji_x(j[x], l[x], x)

    def draw_emoji_x(self, dict1, dict2, num):
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

        filepath = "./data/src/" + title + ".png"
        plt.savefig(filepath, format="png")

        # 显示图表
        plt.tight_layout()
        plt.show()

    def split_dataframe(self, df, n_parts):
        # 确定每个部分的大小
        part_size = len(df) // n_parts

        # 创建包含分割后的DataFrames的列表
        split_dfs = [df[i * part_size : (i + 1) * part_size] for i in range(n_parts)]

        return split_dfs

    def draw_bqb(self, bqb_j, bqb_l):
        self.draw_bqb_kinds(bqb_j, bqb_l)
        self.plot_total_count(bqb_j, bqb_l)
        dfs_j = self.split_dataframe(bqb_j, 4)
        dfs_l = self.split_dataframe(bqb_l, 4)
        for i in range(4):
            self.plot_combined_data(dfs_j[i], dfs_l[i], i)

    def draw_bqb_kinds(self, df1, df2):
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
        filepath = "./data/src/" + title + ".png"
        plt.savefig(filepath, format="png")

        # 显示图表
        plt.show()

    def plot_total_count(self, df1, df2):
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
        filepath = "./data/src/" + title + ".png"
        plt.savefig(filepath, format="png")
        # 显示图表
        plt.show()

    def plot_combined_data(self, df1, df2, num):
        # 合并两个df的data列并去重，创建一个并集
        combined_data = pd.concat([df1["data"], df2["data"]]).unique()

        # 创建一个字典，用于存储每个data值在两个df中的count总和
        counts_df1 = {
            data: df1[df1["data"] == data]["count"].sum() for data in combined_data
        }
        counts_df2 = {
            data: df2[df2["data"] == data]["count"].sum() for data in combined_data
        }

        # 从1开始编号
        x_labels = range(1, len(combined_data) + 1)

        # 数据准备用于绘图
        counts1 = [counts_df1.get(data, 0) for data in combined_data]
        counts2 = [counts_df2.get(data, 0) for data in combined_data]

        plt.figure(figsize=(20, 6))

        # 绘制柱状图
        plt.bar(
            x_labels,
            counts1,
            color="orange",
            width=0.4,
            label="橙子先生",
            edgecolor="black",
        )
        plt.bar(
            [x + 0.4 for x in x_labels],
            counts2,
            color="yellow",
            width=0.4,
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

        filepath = "./data/src/" + title + ".png"
        plt.savefig(filepath, format="png")

        # 显示图表
        plt.show()
