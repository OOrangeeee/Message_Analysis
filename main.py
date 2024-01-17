import getMsg as r
import matplotlib
import data_process as dp
import solve
import save


def main():
    """
    主函数
    :return: 无
    """
    matplotlib.rcParams["font.family"] = "SimHei"  # 例如使用 "SimHei" 字体

    # 实例化解决方案
    s = solve.solve()

    # 实例化可视化工具
    sa = save.save_data()

    # 读取数据
    # path = input()
    path = "E:\python\Message_Analysis\聊天记录\柠檬头.csv"
    df = r.read_msg(path)

    # 处理数据
    j_df, l_df, all_df = dp.process_data(df)

    # 分析表情包
    j_df, l_df = s.process_biaoqingbao(j_df, l_df)

    # 分析emoji
    j_df, l_df = s.process_emoji(j_df, l_df)

    d_data = [l_df, j_df, all_df]
    d_path = ["data/柠檬.xlsx", "data/橙子.xlsx", "data/all.xlsx"]
    sa.save_data_all(d_data, d_path)


if __name__ == "__main__":
    main()
