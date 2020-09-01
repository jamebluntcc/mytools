# coding:utf-8

"""
用于配合filter相关字段设置默认值
"""

import datetime


class DynamicCalendarMonth:
    """
    动态获取自然月
    """
    def __init__(self, format_str='%Y-%m-%d', utc=False, start_month_delta=0, end_month_delta=None):
        """

        :param format_str: 格式化
        :param utc: 是否使用utc时间
        :param start_month_delta: 开始日期偏移量（按月），需要指定为整数，否者设为0
        :param end_month_delta: 结束日期偏移量（按月），需要指定为整数，否者设为None（不会返回结束日期）
        """
        self.format_str = format_str
        self.utc = utc
        if not isinstance(start_month_delta, int):
            self.start_month_delta = 0
        else:
            self.start_month_delta = start_month_delta

        if not isinstance(end_month_delta, int):
            self.end_month_delta = None
        else:
            self.end_month_delta = end_month_delta

    def default(self):
        """
        获取filter的默认值接口
        :return:
        """
        default = dict()
        if self.utc:
            today = datetime.datetime.utcnow()
        else:
            today = datetime.datetime.now()

        year = today.year
        month = today.month

        # 开始时间
        start_year = year
        start_month = month
        if self.start_month_delta:
            start_year += (month + self.start_month_delta - 1) // 12
            start_month = (month + self.start_month_delta - 1) % 12 + 1

        default['start'] = datetime.datetime.strftime(datetime.datetime(year=start_year, month=start_month, day=1),
                                                      self.format_str
                                                      )

        # 结束时间(如果没有指定结束时间偏移量，则默认只有开始时间)
        if self.end_month_delta:
            end_year = year
            end_year += (month + self.end_month_delta - 1) // 12
            end_month = (month + self.end_month_delta - 1) % 12 + 1
            default['end'] = datetime.datetime.strftime(datetime.datetime(year=end_year, month=end_month, day=1),
                                                        self.format_str
                                                        )
        return default
