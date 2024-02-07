import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import PhotoImage
from ctypes import windll
from functools import partial
import getMsg as r
import solve
import data_process as dp
from webbrowser import open_new_tab


class ShowGui:
    def __init__(self):
        try:
            windll.shcore.SetProcessDpiAwareness(1)
        except (AttributeError, ValueError):
            pass
        self.root = tk.Tk()
        self.root.title("橙子作品之聊天记录分析")
        self.root.geometry("1600x1200")
        self.root.iconbitmap('./icon/icon.ico')
        self.shape1 = "fas fa-dog"
        self.shape2 = "far fa-lemon"
        self.shape3 = "fas fa-paw"
        self.init_pages_start()
        pass

    def show(self):
        self.page_start.pack(fill="both", expand=True)
        self.root.mainloop()

    def init_pages_start(self):
        self.page_start = tk.Frame(self.root)
        self.center_frame_start = tk.Frame(self.page_start)
        self.center_frame_start.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        self.logo = PhotoImage(file="./logo/logo.png")
        self.logo2 = PhotoImage(file="./logo/logo2.png")
        tk.Label(self.center_frame_start, image=self.logo).pack()
        tk.Label(self.root, image=self.logo2).pack(side="top", anchor="nw")

        tk.Button(
            self.center_frame_start,
            text="启动程序",
            command=self.show_page_choice_path,
            font=("SimHei", 16),
        ).pack()

    def init_pages_choice_path(self):
        self.page_choice_path = tk.Frame(self.root)
        self.center_frame_choice_path = tk.Frame(self.page_choice_path)
        self.center_frame_choice_path.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        tk.Button(
            self.center_frame_choice_path,
            text="选择聊天记录",
            command=self.load_date,
            font=("SimHei", 16),
        ).pack()

    def init_pages_load_name(self):
        self.page_load_name = tk.Frame(self.root)
        self.center_frame_load_name = tk.Frame(self.page_load_name)
        self.center_frame_load_name.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        tk.Label(
            self.center_frame_load_name,
            text="请输入两个分析对象的名字",
            font=("SimHei", 16),
        ).pack(pady=(0, 20))
        tk.Label(
            self.center_frame_load_name,
            text="分析对象1的名字(你的名字，如：橙子先生)：",
            font=("SimHei", 16),
        ).pack()
        name_entry_one = tk.Entry(self.center_frame_load_name)
        name_entry_one.pack(pady=5)
        tk.Label(
            self.center_frame_load_name,
            text="分析对象2的名字(对方的名字，如：柠檬女士)：",
            font=("SimHei", 16),
        ).pack()
        name_entry_two = tk.Entry(self.center_frame_load_name)
        name_entry_two.pack(pady=5)
        tk.Button(
            self.center_frame_load_name,
            text="确认",
            command=partial(self.save_name, name_entry_one, name_entry_two),
            font=("SimHei", 16),
        ).pack(pady=10)

    def initpages_process_data(self):
        self.page_process_data = tk.Frame(self.root)
        self.center_frame_process_data = tk.Frame(self.page_process_data)
        self.center_frame_process_data.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        tk.Label(
            self.center_frame_process_data,
            text=f"将分析从 {self.s_date} 到 {self.e_date} 的聊天记录",
            font=("SimHei", 16),
        ).pack(pady=(0, 20))
        tk.Button(
            self.center_frame_process_data,
            text="开始分析",
            command=self.Go,
            font=("SimHei", 16),
        ).pack()

    def initpages_process_heat(self):
        self.s.get_max_count_date()
        self.page_process_heat = tk.Frame(self.root)
        self.center_frame_process_heat = tk.Frame(self.page_process_heat)
        self.center_frame_process_heat.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        tk.Label(
            self.center_frame_process_heat,
            text="聊天热度分析\n现在开始分析聊天热度\n请选择分析谁的聊天记录？",
            font=("SimHei", 16),
        ).pack(pady=(0, 20))
        tk.Label(
            self.center_frame_process_heat,
            text="-----------------------",
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Button(
            self.center_frame_process_heat,
            text=self.name1,
            command=partial(self.process_heat, 1),
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Label(
            self.center_frame_process_heat,
            text="-----------------------",
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Button(
            self.center_frame_process_heat,
            text=self.name2,
            command=partial(self.process_heat, 2),
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Label(
            self.center_frame_process_heat,
            text="-----------------------",
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Button(
            self.center_frame_process_heat,
            text=self.name1 + "和" + self.name2,
            command=partial(self.process_heat, 3),
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Label(
            self.center_frame_process_heat,
            text="-----------------------",
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Button(
            self.center_frame_process_heat,
            text="我全都要！（推荐）",
            command=partial(self.process_heat, 4),
            font=("SimHei", 16),
        ).pack()
        tk.Label(
            self.center_frame_process_heat,
            text="-----------------------",
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Button(
            self.center_frame_process_heat,
            text="跳过",
            command=partial(self.process_heat, 5),
            font=("SimHei", 16),
        ).pack()

    def initpages_process_time(self):
        self.s.get_max_count_time()
        self.page_process_time = tk.Frame(self.root)
        self.center_frame_process_time = tk.Frame(self.page_process_time)
        self.center_frame_process_time.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        tk.Label(
            self.center_frame_process_time,
            text="聊天时间分析\n现在开始分析聊天时间分布\n请选择分析谁的聊天记录？",
            font=("SimHei", 16),
        ).pack(pady=(0, 20))
        tk.Label(
            self.center_frame_process_time,
            text="-----------------------",
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Button(
            self.center_frame_process_time,
            text=self.name1,
            command=partial(self.process_time, 1),
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Label(
            self.center_frame_process_time,
            text="-----------------------",
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Button(
            self.center_frame_process_time,
            text=self.name2,
            command=partial(self.process_time, 2),
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Label(
            self.center_frame_process_time,
            text="-----------------------",
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Button(
            self.center_frame_process_time,
            text=self.name1 + "和" + self.name2,
            command=partial(self.process_time, 3),
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Label(
            self.center_frame_process_time,
            text="-----------------------",
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Button(
            self.center_frame_process_time,
            text="我全都要！（推荐）",
            command=partial(self.process_time, 4),
            font=("SimHei", 16),
        ).pack()
        tk.Label(
            self.center_frame_process_time,
            text="-----------------------",
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Button(
            self.center_frame_process_time,
            text="跳过",
            command=partial(self.process_time, 5),
            font=("SimHei", 16),
        ).pack()

    def initpages_process_biaoqingbao(self):
        self.page_process_bqb = tk.Frame(self.root)
        self.center_frame_process_bqb = tk.Frame(self.page_process_bqb)
        self.center_frame_process_bqb.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        tk.Label(
            self.center_frame_process_bqb,
            text="现在开始分析表情包",
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Button(
            self.center_frame_process_bqb,
            text="开始分析表情包",
            command=partial(self.process_bqb, 1),
            font=("SimHei", 16),
        ).pack()
        tk.Label(
            self.center_frame_process_bqb,
            text="-----------------------",
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Button(
            self.center_frame_process_bqb,
            text="跳过",
            command=partial(self.process_bqb, 0),
            font=("SimHei", 16),
        ).pack()

    def initpages_process_emoji(self):
        self.page_process_emoji = tk.Frame(self.root)
        self.center_frame_process_emoji = tk.Frame(self.page_process_emoji)
        self.center_frame_process_emoji.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        tk.Label(
            self.center_frame_process_emoji,
            text="现在开始分析emoji",
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Button(
            self.center_frame_process_emoji,
            text="开始分析emoji",
            command=partial(self.process_emoji, 1),
            font=("SimHei", 16),
        ).pack()
        tk.Label(
            self.center_frame_process_emoji,
            text="-----------------------",
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Button(
            self.center_frame_process_emoji,
            text="跳过",
            command=partial(self.process_emoji, 0),
            font=("SimHei", 16),
        ).pack()

    def initpages_process_word_all(self):
        self.page_process_word_all = tk.Frame(self.root)
        self.center_frame_process_word_all = tk.Frame(self.page_process_word_all)
        self.center_frame_process_word_all.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        tk.Label(
            self.center_frame_process_word_all,
            text="现在开始分析词频",
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Button(
            self.center_frame_process_word_all,
            text="自定义词云形状",
            command=partial(self.process_word_all, 1),
            font=("SimHei", 16),
        ).pack()
        tk.Label(
            self.center_frame_process_word_all,
            text="-----------------------",
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Button(
            self.center_frame_process_word_all,
            text="使用默认词云形状",
            command=partial(self.process_word_all, 2),
            font=("SimHei", 16),
        ).pack()
        tk.Label(
            self.center_frame_process_word_all,
            text="-----------------------",
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Button(
            self.center_frame_process_word_all,
            text="跳过",
            command=partial(self.process_word_all, 0),
            font=("SimHei", 16),
        ).pack()

    def initpages_process_word_1(self):
        self.page_process_word_1 = tk.Frame(self.root)
        self.center_frame_process_word_1 = tk.Frame(self.page_process_word_1)
        self.center_frame_process_word_1.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        tk.Label(
            self.center_frame_process_word_1,
            text="进入下面的网站，点击“查看图标”，找到喜欢的形状，点击右上角的复制，然后粘贴到下面的输入栏即可\n如果还是不明白，就去查看使用教程中的词云形状自定义教程",
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        link_label = tk.Label(
            self.center_frame_process_word_1,
            text="点击打开网站，选取词云形状",
            fg="blue",
            cursor="hand2",
            font=("SimHei", 16),
        )
        link_label.pack()
        link_label.bind(
            "<Button-1>", lambda e: self.open_link("https://fa5.dashgame.com/#/")
        )
        tk.Label(
            self.center_frame_process_word_1,
            text="请输入三个形状编码",
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Label(
            self.center_frame_process_word_1,
            text=f"{self.name1}的词云形状：",
            font=("SimHei", 16),
        ).pack()
        shape_entry1 = tk.Entry(self.center_frame_process_word_1)
        shape_entry1.pack(pady=5)
        tk.Label(
            self.center_frame_process_word_1,
            text=f"{self.name2}的词云形状：",
            font=("SimHei", 16),
        ).pack()
        shape_entry2 = tk.Entry(self.center_frame_process_word_1)
        shape_entry2.pack(pady=5)
        tk.Label(
            self.center_frame_process_word_1,
            text="全部聊天记录的词云形状：",
            font=("SimHei", 16),
        ).pack()
        shape_entry3 = tk.Entry(self.center_frame_process_word_1)
        shape_entry3.pack(pady=5)
        tk.Button(
            self.center_frame_process_word_1,
            text="确认",
            command=partial(self.save_shape, shape_entry1, shape_entry2, shape_entry3),
            font=("SimHei", 16),
        ).pack(pady=10)
        tk.Label(
            self.center_frame_process_word_1,
            text="请注意一定要输入正确的词云代码，例如：far fa-lemon，如果输入错误会导致程序出现未知错误",
            font=("SimHei", 16),
        ).pack()

    def initpages_process_word_2(self):
        self.s.change_shape(self.shape1, self.shape2, self.shape3)
        self.page_process_word_2 = tk.Frame(self.root)
        self.center_frame_process_word_2 = tk.Frame(self.page_process_word_2)
        self.center_frame_process_word_2.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        tk.Label(
            self.center_frame_process_word_2,
            text="词频分析\n现在开始分析词频并生成词云\n请选择分析谁的聊天记录？",
            font=("SimHei", 16),
        ).pack(pady=(0, 20))
        tk.Label(
            self.center_frame_process_word_2,
            text="-----------------------",
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Button(
            self.center_frame_process_word_2,
            text=self.name1,
            command=partial(self.process_word, 1),
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Label(
            self.center_frame_process_word_2,
            text="-----------------------",
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Button(
            self.center_frame_process_word_2,
            text=self.name2,
            command=partial(self.process_word, 2),
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Label(
            self.center_frame_process_word_2,
            text="-----------------------",
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Button(
            self.center_frame_process_word_2,
            text=self.name1 + "和" + self.name2,
            command=partial(self.process_word, 3),
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Label(
            self.center_frame_process_word_2,
            text="-----------------------",
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Button(
            self.center_frame_process_word_2,
            text="我全都要！（推荐）",
            command=partial(self.process_word, 4),
            font=("SimHei", 16),
        ).pack()

    def initpages_process_emo_all(self):
        self.page_process_emo_all = tk.Frame(self.root)
        self.center_frame_process_emo_all = tk.Frame(self.page_process_emo_all)
        self.center_frame_process_emo_all.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        tk.Label(
            self.center_frame_process_emo_all,
            text="你是否想分析每一句聊天记录的情感倾向来判断谁在聊天中带来了更多的正能量，谁又经常在聊天中诉苦？！\n请注意，此部分需要您自行获得百度智能云中自然语言分析中的情感倾向分析API，这部分请自行百度。\n新用户有50万次免费使用，但是QPS只有2，也就是一秒只能分析两句话，速度会很慢。\n请注意本部分需要联网",
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Button(
            self.center_frame_process_emo_all,
            text="想！",
            command=partial(self.process_emo, 1),
            font=("SimHei", 16),
        ).pack()
        tk.Label(
            self.center_frame_process_emo_all,
            text="-----------------------",
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Button(
            self.center_frame_process_emo_all,
            text="不想",
            command=partial(self.process_emo, 0),
            font=("SimHei", 16),
        ).pack()
        tk.Label(
            self.center_frame_process_emo_all,
            text="请注意：如果你要进行情感分析，请一定确保自己的api次数足够，或者自己的账户余额足够，否则当次数用完会前功尽弃",
            font=("SimHei", 16),
        ).pack(pady=(0, 10))

    def initpages_process_emo_1(self):
        self.page_process_emo_1 = tk.Frame(self.root)
        self.center_frame_process_emo_1 = tk.Frame(self.page_process_emo_1)
        self.center_frame_process_emo_1.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        tk.Label(
            self.center_frame_process_emo_1,
            text="请输入您API的QPS",
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        qps_entry = tk.Entry(self.center_frame_process_emo_1)
        qps_entry.pack(pady=5)
        tk.Label(
            self.center_frame_process_emo_1,
            text="请输入App_ID",
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        api_entry1 = tk.Entry(self.center_frame_process_emo_1)
        api_entry1.pack(pady=5)
        tk.Label(
            self.center_frame_process_emo_1,
            text="请输入API_KEY",
            font=("SimHei", 16),
        ).pack()
        api_entry2 = tk.Entry(self.center_frame_process_emo_1)
        api_entry2.pack(pady=5)
        tk.Label(
            self.center_frame_process_emo_1,
            text="请输入SECRET_KEY",
            font=("SimHei", 16),
        ).pack()
        api_entry3 = tk.Entry(self.center_frame_process_emo_1)
        api_entry3.pack(pady=5)
        tk.Button(
            self.center_frame_process_emo_1,
            text="确定",
            command=partial(
                self.save_api, qps_entry, api_entry1, api_entry2, api_entry3
            ),
            font=("SimHei", 16),
        ).pack(pady=10)
        tk.Label(
            self.center_frame_process_emo_1,
            text="请注意一定要输入正确的api，如果输入错误会导致程序出现未知错误",
            font=("SimHei", 16),
        ).pack()

    def initpages_process_emo_2(self):
        self.page_process_emo_2 = tk.Frame(self.root)
        self.center_frame_process_emo_2 = tk.Frame(self.page_process_emo_2)
        self.center_frame_process_emo_2.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        tk.Label(
            self.center_frame_process_emo_2,
            text="情感分析\n现在开始分析情感\n请选择分析谁的聊天记录？",
            font=("SimHei", 16),
        ).pack(pady=(0, 20))
        tk.Label(
            self.center_frame_process_emo_2,
            text="-----------------------",
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Button(
            self.center_frame_process_emo_2,
            text=self.name1,
            command=partial(self.process_emo_do, 1),
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Label(
            self.center_frame_process_emo_2,
            text="-----------------------",
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Button(
            self.center_frame_process_emo_2,
            text=self.name2,
            command=partial(self.process_emo_do, 2),
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Label(
            self.center_frame_process_emo_2,
            text="-----------------------",
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Button(
            self.center_frame_process_emo_2,
            text=self.name1 + "和" + self.name2,
            command=partial(self.process_emo_do, 3),
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Label(
            self.center_frame_process_emo_2,
            text="-----------------------",
            font=("SimHei", 16),
        ).pack(pady=(0, 10))
        tk.Button(
            self.center_frame_process_emo_2,
            text="我全都要！（推荐）",
            command=partial(self.process_emo_do, 4),
            font=("SimHei", 16),
        ).pack()

    def initpages_process_end(self):
        self.page_process_end = tk.Frame(self.root)
        self.center_frame_process_end = tk.Frame(self.page_process_end)
        self.center_frame_process_end.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        tk.Label(
            self.center_frame_process_end,
            text="恭喜！分析完成！可以退出啦！\n本软件由橙子先生一人独立开发，免费分享给大家使用！\n如果大家想的话，可以给橙子先生或者柠檬女士点个关注，这会让我们有成就感\n并且我预计会在未来不定期分享一些自己写的好玩的程序，谢谢大家。",
            font=("SimHei", 16),
        ).pack()
        link_label_1 = tk.Label(
            self.center_frame_process_end,
            text="点击打开橙子先生小红书主页",
            fg="blue",
            cursor="hand2",
            font=("SimHei", 16),
        )
        link_label_1.pack()
        link_label_1.bind(
            "<Button-1>",
            lambda e: self.open_link(
                "https://www.xiaohongshu.com/user/profile/60f2fd48000000000100aaff"
            ),
        )
        link_label_2 = tk.Label(
            self.center_frame_process_end,
            text="点击打开橙子先生bilibili主页",
            fg="blue",
            cursor="hand2",
            font=("SimHei", 16),
        )
        link_label_2.pack()
        link_label_2.bind(
            "<Button-1>",
            lambda e: self.open_link(
                "https://space.bilibili.com/316695110?spm_id_from=333.999.0.0"
            ),
        )
        link_label_3 = tk.Label(
            self.center_frame_process_end,
            text="点击打开柠檬女士小红书主页",
            fg="blue",
            cursor="hand2",
            font=("SimHei", 16),
        )
        link_label_3.pack()
        link_label_3.bind(
            "<Button-1>",
            lambda e: self.open_link(
                "https://www.xiaohongshu.com/user/profile/5a79c3c64eacab6e6f5400c1?channelType=web_engagement_notification_page&channelTabId=mentions"
            ),
        )
        tk.Label(
            self.center_frame_process_end,
            text="PS：结果都保存在 用户数据/data 文件夹中，无论是导出的表格还是图片都在里面\n图片在 用户数据/data/src 文件夹里\n祝大家生活愉快!",
            font=("SimHei", 14),
        ).pack()

    def show_page_choice_path(self):
        self.init_pages_choice_path()
        self.page_start.pack_forget()
        self.page_choice_path.pack(fill="both", expand=True)

    def show_page_load_name(self):
        self.init_pages_load_name()
        self.page_choice_path.pack_forget()
        self.page_load_name.pack(fill="both", expand=True)

    def show_page_process_data(self):
        self.initpages_process_data()
        self.page_load_name.pack_forget()
        self.page_process_data.pack(fill="both", expand=True)

    def show_page_process_heat(self):
        self.initpages_process_heat()
        self.page_process_data.pack_forget()
        self.page_process_heat.pack(fill="both", expand=True)

    def show_page_process_time(self):
        self.initpages_process_time()
        self.page_process_heat.pack_forget()
        self.page_process_time.pack(fill="both", expand=True)

    def show_page_process_bqb(self):
        self.initpages_process_biaoqingbao()
        self.page_process_time.pack_forget()
        self.page_process_bqb.pack(fill="both", expand=True)

    def show_page_process_emoji(self):
        self.initpages_process_emoji()
        self.page_process_bqb.pack_forget()
        self.page_process_emoji.pack(fill="both", expand=True)

    def show_page_process_word_all(self):
        self.initpages_process_word_all()
        self.page_process_emoji.pack_forget()
        self.page_process_word_all.pack(fill="both", expand=True)

    def show_page_process_word_1(self):
        self.initpages_process_word_1()
        self.page_process_word_all.pack_forget()
        self.page_process_word_1.pack(fill="both", expand=True)

    def show_page_process_word_2_from1(self):
        self.initpages_process_word_2()
        self.page_process_word_1.pack_forget()
        self.page_process_word_2.pack(fill="both", expand=True)

    def show_page_process_word_2_fromall(self):
        self.initpages_process_word_2()
        self.page_process_word_all.pack_forget()
        self.page_process_word_2.pack(fill="both", expand=True)

    def show_page_process_emo_all(self):
        self.initpages_process_emo_all()
        self.page_process_word_2.pack_forget()
        self.page_process_emo_all.pack(fill="both", expand=True)

    def show_page_process_emo_all_from_all(self):
        self.initpages_process_emo_all()
        self.page_process_word_all.pack_forget()
        self.page_process_emo_all.pack(fill="both", expand=True)

    def show_page_process_emo_1(self):
        self.initpages_process_emo_1()
        self.page_process_emo_all.pack_forget()
        self.page_process_emo_1.pack(fill="both", expand=True)

    def show_page_process_emo_2(self):
        self.initpages_process_emo_2()
        self.page_process_emo_1.pack_forget()
        self.page_process_emo_2.pack(fill="both", expand=True)

    def show_page_end_emo_all(self):
        self.initpages_process_end()
        self.page_process_emo_all.pack_forget()
        self.page_process_end.pack(fill="both", expand=True)

    def show_page_end_emo_2(self):
        self.initpages_process_end()
        self.page_process_emo_2.pack_forget()
        self.page_process_end.pack(fill="both", expand=True)

    def open_link(self, url):
        open_new_tab(url)

    def save_name(self, name_entry1, name_entry2):
        self.name1 = name_entry1.get()
        self.name2 = name_entry2.get()
        self.process_data()
        self.show_page_process_data()

    def save_shape(self, shape_entry1, shape_entry2, shape_entry3):
        self.shape1 = shape_entry1.get()
        self.shape2 = shape_entry2.get()
        self.shape3 = shape_entry3.get()
        self.show_page_process_word_2_from1()

    def save_api(self, qps_entry, api_entry1, api_entry2, api_entry3):
        self.api1 = api_entry1.get()
        self.api2 = api_entry2.get()
        self.api3 = api_entry3.get()
        self.QPS = qps_entry.get()
        self.s.get_api(self.QPS, self.api1, self.api2, self.api3)
        self.show_page_process_emo_2()

    def load_date(self):
        while True:
            file_path = filedialog.askopenfilename(
                parent=self.page_choice_path, filetypes=[("CSV files", "*.csv")]
            )
            if file_path:
                if file_path.endswith(".csv"):
                    self.df = r.read_msg(file_path)
                    p_l = tk.Label(
                        self.root,
                        text=f"聊天记录文件为：{file_path}",
                        bg="yellow",
                        font=("SimHei", 12),
                        width=500,
                        height=1,
                    )
                    p_l.pack(side=tk.BOTTOM)
                    break
                else:
                    messagebox.showerror("错误", "请选择一个CSV文件", parent=self.root)  # 显示错误消息
            else:
                break
        self.show_page_load_name()

    def process_data(self):
        self.j_df, self.n_df, self.all_df = dp.process_data(self.df)
        self.s_date = self.all_df.iloc[0]["time"]
        self.e_date = self.all_df.iloc[-1]["time"]

    def Go(self):
        self.s = solve.solve(self.j_df, self.n_df, self.all_df, self.name1, self.name2)
        self.show_page_process_heat()

    def process_heat(self, choice):
        if choice == 1:
            self.s.process_heat(self.name1)
            messagebox.showinfo("分析结果", "分析完毕，结果保存在 ./用户数据/data/src/热力图 中，请自行查看！")
        elif choice == 2:
            self.s.process_heat(self.name2)
            messagebox.showinfo("分析结果", "分析完毕，结果保存在 ./用户数据/data/src/热力图 中，请自行查看！")
        elif choice == 3:
            self.s.process_heat(self.name1 + self.name2)
            messagebox.showinfo("分析结果", "分析完毕，结果保存在 ./用户数据/data/src/热力图 中，请自行查看！")
        elif choice == 4:
            self.s.process_heat(self.name1)
            self.s.process_heat(self.name2)
            self.s.process_heat(self.name1 + self.name2)
            messagebox.showinfo("分析结果", "分析完毕，结果保存在 ./用户数据/data/src/热力图 中，请自行查看！")
        self.show_page_process_time()


    def process_time(self, choice):
        if choice == 1:
            self.s.process_time(self.name1)
            messagebox.showinfo("分析结果", "分析完毕，结果保存在 ./用户数据/data/src/time 中，请自行查看！")
        elif choice == 2:
            self.s.process_time(self.name2)
            messagebox.showinfo("分析结果", "分析完毕，结果保存在 ./用户数据/data/src/time 中，请自行查看！")
        elif choice == 3:
            self.s.process_time(self.name1 + self.name2)
            messagebox.showinfo("分析结果", "分析完毕，结果保存在 ./用户数据/data/src/time 中，请自行查看！")
        elif choice == 4:
            self.s.process_time(self.name1)
            self.s.process_time(self.name2)
            self.s.process_time(self.name1 + self.name2)
            messagebox.showinfo("分析结果", "分析完毕，结果保存在 ./用户数据/data/src/time 中，请自行查看！")
        self.show_page_process_bqb()

    def process_emoji(self, choice):
        if choice == 1:
            self.s.process_emoji()
            messagebox.showinfo("分析结果", "分析完毕，结果保存在 ./用户数据/data/src/emoji 中，请自行查看！")
        self.show_page_process_word_all()

    def process_bqb(self, choice):
        if choice == 1:
            self.s.process_biaoqingbao()
            messagebox.showinfo("分析结果", "分析完毕，结果保存在 ./用户数据/data/src/表情包 中，请自行查看！")
        self.show_page_process_emoji()

    def process_word_all(self, choice):
        if choice == 1:
            self.show_page_process_word_1()
        elif choice == 2:
            self.show_page_process_word_2_fromall()
        else:
            self.show_page_process_emo_all_from_all()

    def process_word(self, choice):
        if choice == 1:
            self.s.process_words(self.name1)
            messagebox.showinfo("分析结果", "分析完毕，结果保存在 ./用户数据/data/src/word 中，请自行查看！")
        elif choice == 2:
            self.s.process_words(self.name2)
            messagebox.showinfo("分析结果", "分析完毕，结果保存在 ./用户数据/data/src/word 中，请自行查看！")
        elif choice == 3:
            self.s.process_words(self.name1 + self.name2)
            messagebox.showinfo("分析结果", "分析完毕，结果保存在 ./用户数据/data/src/word 中，请自行查看！")
        elif choice == 4:
            self.s.process_words(self.name1)
            self.s.process_words(self.name2)
            self.s.process_words(self.name1 + self.name2)
            messagebox.showinfo("分析结果", "分析完毕，结果保存在 ./用户数据/data/src/word 中，请自行查看！")
        self.show_page_process_emo_all()

    def process_emo(self, choice):
        if choice == 1:
            self.show_page_process_emo_1()
        else:
            self.show_page_end_emo_all()

    def process_emo_do(self, choice):
        if choice == 1:
            self.s.process_emo(self.name1)
            messagebox.showinfo("分析结果", "分析完毕，结果保存在 ./用户数据/data/src/emo 中，请自行查看！")
        elif choice == 2:
            self.s.process_emo(self.name2)
            messagebox.showinfo("分析结果", "分析完毕，结果保存在 ./用户数据/data/src/emo 中，请自行查看！")
        elif choice == 3:
            self.s.process_emo(self.name1 + self.name2)
            messagebox.showinfo("分析结果", "分析完毕，结果保存在 ./用户数据/data/src/emo 中，请自行查看！")
        elif choice == 4:
            self.s.process_emo(self.name1)
            self.s.process_emo(self.name2)
            self.s.process_emo(self.name1 + self.name2)
            messagebox.showinfo("分析结果", "分析完毕，结果保存在 ./用户数据/data/src/emo 中，请自行查看！")
        self.show_page_end_emo_2()
