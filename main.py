# 最后编辑：
# 晋晨曦 2024.1.27 1:34
# qq：2950171570
# email：Jin0714@outlook.com  回复随缘
import matplotlib
import data_process as dp
import time

import getMsg as r
import solve
import os
import show


def main():
    """
    主函数
    :return: 无
    """

    # 记录时间

    s_time = time.time()

    # 初始化程序
    os.makedirs("用户数据/api", exist_ok=True)
    os.makedirs("用户数据/data", exist_ok=True)
    os.makedirs("用户数据/data/bqb", exist_ok=True)
    os.makedirs("用户数据/data/emoji", exist_ok=True)
    os.makedirs("用户数据/data/src", exist_ok=True)
    os.makedirs("用户数据/data/word", exist_ok=True)
    os.makedirs("用户数据/data/src/emo", exist_ok=True)
    os.makedirs("用户数据/data/src/emoji", exist_ok=True)
    os.makedirs("用户数据/data/src/time", exist_ok=True)
    os.makedirs("用户数据/data/src/word", exist_ok=True)
    os.makedirs("用户数据/data/src/表情包", exist_ok=True)
    os.makedirs("用户数据/data/src/热力图", exist_ok=True)

    # 实例化显示工具

    st = show.Show_Tool()

    # 开始

    st.show_start()

    # 输入字体

    st.show_front()

    front = input()

    front = int(front)

    if front == 0:
        matplotlib.rcParams["font.family"] = str("SimHei")
    else:
        matplotlib.rcParams["font.family"] = str(front)

    st.clear()

    # 读取数据
    st.show_chat_file_path()
    path = input()
    df = r.read_msg(path)  # 聊天记录\柠檬头_x.csv

    st.clear()

    # 读取名称

    st.show_input_name()
    name1 = input()
    name2 = input()
    name1 = str(name1)
    name2 = str(name2)

    st.clear()

    st.set_name(name1, name2)

    # 处理数据
    j_df, n_df, all_df = dp.process_data(df)

    # 输出时间
    st.show_date(all_df)

    # 实例化解决方案
    s = solve.solve(j_df, n_df, all_df, name1, name2)

    # 分析热度
    st.show_heat()
    st.show_choice()

    while True:
        choice = input()
        if choice.isdigit() and 1 <= int(choice) <= 4:
            break
        else:
            print("输入无效，请输入一个数字（1到4之间）。")
    choice = int(choice)

    if choice == 1:
        s.process_heat(name1)
    elif choice == 2:
        s.process_heat(name2)
    elif choice == 3:
        s.process_heat(name1 + name2)
    else:
        s.process_heat(name1)
        s.process_heat(name2)
        s.process_heat(name1 + name2)

    st.clear()

    # 分析时间
    st.show_time()
    st.show_choice()

    while True:
        choice = input()
        if choice.isdigit() and 1 <= int(choice) <= 4:
            break
        else:
            print("输入无效，请输入一个数字（1到4之间）。")
    choice = int(choice)

    if choice == 1:
        s.process_time(name1)
    elif choice == 2:
        s.process_time(name2)
    elif choice == 3:
        s.process_time(name1 + name2)
    else:
        s.process_time(name1)
        s.process_time(name2)
        s.process_time(name1 + name2)

    st.clear()

    # 分析表情包
    st.show_bqb()

    s.process_biaoqingbao()

    st.clear()

    # 分析emoji
    st.show_emoji()

    s.process_emoji()

    st.clear()

    # 分析词语
    st.show_word()

    st.show_choice()

    while True:
        choice = input()
        if choice.isdigit() and 1 <= int(choice) <= 4:
            break
        else:
            print("输入无效，请输入一个数字（1到4之间）。")
    choice = int(choice)

    if choice == 1:
        s.process_words(name1)
    elif choice == 2:
        s.process_words(name2)
    elif choice == 3:
        s.process_words(name1 + name2)
    else:
        s.process_words(name1)
        s.process_words(name2)
        s.process_words(name1 + name2)

    st.clear()

    # 情感分析
    st.show_emo_choice()

    while True:
        choice = input()
        if choice.isdigit() and 1 <= int(choice) <= 2:
            break
        else:
            print("输入无效，请输入一个数字（1到2之间）。")
    choice = int(choice)

    if choice == 1:
        st.show_emo()

        st.show_QPS()

        QPS = input()

        s.set_QPS(QPS)

        st.show_choice()
        while True:
            choice2 = input()
            if choice2.isdigit() and 1 <= int(choice2) <= 4:
                break
            else:
                print("输入无效，请输入一个数字（1到4之间）。")
        choice2 = int(choice2)

        if choice2 == 1:
            s.process_emo(name1)
        elif choice2 == 2:
            s.process_emo(name2)
        elif choice2 == 3:
            s.process_emo(name1 + name2)
        else:
            s.process_emo(name1)
            s.process_emo(name2)
            s.process_emo(name1 + name2)

    st.clear()

    # 保存
    s.save_kinds_of_data()

    # 结束
    e_time = time.time()
    st.show_end(s_time, e_time)

    time.sleep(10)


if __name__ == "__main__":
    main()
