# flywrench

A

[flyweight]() [design](https://refactoring.guru/design-patterns/flyweight) [pattern]()

### Getting started

- Step 1: install **flywrench**

```
pip install flywrench
```

- Step 2: import **flywrench**

```python
from flywrench import Flywrench
```

- Step 3: subclass from **flywrench**

```python
# instead of this
class SomeClass(object):
    def __init__(self,args):
        # more magic
```

```python
# do this
class SomeClass(Flywrench):
    def __init__(self,args):
        # more magic
```

- Step 4: *there is no Step 4*

**ENJOY!**

## Advanced

[tricks and tips](advanced.md)

## To Do

- [ ] Implement ability to specify a blacklist of attributes to not cache
- [ ] Perhaps garbage collection. Keep track of how many links there are to a given object in cache, and when the number of links hits zero, delete it


