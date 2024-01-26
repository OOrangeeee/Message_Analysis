# 最后编辑：
# 晋晨曦 2024.1.26 15.46
# qq：2950171570
# email：Jin0714@outlook.com  回复随缘
import os
import platform


class Show_Tool:
    def __init__(self):
        """
        初始化展示器
        """
        pass

    @property
    def __str__(self):
        """
        返回类介绍
        :return: 类介绍
        """
        return "显示程序中的各种文本"

    def show_front(self):
        print("请输入您想要使用的字体样式")
        print("查看方式为，进入“控制面板\外观和个性化\字体”中，选择您喜欢的字体，右键查看属性，点击详细信息，输入详细信息中的标题即可")
        print("输入0，则采用默认字体")
        print("请输入：", end="")

    def show_chat_file_path(self):
        print("请输入聊天记录路径:", end="")

    def show_input_name(self):
        print("请输入您和您聊天对象的姓名")
        print("请先输入您的姓名再输入聊天对象的姓名")
        print("例如：橙子先生和柠檬女士，请在输入完一个名字后按回车再输入另一个")
        print("请输入：", end="")

    def set_name(self, name1, name2):
        self.name1 = name1
        self.name2 = name2

    def show_heat(self):
        print("现在开始分析聊天热度")

    def show_time(self):
        print("现在开始分析聊天时间分布")

    def show_bqb(self):
        print("现在开始分析表情包")

    def show_emoji(self):
        print("现在开始分析emoji")

    def show_word(self):
        print("现在开始分析词频，并生成词云")

    def show_emo_choice(self):
        print("你是否想分析每一句聊天记录的情感倾向来判断谁在聊天中带来了更多的正能量，谁又经常在聊天中诉苦？！")
        print("如果你想分析那么请输入 1 ，如果不想请输入 2 。")
        print(
            "请注意，此部分需要您自行获得百度智能云中自然语言分析中的情感倾向分析API，这部分请自行百度。(新用户有50万次免费使用，但是QPS只有2，也就是一秒只能分析两句话，速度会很慢)"
        )
        print("请输入：", end="")

    def show_emo(self):
        print("现在开始分析语句情感倾向")

    def show_QPS(self):
        print("请输入您API的QPS值(输入错误可能程序崩溃)：",end='')

    def show_start(self):
        print("现在开始分析聊天记录，请注意：分析的过程中会生成各种各样的图片，切记查看完图片后关闭图片后才能继续运行程序")
        print("不必担心关闭图片会丢失图片，所有的结果都会保存在根目录下 “用户数据” 的文件夹下，图片都在“用户数据/src”文件夹下")
        print("现在让我们开始吧！")
        print("----------------------------------------------")

    def show_end(self, s_time, e_time):
        print("分析完毕，将退出程序。")
        print(f"本次分析所用时间（包括显示图片的时间）：{e_time - s_time}秒")

    def show_choice(self):
        print("请选择分析谁的聊天记录？")
        print("1. " + self.name1 + "  2. " + self.name2 + "  3. 两个人聊天记录" + "  4. 三种都要！(推荐)")
        print("请输入：", end="")

    def clear(self):
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    def show_date(self, df):
        s_date = df.iloc[0]["time"]
        e_date = df.iloc[-1]["time"]
        print(f"将分析从 {s_date} 到 {e_date} 的聊天记录")

        while True:
            ans = input("请输入YES开始分析")
            if ans == "YES":
                break
