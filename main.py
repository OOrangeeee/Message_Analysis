# 最后编辑：
# 晋晨曦 2024.2.2 17.13
# qq：2950171570
# email：Jin0714@outlook.com  回复随缘
from matplotlib import rcParams
from os import makedirs
from show_gui import ShowGui


def main():
    """
    主函数
    :return: 无
    """

    # 初始化程序
    makedirs("用户数据/api", exist_ok=True)
    makedirs("用户数据/data", exist_ok=True)
    makedirs("用户数据/data/bqb", exist_ok=True)
    makedirs("用户数据/data/emoji", exist_ok=True)
    makedirs("用户数据/data/src", exist_ok=True)
    makedirs("用户数据/data/word", exist_ok=True)
    makedirs("用户数据/data/src/emo", exist_ok=True)
    makedirs("用户数据/data/src/emoji", exist_ok=True)
    makedirs("用户数据/data/src/time", exist_ok=True)
    makedirs("用户数据/data/src/word", exist_ok=True)
    makedirs("用户数据/data/src/表情包", exist_ok=True)
    makedirs("用户数据/data/src/热力图", exist_ok=True)

    rcParams["font.family"] = str("SimHei")

    sh = ShowGui()

    sh.show()


if __name__ == "__main__":
    main()
