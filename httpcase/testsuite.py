# coding: utf-8

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

class TestSuite:
    def __init__(self,testsuite_json):
        self.testsuite_json = testsuite_json
        self.name = self.testsuite_json.get("name","test suite")
        self.testcases = []

    def addTestcase(self,obj_testcase):
        self.testcases.append(obj_testcase)

    def run(self):
        logging.info("--running testsuite: %s"%self.name)
        for testcase in self.testcases:
            testcase.run()
