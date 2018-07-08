# -*- coding: utf-8 -*-

from functools import reduce


def distinct_append(list1, list2):
    seen = set(list1)
    seen_add = seen.add
    for elem in list2:
        if elem not in seen:
            seen_add(elem)
            list1.append(elem)

def distinct(list1):
    seen = set()
    seen_add = seen.add
    return [elem for elem in list1 if elem not in seen and not seen_add(elem)]

foldRight = lambda func, acc, xs: reduce(lambda x, y: func(y, x), xs[::-1], acc)

def flatten(list1):
    flatlist = [x for sublist in list1 for x in sublist]
    return flatlist

def getOrElse(json, name, default):
    value = json.get(name, default)
    if value is not None:
        return value
    else:
        return default