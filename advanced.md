
# Advanced

## Separate caches per class

The setup described in *getting started* uses a single cache for all classes. It may be useful at times to have a separate cache for each class definition, perhaps to minimize hash collisions, etc. Doing this is also pretty simple.

Defining multiple classes with a single global cache (simplest):

```python
from flywrench import Flywrench

class SomeClass(Flywrench):
    def __init__(self,i):
        self.test = i

class OtherClass(Flywrench):
    def __init__(self,i):
        self.test = i

some = SomeClass(4)
other = OtherClass(5)

pprint(SomeClass.cache.d)
pprint(OtherClass.cache.d)
```
```
{'785ee38e51369f64df4f68af923b3456': 5, 
 'a8216e26a2093b48a0b7c57159313c8e': 4}

{'785ee38e51369f64df4f68af923b3456': 5, 
 'a8216e26a2093b48a0b7c57159313c8e': 4}
```


Defining multiple classes with distinct individual caches:

```python
from flywrench import Flywrench, Cache # also importing 'Cache'

class SomeClass(Flywrench):
    cache = Cache() # creating separate cache for SomeClass instances
    def __init__(self,i):
        self.test = i

class OtherClass(Flywrench):
    cache = Cache() # creating separate cache for OtherClass instances
    def __init__(self,i):
        self.test = i

some = SomeClass(4)
other = OtherClass(5)

pprint(SomeClass.cache.d)
pprint(OtherClass.cache.d)
```
```
{'a8216e26a2093b48a0b7c57159313c8e': 4}

{'785ee38e51369f64df4f68af923b3456': 5}
```

It is also possible to have multiple classes share the same cache, while others are distinct:

```python
class Apple(Flywrench): # cache is shared with Banana class instances
    def __init__(self,i):
        self.test = i

class Banana(Flywrench): # cache is shared with Apple class instances
    def __init__(self,i):
        self.test = i

class Orange(Flywrench): # cache isn't shared with any other classes
    cache = Cache()
    def __init__(self,i):
        self.test = i

class Pear(Flywrench): # cache isn't shared with any other classes
    cache = Cache()
    def __init__(self,i):
        self.test = i
```

It's important to note that during typical operation, it's not a problem to have multiple classes sharing the same cache, as there is (ideally) a one-to-one relationship between hashes and stored objects. This feature is likely one of those "when you need it, you'll *know*" things.


## Blacklists

Maybe there are instance variables that you don't ever want to be cached. Perhaps they're frequently accessed or modified, and you want the best performance possible. Perhaps you know they'll be tiny variables, and you'd rather store a million integers than a million hashes. Whatever the reason, **flywrench** offers an easy way to 'blacklist' instance variables such that they are stored in the object itself, and never cached.

```python
class SomeClass(Flywrench):
    cache = Cache(blacklist=['test', 'other'])
    def __init__(self,i):
        self.test = i
```

That's it.

Now if we check under the hood:

```python
some = SomeClass(5)
print(SomeClass.cache.d)
```
```
{}
```

If we hadn't specified the blacklist:

```python
class SomeClass(Flywrench):
    cache = Cache()
    def __init__(self,i):
        self.test = i

some = SomeClass(5)
print(SomeClass.cache.d)
```
```
{'785ee38e51369f64df4f68af923b3456': 5}
```

Just don't change the blacklist after defining the class. It'll cause ~~a hideous and catastrophic mess~~ unexpected behavior. Plus errors. Lots of errors.

## Custom hash functions

What if you don't like the `pickle.dumps`/`hashlib.md5` tag-team that **flywrench** currently rolls with for hashing of arbitrary objects? Can you roll your own? You bet!

```python
from flywrench import Flywrench, Cache

def crapHash(obj): # don't you dare use this anywhere
    try:
        return len(obj)
    except:
        return -1

# needs to be Cache().makeHash, not Cache.makeHash
Cache().makeHash = crapHash
```

There you go. It's all 'upgraded'. And it's probably a bit faster, too! Let's take it for a spin:

```python
class SomeClass(Flywrench):
    def __init__(self,i):
        self.test = i

a = SomeClass(1)
b = SomeClass((4,5,6))
c = SomeClass([2,3])

pprint(SomeClass.cache.d)

print(a.test)
print(b.test)
print(c.test)
```
```
{-1: 1, 
  2: [2, 3], 
  3: (4, 5, 6)}

1
(4, 5, 6)
[2, 3]
```

So far so good!

```python
d = SomeClass((7,8))
print(c.test)
print(d.test)
```

```
(7, 8) # should be [2, 3]
(7, 8) # should be (7, 8)
```

With great power comes great responsibility. Looks like `crapHash` won't be replacing `pickle.dumps`/`hashlib.md5` any time soon. But now you know how to define your own custom hash function. It's also possible to define different hash functions for different classes:


```python
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

temp = [SomeClass(1),
        SomeClass((4, 5, 6)),
        SomeClass([2, 3]),
        SomeClass((7, 8)),
        OtherClass(1),
        OtherClass((4, 5, 6)),
        OtherClass([2, 3]),
        OtherClass((7, 8))]

pprint(SomeClass.cache.d)
pprint(OtherClass.cache.d)
```

```
{'hash1:1': [1],
 'hash1:2-3': [2, 3],
 'hash1:4-5-6': (4, 5, 6),
 'hash1:7-8': (7, 8)}

{'hash2:1': [1],
 'hash2:2.3': [2, 3],
 'hash2:4.5.6': (4, 5, 6),
 'hash2:7.8': (7, 8)}
```
