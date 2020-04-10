# coding: utf-8

import logging
import requests
import unittest

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


def add_test(httpobj):
    def test(case):
        response = httpobj.run()
        for assertinfo in httpobj.assertion:
            for assert_exp,assert_value in assertinfo.items():
                ele1 = assert_value[0] if assert_value[0] not in response.__attrs__ else response.__getattribute__(
                    assert_value[0])
                ele2 = assert_value[1] if assert_value[1] not in response.__attrs__ else response.__getattribute__(
                    assert_value[1])
                if assert_exp == "eq":
                    case.assertEqual(str(ele1), str(ele2))
                else:
                    raise Exception("不支持的断言：%s"%assert_exp)

    return test


class TestCase():
    def __init__(self, testcase_json):
        self.testcase_json = testcase_json
        self.name = self.testcase_json.get("name", "test case")
        self.httpsamplers = []
        self.session = requests.session()
        self.variables = self.testcase_json.get("variables",{})     # 用例层的变量表

    def addHttpsampler(self, obj_http):
        self.httpsamplers.append(obj_http)

    def run(self):
        logging.info("--------running testcase: %s" % self.name)
        for httpsampler in self.httpsamplers:
            httpsampler.run()

    def __call__(self):
        testcase = type('HttpCase', (unittest.TestCase,), {})
        for index, httpsampler in enumerate(self.httpsamplers, start=1):
            test_method = add_test(httpsampler)
            setattr(testcase, "test_%s" % (index), test_method)
        case = unittest.TestLoader().loadTestsFromTestCase(testcase)
        return case
