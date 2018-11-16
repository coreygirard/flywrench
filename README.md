# flywrench

[![Build Status](https://travis-ci.org/coreygirard/flywrench.svg?branch=master)](https://travis-ci.org/coreygirard/flywrench) <br>
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black) <br><br>

An ultralight drop-in module implementing the [flyweight](https://en.wikipedia.org/wiki/Flyweight_pattern) [design](https://refactoring.guru/design-patterns/flyweight) [pattern](http://w3sdesign.com/?gr=s06&ugr=proble#gf)

## Getting started

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
    def __init__(self, args):
        # more magic
```

```python
# do this
class SomeClass(Flywrench):
    def __init__(self, args):
        # more magic
```

- Step 4: _there is no Step 4_

**ENJOY!**

## Advanced

[tricks and tips](docs/advanced.md)

## To Do

- [ ] Move
- [ ] Perhaps garbage collection. Keep track of how many links there are to a given object in cache, and when the number of links hits zero, delete it
