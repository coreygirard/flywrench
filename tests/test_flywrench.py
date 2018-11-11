import pytest
from hypothesis import given
from hypothesis.strategies import floats, integers, lists, one_of, text

from src import flywrench


@given(floats())
def test_hashing_floats(e):
    h = flywrench.Cache().make_hash(e)
    assert isinstance(h, str)
    assert len(h) == 32

@given(integers())
def test_hashing_integers(e):
    h = flywrench.Cache().make_hash(e)
    assert isinstance(h, str)
    assert len(h) == 32

@given(text(max_size=100))
def test_hashing_text(e):
    h = flywrench.Cache().make_hash(e)
    assert isinstance(h, str)
    assert len(h) == 32

@given(lists(one_of(floats(),
                    integers(),
                    text(max_size=100)), max_size=10))
def test_hashing_lists(e):
    h = flywrench.Cache().make_hash(e)
    assert isinstance(h, str)
    assert len(h) == 32

@given(integers())
def test_hashing_unique(e):
    h1 = flywrench.Cache().make_hash(e)
    h2 = flywrench.Cache().make_hash(e+1)
    assert h1 != h2




def test_basic():
    class Example(flywrench.Flywrench):
        cache = flywrench.Cache()
        def __init__(self, i):
            self.test = i

    example = Example(5)
    assert example.test == 5


def test_modify():
    class Example2(flywrench.Flywrench):
        cache = flywrench.Cache()
        def __init__(self, i):
            self.test = i

        def test_method(self):
            return self.test + 5

    example = [Example2(42) for i in range(100)]
    example[-1].test = 7

    example = Example2(42)

    assert example.test == 42
    assert example.test_method() == 47

def test_invalid():

    class Example3(flywrench.Flywrench):
        cache = flywrench.Cache()
        def __init__(self, i):
            self.test = i

    example = Example3(2)
    with pytest.raises(AttributeError):
        example.fail

    '''
    >>> Cache().makeHash(4)
    'a8216e26a2093b48a0b7c57159313c8e'

    >>> Cache().makeHash([1,2])
    'ad6352385cc5e69d5c24fad28c7fd226'

    >>> Cache().makeHash([3,4,5])
    '598d44cde01ea1b5b948f409495a003c'

    >>> Cache().makeHash((3,4,5))
    'fa693414f5932aaccbd492381185fe50'
    '''

def test_custom_algorithm():
    class Example(flywrench.Flywrench):
        cache = flywrench.Cache(hash_algorithm=lambda x: 42)

    example = Example()
    example.test = 5
    assert example.test == 5

    example.other = 6
    assert example.test == 6
