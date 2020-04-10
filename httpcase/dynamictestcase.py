# coding: utf-8
import unittest
from httpcase.httpsampler import HttpSampler


class DynamicTestClass:
    def __init__(self):
        pass

    def __call__(self):
        TestSequense = type('TestSequense', (unittest.TestCase,), {})
        test_method_name = "test_001"
        test_method =
