from functools import reduce
from typing import List
import re 

def extract_match(match:re.Match, positions:List[int]):
    length = len(positions)
    if length and length > 1:
        return reduce(lambda x,y: match.group(x) + match.group(y), positions)
    return match.group(3)

def emit_collect_success(*args, **kwargs):
    for item in args:
        print(f"Succesfully collected {item}")
    print(f"TYPE: {kwargs.get('type')}")


def match_signal(message, pattern):
    """Returns a valid match"""
    return re.search(pattern, message)