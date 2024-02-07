# 最后编辑：
# 晋晨曦 2024.1.20 20:28
# qq：2950171570
# email：Jin0714@outlook.com  回复随缘
from pandas import read_csv


def read_msg(path):
    """
    读取数据
    :param path: 数据位置
    :return: df
    """
    lemon = read_csv(path)
    return lemon
