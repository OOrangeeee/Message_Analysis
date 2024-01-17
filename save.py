class save_data:
    def __init__(self):
        """
        构造函数，初始化一些可能需要的属性。
        """
        pass

    def __str__(self):
        """
        字符串表示，用于打印对象时提供有用的信息。
        """
        return "draw类实例，用于保存数据"
        pass

    def save_data_all(self, data, path):
        for d, p in zip(data, path):
            d.to_excel(p, index=False)
        pass
