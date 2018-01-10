import hashlib
import pickle
import types


class Cache(object):
    def __init__(self,blacklist=None,hash_algorithm=None):
        '''
        >>> cache = Cache(blacklist=['aaa','bbb','ccc'])
        >>> cache.blacklist
        ['aaa', 'bbb', 'ccc']
        '''
        self.d = {}
        if blacklist: self.blacklist = blacklist
        else: self.blacklist = []

        if hash_algorithm: self.makeHash = hash_algorithm

    def makeHash(self,obj):
        '''
        >>> Cache().makeHash([3,4,5])
        '598d44cde01ea1b5b948f409495a003c'
        '''
        s = pickle.dumps(obj)

        # TODO: upgrade to faster hash lib, perhaps CityHash or FarmHash
        return hashlib.md5(s).hexdigest()


class Flywrench(object):
    '''
    >>> f = Flywrench()
    >>> type(f.cache) == type(Cache())
    True
    '''

    cache = Cache()

    def __getattribute__(self,k):
        '''
        >>> f = Flywrench()
        >>> f.test = 'hello'
        >>> f.test
        'hello'
        '''

        if k == 'cache':
            # don't cache the cache
            return object.__getattribute__(self,k)
        elif k in self.cache.blacklist:
            # if object is blacklisted, it's stored in the instance
            return object.__getattribute__(self,k)
        elif isinstance(object.__getattribute__(self,k), types.MethodType):
            # if we're accessing a method, just return it
            return object.__getattribute__(self,k)
        else:
            # get the stored hash value and look up in cache
            h = object.__getattribute__(self,k)
            return self.cache.d[h]

    def __setattr__(self,k,v):
        if k in self.cache.blacklist:
            # store object directly into instance
            object.__setattr__(self,k,v)
        else:
            # store hash in instance and object in cache
            h = self.cache.makeHash(v)
            object.__setattr__(self,k,h)
            self.cache.d[h] = v
