# 最后编辑：
# 晋晨曦 2024.1.20 20:43
# qq：2950171570
# email：Jin0714@outlook.com  回复随缘
import matplotlib
import data_process as dp

import getMsg as r
import solve


def main():
    """
    主函数
    :return: 无
    """
    matplotlib.rcParams["font.family"] = "SimHei"  # 例如使用 "SimHei" 字体

    # 读取数据
    path = input()
    df = r.read_msg(path)  # 聊天记录\柠檬头.csv

    # 处理数据
    j_df, n_df, all_df = dp.process_data(df)

    # 实例化解决方案
    s = solve.solve(j_df, n_df, all_df)

    # 分析热度
    s.process_heat("全部记录")
    s.process_heat("晋晨曦")
    s.process_heat("宁静")

    # 分析时间
    s.process_time("全部记录")
    s.process_time("晋晨曦")
    s.process_time("宁静")

    # 分析表情包
    s.process_biaoqingbao()

    # 分析emoji
    s.process_emoji()

    # 分析词语
    s.process_words("全部文字")
    s.process_words("晋晨曦")
    s.process_words("宁静")

    # 情感分析
    s.process_emo("全部记录")
    s.process_emo("晋晨曦")
    s.process_emo("宁静")

    # 保存
    s.save_kinds_of_data()


if __name__ == "__main__":
    main()
