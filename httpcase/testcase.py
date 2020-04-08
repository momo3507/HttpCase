# coding: utf-8

import logging
import requests
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

class TestCase:
    def __init__(self,testcase_json):
        self.testcase_json = testcase_json
        self.name = self.testcase_json.get("name","test case")
        self.httpsamplers = []
        self.session = requests.session()
    def addHttpsampler(self,obj_http):
        self.httpsamplers.append(obj_http)

    def run(self):
        logging.info("--------running testcase: %s"%self.name)
        for httpsampler in self.httpsamplers:
            httpsampler.run()


