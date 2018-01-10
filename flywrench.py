import hashlib
import pickle
import types


class Cache(object):
    def __init__(self,blacklist=None,hash_algorithm=None):
        self.d = {}
        if blacklist:
            self.blacklist = blacklist
        else:
            self.blacklist = []

        if hash_algorithm:
            self.makeHash = hash_algorithm

    def makeHash(self,obj):
        s = pickle.dumps(obj)

        # TODO: upgrade to faster hash lib, perhaps CityHash or FarmHash
        return hashlib.md5(s).hexdigest()


class Flywrench(object):
    cache = Cache()

    def __getattribute__(self,k):
        # don't cache the cache
        if k == 'cache':
            return object.__getattribute__(self,k)
        elif k in self.cache.blacklist:
            return object.__getattribute__(self,k)
        else:
            # return methods without any cache retrieval
            if isinstance(object.__getattribute__(self,k), types.MethodType):
                return object.__getattribute__(self,k)

            # get the stored hash value and look up
            h = object.__getattribute__(self,k)
            return self.cache.d[h]

    def __setattr__(self,k,v):
        if k in self.cache.blacklist:
            object.__setattr__(self,k,v)
        else:
            h = self.cache.makeHash(v)
            object.__setattr__(self,k,h)
            self.cache.d[h] = v
