from pprint import pprint
import unittest
import doctest
from flywrench import Flywrench, Cache


def hash1(obj):
    return 'hash1:'+'-'.join([str(e) for e in obj])

def hash2(obj):
    return 'hash2:'+'.'.join([str(e) for e in obj])


class SomeClass(Flywrench):
    cache = Cache(hash_algorithm=hash1)
    def __init__(self,i):
        self.test = i

class OtherClass(Flywrench):
    cache = Cache(hash_algorithm=hash2)
    def __init__(self,i):
        self.test = i

temp = [SomeClass([1]),
        SomeClass((4,5,6)),
        SomeClass([2,3]),
        SomeClass((7,8)),
        OtherClass([1]),
        OtherClass((4,5,6)),
        OtherClass([2,3]),
        OtherClass((7,8))]


pprint(SomeClass.cache.d)
pprint(OtherClass.cache.d)
