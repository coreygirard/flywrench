import unittest
import doctest
import flywrench


class TestBasic(unittest.TestCase):
    def test_basic(self):

        class Example(flywrench.Flywrench):
            cache = flywrench.Cache()
            def __init__(self,i):
                self.test = i

        example = Example(5)
        self.assertEqual(example.test,5)

        print(Example.cache.d)

class TestModify(unittest.TestCase):
    def test_modify(self):

        class Example2(flywrench.Flywrench):
            cache = flywrench.Cache()
            def __init__(self,i):
                self.test = i

            def testMethod(self):
                return self.test + 5

        example = [Example2(42) for i in range(100)]
        example[-1].test = 7
        print(Example2.cache.d)

        example = Example2(42)

        print(dir(example))

        self.assertEqual(example.test,42)
        self.assertEqual(example.testMethod(),47)

class TestInvalidAttribute(unittest.TestCase):
    def test_invalid(self):

        class Example3(flywrench.Flywrench):
            cache = flywrench.Cache()
            def __init__(self,i):
                self.test = i

        example = Example3(2)
        with self.assertRaises(AttributeError):
            example.fail



# test calling methods



def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(flywrench))
    return tests

if __name__ == '__main__':
    unittest.main()
