# -*- coding: utf-8 -*-
from redis import Redis
import json

def get_data(keys):
    r = Redis(host='localhost', port=6379, decode_responses=True)
    data = json.loads(r.get(keys))
    return data
