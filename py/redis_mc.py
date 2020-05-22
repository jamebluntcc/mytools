import re
import redis
import pickle
import inspect
from functools import wraps

__formaters = {}
percent_pattern = re.compile(r"%\w")
brace_pattern = re.compile(r"\{[\w\d\.\[\]_]+\}")

MC_DEFAULT_EXPIRE_IN = 0

mc = redis.StrictRedis(host='localhost', port='6379')



def formater(text):
    percent = percent_pattern.findall(text)
    brace = brace_pattern.search(text)
    if percent and brace:
        raise Exception('mixed format is not allowed')

    if percent:
        n = len(percent)
        return lambda *a, **kw: text % tuple(a[:n])
    elif '%(' in text:
        return lambda *a, **kw: text % kw
    else:
        return text.format


def format(text, *a, **kw):
    f = __formaters.get(text)
    if f is None:
        f = formater(text)
        __formaters[text] = f
    return f(*a, **kw)


def gen_key_factory(key_pattern, arg_names, defaults):
    args = dict(zip(arg_names[-len(defaults):], defaults)) if defaults else {}
    if callable(key_pattern):
        names = inspect.getargspec(key_pattern)[0]

    def gen_key(*a, **kw):
        aa = args.copy()
        aa.update(zip(arg_names, a))
        aa.update(kw)
        if callable(key_pattern):
            key = key_pattern(*[aa[n] for n in names])
        else:
            key = format(key_pattern, *[aa[n] for n in arg_names], **aa)
        return key and key.replace(' ', '_'), aa
    return gen_key


def cached(key_pattern, mc=mc, expire=MC_DEFAULT_EXPIRE_IN):
    def deco(f):
        arg_names, varagrs, varkw, defaults = inspect.getfullargspec(f)[:4]
        if varagrs or varkw:
            raise Exception("not support varargs or varkwagrs")
        gen_key = gen_key_factory(key_pattern, arg_names, defaults)

        @wraps(f)
        def _(*a, **kw):
            key, args = gen_key(*a, **kw)
            if not key:
                return f(*a, **kw)
            r = mc.get(key)
            if r is not None:
                return pickle.loads(r)
            r = f(*a, **kw)
            if r is not None and expire != 0:
                mc.set(key, pickle.dumps(r), expire)
            elif r is not None:
                mc.set(key, pickle.dumps(r))
            return r

        _.original_function = f
        return _
    return deco


@cached('test:{a}:{b}')
def test(a=1, b=2):
    return a+b, a, b


if __name__ == '__main__':
    # mc.delete('test:%s' %1)
    # print(gen_key_factory('test:{id}:{a}', ('id', 'a'), defaults=None)(1, 2))
    print(test(1, 3))


