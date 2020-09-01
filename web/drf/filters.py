# coding: utf-8
import django_filters

from rest_framework import exceptions


class ChoiceFilter(django_filters.BaseInFilter):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('distinct', False)
        # info为元组类型,元素类型为也是元组
        self.choice = kwargs.pop('choice', kwargs.pop('choices', []))
        # multiple为True时：默认值为列表类型
        self.multiple = kwargs.pop('multiple', False)
        self.default = kwargs.pop('default', None)
        self.display = kwargs.pop('display', True)
        # 联动过滤，字典类型，需包含is_multi、key、name、url
        self.sub = kwargs.pop('sub', None)
        super().__init__(*args, **kwargs)


class ApiSearchFilter(django_filters.BaseInFilter):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('distinct', False)
        self.multiple = kwargs.pop('multiple', False)
        self.url = kwargs.pop('url', None)
        self.search_key = kwargs.pop('search_key', None)
        self.display = kwargs.pop('display', True)
        self.other_keys = kwargs.pop('other_keys', [])  # 要显示的额外字段列表
        self.sep = kwargs.pop('sep', ' ')  # 显示字段的分隔符，默认为空格
        # 联动过滤, 子字段的值受父字段过滤, 需包含key、name、url、is_multi
        self.sub = kwargs.pop('sub', None)
        if not self.url:
            raise exceptions.ValidationError('Parameter "url" of ApiSearch cannot be None')
        if not self.search_key:
            raise exceptions.ValidationError('Parameter "search_key" of ApiSearch cannot be None')

        super().__init__(*args, **kwargs)


class CharFilter(django_filters.CharFilter):
    def __init__(self, *args, **kwargs):
        self.default = kwargs.pop('default', None)
        self.format = kwargs.pop('format', None)
        self.display = kwargs.pop('display', True)
        self.placeholder = kwargs.pop('placeholder', None)
        super().__init__(*args, **kwargs)


class NumberFilter(django_filters.NumberFilter):
    def __init__(self, *args, **kwargs):
        self.default = kwargs.pop('default', None)
        self.format = kwargs.pop('format', None)
        self.display = kwargs.pop('display', True)
        super().__init__(*args, **kwargs)


class DateFromToRangeFilter(django_filters.DateFromToRangeFilter):
    def __init__(self, *args, **kwargs):
        # 默认值为dict类型，包含开始时间start和结束时间end
        self.default = kwargs.pop('default', None)
        self.format = kwargs.pop('format', 'YYYY-MM-DD')
        self.display = kwargs.pop('display', True)
        super().__init__(*args, **kwargs)


class DateTimeFromToRangeFilter(django_filters.DateTimeFromToRangeFilter):
    def __init__(self, *args, **kwargs):
        # 默认值为dict类型，包含开始时间start和结束时间end
        self.default = kwargs.pop('default', None)
        self.format = kwargs.pop('format', 'YYYY-MM-DD HH:mm')
        self.display = kwargs.pop('display', True)
        super().__init__(*args, **kwargs)


class RangeFilter(django_filters.NumericRangeFilter):
    def __init__(self, *args, **kwargs):
        # 单位
        self.addon_after = kwargs.pop('addon_after', None)
        self.display = kwargs.pop('display', True)
        super().__init__(*args, **kwargs)


class DateStringFilter(django_filters.CharFilter):
    def __init__(self, *args, **kwargs):
        p_format = kwargs.pop('p_format', None)
        if not p_format:
            raise exceptions.ArgumentNoneException('Parameter "p_format" of ApiSearch cannot be None')
        self.default = kwargs.pop('default', None)
        if not self.default:
            import datetime
            self.default = datetime.datetime.now().strftime(p_format)
        self.format = kwargs.pop('format', 'YYYY')
        self.display = kwargs.pop('display', True)
        super().__init__(*args, **kwargs)


class BooleanFilter(django_filters.BooleanFilter):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('distinct', False)
        # info为元组类型,元素类型为也是元组
        self.choice = kwargs.pop('choice', kwargs.pop('choices', []))
        if not self.choice:
            self.choice = (('False', '否'), ('True', '是'), ('', '全部'))
        # multiple为True时：默认值为列表类型
        self.multiple = False
        self.default = kwargs.pop('default', None)
        self.display = kwargs.pop('display', True)
        self.sub = None
        super().__init__(*args, **kwargs)
