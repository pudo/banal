#!/usr/bin/env python3
import sys
import unittest
from collections import OrderedDict
from pathlib import Path

thisDir = Path(__file__).parent

sys.path.insert(0, str(thisDir.parent))


from banal.dicts import items, keys, values

class UniformIterationTests(unittest.TestCase):
    testMatrix = []
    uniform_iteration_functions = tuple((f, getattr(dict, f.__name__)) for f in (keys, values, items))

    def test_uniform_iteration(self):
        test_dic = {0: "a", 1: "b", 2: "c"}
        test_seq = tuple(test_dic.values())

        for func, etalon_getter in self.__class__.uniform_iteration_functions:
            with self.subTest(func=func):
                etalon_res = tuple(etalon_getter(test_dic))
                with self.subTest(etalon_res=etalon_res):
                    with self.subTest(seq=test_seq):
                        self.assertEqual(tuple(func(test_seq)), etalon_res)

                    with self.subTest(dic=test_dic):
                        self.assertEqual(tuple(func(test_dic)), etalon_res)


if __name__ == "__main__":
    unittest.main()
