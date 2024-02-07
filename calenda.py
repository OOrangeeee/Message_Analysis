# 最后编辑：
# 晋晨曦 2024.1.26 15.46
# qq：2950171570
# email：Jin0714@outlook.com  回复随缘
from calendar import monthrange
from numpy import ones


def generate_calendar(year, month):
    """
    返回日历样式的numpy数组
    :param year: 年份
    :param month: 月份
    :return: numpy数组
    """
    first_day_weekday, month_days = monthrange(year, month)
    rows_needed = ((first_day_weekday + month_days - 1) // 7) + 1
    calendar_array = ones((rows_needed, 7), dtype=int)
    day_counter = 1

    for week in range(rows_needed):
        for day in range(7):
            if week > 0 or day >= first_day_weekday:
                if day_counter <= month_days:
                    calendar_array[week][day] = 0
                day_counter += 1

    return calendar_array


def get_month_dates(year1, month1, year2, month2):
    """
    返回时间范围
    :param year1: 开始年
    :param month1: 开始月
    :param year2: 结束年
    :param month2: 结束月
    :return: 时间范围
    """
    first_date = f"{year1}-{str(month1).zfill(2)}-01"

    last_day = monthrange(year2, month2)[1]
    last_date = f"{year2}-{str(month2).zfill(2)}-{last_day}"

    return first_date, last_date
