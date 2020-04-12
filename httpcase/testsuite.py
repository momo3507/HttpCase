# coding: utf-8

import unittest
from httpcase.logger import logger

class TestSuite():
    def __init__(self, testsuite_json):
        super().__init__()
        self.testsuite_json = testsuite_json
        self.name = self.testsuite_json.get("name","test suite")
        self.testcases = []
        self.variables = self.testsuite_json.get("variables",{})     # 套件层变量表

    def addTestcase(self,obj_testcase):
        self.testcases.append(obj_testcase)

    def __call__(self):
        suite = unittest.TestSuite()
        for testcase in self.testcases:
            suite.addTest(testcase)
        return suite
