import matplotlib.pyplot as plt


def split_dict(original_dict, size=21):
    keys = list(original_dict.keys())
    split_dicts = []

    for i in range(0, len(keys), size):
        # 提取键的子集
        subset_keys = keys[i : i + size]
        # 使用字典推导式创建新的字典，包含子集键值对
        new_dict = {key: original_dict[key] for key in subset_keys}
        split_dicts.append(new_dict)

    return split_dicts


def solve_emoji(dict1, dict2):
    j = split_dict(dict1)
    l = split_dict(dict2)
    for x in range(4):
        draw_emoji(j[x], l[x], x)


def draw_emoji(dict1, dict2, num):
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
