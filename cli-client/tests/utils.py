from collections import Counter
from frozendict import frozendict
import json

def json_process(item):
    if isinstance(item, dict):
        return frozendict((key,json_process(value)) for key, value in item.items())
    if isinstance(item, list):
        return frozendict(Counter(json_process(x) for x in item))
    else:
        return item

def json_compare(a,b):
    return json_process(a) == json_process(b)

def json_compare2(stdout,b):
    """Skips 1st line of stdout and compares with b"""
    a = stdout.split('\n')
    a = ''.join(a[1:])
    a = json.loads(a)
    return json_process(a) == json_process(b)

