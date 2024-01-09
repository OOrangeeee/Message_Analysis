import getMsg as r
import matplotlib
import data_process as dp
import draw


def main():
    matplotlib.rcParams["font.family"] = "SimHei"  # 例如使用 "SimHei" 字体
    # path = input()
    path = "E:\python\WeChatMsg\聊天记录\柠檬头.csv"
    df = r.read_msg(path)
    l_df, emoji_j, emoji_l = dp.process_data(df)
    draw.solve_emoji(emoji_j, emoji_l)


if __name__ == "__main__":
    main()
