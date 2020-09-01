# coding: utf-8
import datetime
import json
from decimal import Decimal
from django.db.models.fields.files import ImageFieldFile

from . import datetime_helper


def instance_to_dict(instance):
    """
    将实例转化成字典
    """
    if not hasattr(instance, '__dict__'):
        return None
    data = {}
    for k, v in instance.__dict__.items():
        if k.startswith('__'):
            continue
        if k.startswith('_'):
            continue
        if callable(v):
            continue
        data[k] = v
    return data


def to_json(data):
    """
    将特殊类型(datetime, date等)类型转化成可以可以序列化的json串
    """
    if isinstance(data, list):
        result = [to_json(item) for item in data]

    elif isinstance(data, dict):
        result = {}
        for key, value in data.items():
            result[key] = to_json(value)

    elif isinstance(data, set):
        result = [to_json(item) for item in data]

    elif isinstance(data, datetime.datetime):
        result = datetime_helper.get_time_str(data)

    elif isinstance(data, datetime.date):
        result = datetime_helper.get_date_str(data)
    elif isinstance(data, Decimal):
        result = float(data)
    else:
        result = data

    return result


def from_json(data):
    """
    将符合特殊类型(datetime, date等)的json串转化成对应的类型
    """
    if isinstance(data, list):
        result = [from_json(item) for item in data]

    elif isinstance(data, dict):
        result = {}
        for key, value in data.items():
            result[key] = from_json(value)
    elif isinstance(data, str):
        value = datetime_helper.parse_datetime(data)
        if not value:
            value = datetime_helper.parse_date(data)

        result = value or data
    else:
        result = data

    return result


def from_python(cls, data):
    """
    将传入的数据构建成传入cls的实例
    :param cls: type of class
    :param data: list or dict
    :return: 如果是data是list，则对其item转化，然后返回一个list
             如果data是dict，则直接对其转化，然后返回一个instance
             如果转化失败，则返回None
    """
    if isinstance(data, list):
        try:
            return [cls(**item) for item in data]
        except:
            return None
    elif isinstance(data, dict):
        try:
            return cls(**data)
        except:
            return None
    return None


def to_python(data):
    """
    将传入的data转化成python内置类型, data内可能包含instance
    """
    if isinstance(data, list):
        return [to_python(item) for item in data]
    elif isinstance(data, tuple):
        return (to_python(item) for item in data)
    elif isinstance(data, Decimal):
        return float(data)
    elif isinstance(data, dict):
        result = {}
        for k, v in data.items():
            result[k] = to_python(v)
    # ImageFieldFile循环引用
    elif isinstance(data, ImageFieldFile):
        if not data:
            return ''
        return data.url
    elif hasattr(data, '__dict__'):
        return to_python(instance_to_dict(data))
    return data


def loads(data_string, cls=None):
    """
    如果cls是None, 则将data_string转化成对应的instance(s)
    否则，转化成python内置类型
    转化失败时：
        如果cls是None, 则返回原字符串
        否则，返回None
    :param data_string: json结构的字符串
    :param cls: type of class
    :return: 
    """
    try:
        data = json.loads(data_string)
        if not cls:
            return data
        else:
            if isinstance(data, list):
                result = []
                for item in data:
                    item_result = from_python(cls, from_json(item))
                    if not item_result:
                        return None
                    result.append(item_result)
                return result or None
            else:
                return from_python(cls, from_json(data))
    except:
        return None if cls else data_string


def dumps(data):
    """
    将传入的数据转化成json结构的字符串
    :param data: 任意数据
    :return: json格式的字符串
    """
    data = to_python(data)
    data = to_json(data)
    if isinstance(data, str):
        return data
    return json.dumps(data)
