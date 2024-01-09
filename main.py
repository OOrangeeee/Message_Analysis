import getMsg as r
import matplotlib
import data_process as dp
import draw


def main():
    matplotlib.rcParams["font.family"] = "SimHei"  # 例如使用 "SimHei" 字体
    # path = input()
    path = "E:\python\Message_Analysis\聊天记录\柠檬头.csv"
    df = r.read_msg(path)
    j_df, l_df, emoji_j, emoji_l, j_df_bqb, l_df_bqb = dp.process_data(df)
    draw.draw_emoji(emoji_j, emoji_l)
    draw.draw_bqb(j_df_bqb, l_df_bqb)


if __name__ == "__main__":
    main()
