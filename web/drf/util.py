import inspect
from collections import OrderedDict

import yaml


def cls_str_of_meth(meth):
    mod = inspect.getmodule(meth)
    cls = meth.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0]
    return '{0}.{1}'.format(mod.__name__, cls)


def cls_str_of_obj(obj):
    return '{0}.{1}'.format(obj.__class__.__module__, obj.__class__.__name__)


def cls_str_of_cls(cls):
    return '{0}.{1}'.format(cls.__module__, cls.__name__)


def meth_str(meth):
    return '{0}.{1}'.format(meth.__module__, meth.__qualname__)


def import_from_str(cls_path):
    module_name, class_name = cls_path.rsplit('.', 1)
    module_meta = __import__(module_name, globals(), locals(), [class_name])
    class_meta = getattr(module_meta, class_name)
    return class_meta


def to_choices_dict(choices):
    """
    Convert choices into key/value dicts.

    to_choices_dict([1]) -> {1: 1}
    to_choices_dict([(1, '1st'), (2, '2nd')]) -> {1: '1st', 2: '2nd'}
    to_choices_dict([('Group', ((1, '1st'), 2))]) -> {'Group': {1: '1st', 2: '2'}}
    """
    # Allow single, paired or grouped choices style:
    # choices = [1, 2, 3]
    # choices = [(1, 'First'), (2, 'Second'), (3, 'Third')]
    # choices = [('Category', ((1, 'First'), (2, 'Second'))), (3, 'Third')]
    ret = OrderedDict()
    for choice in choices:
        if not isinstance(choice, (list, tuple)):
            # single choice
            ret[choice] = choice
        else:
            key, value = choice
            if isinstance(value, (list, tuple)):
                # grouped choices (category, sub choices)
                ret[key] = to_choices_dict(value)
            else:
                # paired choice (key, display value)
                ret[key] = value
    return ret


def flatten_choices_dict(choices):
    """
    Convert a group choices dict into a flat dict of choices.

    flatten_choices_dict({1: '1st', 2: '2nd'}) -> {1: '1st', 2: '2nd'}
    flatten_choices_dict({'Group': {1: '1st', 2: '2nd'}}) -> {1: '1st', 2: '2nd'}
    """
    ret = OrderedDict()
    for key, value in choices.items():
        if isinstance(value, dict):
            # grouped choices (category, sub choices)
            for sub_key, sub_value in value.items():
                ret[sub_key] = sub_value
        else:
            # choice (key, display value)
            ret[key] = value
    return ret


def yaml_to_dict(doc_string):
    try:
        res = yaml.load(doc_string)
    except:
        res = {}
    return res or {}
