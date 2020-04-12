# coding: utf-8

import ast
from httpcase.parse import Parse
from httpcase.jsonextractor import JsonExtractor
from httpcase.logger import logger


class HttpSampler():
    def __init__(self, http_json):
        self.http_json = http_json
        self.name = self.http_json.get("name", "test step")
        self.method = self.http_json.get("method")
        self.path = self.http_json.get("path")
        self.step_headers = self.http_json.get("headers", {})
        self.project_variables = {}  # 整个项目的全局变量表
        self.testsuite_variables = {}  # 套件中变量表
        self.testcase_variables = {}  # 用例中的变量表
        self.project_HttpRequestDefaults = {}
        self.project_HttpHeaderDefaults = {}
        self.params = self.http_json.get("params", None)
        self.body = self.http_json.get("body", None)
        self.extract = self.http_json.get("extract", None)
        self.assertion = self.http_json.get("assertion", [])

    def setSession(self, obj_session):
        self.session = obj_session

    def __gen_url(self):
        # 生成完整url
        self.protocol = self.http_json.get("protocol") if self.http_json.get(
            "protocol") else self.project_HttpRequestDefaults.get("protocol")
        self.ip = self.http_json.get("ip") if self.http_json.get(
            "ip") else self.project_HttpRequestDefaults.get("ip")
        self.port = self.http_json.get("port") if self.http_json.get(
            "port") else self.project_HttpRequestDefaults.get("port")
        self.url = "{protocol}://{ip}:{port}{path}".format(protocol=self.protocol, ip=self.ip, port=self.port,
                                                           path=self.path)

    def __gen_headers(self):
        # 生成完整请求头
        self.headers = self.project_HttpHeaderDefaults.copy()
        self.headers.update(self.step_headers)

    def __parse(self, http_property):
        return Parse(http_property, self.testcase_variables, self.testsuite_variables, self.project_variables).parse_obj

    def run(self):
        logger.info(">>> Running test step: %s" % self.name)
        self.__gen_url()
        self.__gen_headers()
        # 解析运行前参数中的变量和函数
        self.url = self.__parse(self.url)
        self.headers = self.__parse(self.headers)
        self.params = self.__parse(self.params)
        self.body = self.__parse(self.body)
        self.body = self.body.encode("utf-8") if isinstance(self.body,str) else self.body
        # 发起请求
        logger.info("======url-headers-params-body=======")
        for p in [self.url, self.headers,self.params,self.body]:
            logger.info(p)
        logger.info("=========================================")
        if self.method == "GET":
            self.response = self.session.get(url=self.url, params=self.params, headers=self.headers)
        elif self.method == "POST":
            self.response = self.session.post(self.url, params=self.params, data=self.body, headers=self.headers)
        if self.extract:
            logger.debug("running extractor: %s" % self.extract)
            for varname, path in self.extract.items():
                self.testcase_variables[varname] = JsonExtractor(self.response.json(), path).res
            logger.debug("testcasr_variables：%s" % self.testcase_variables)
        # 解析断言中的变量和函数
        self.assertlist = [Parse(property, self.testcase_variables, self.testsuite_variables, self.project_variables).parse_obj
                           for property in self.assertion]
        logger.debug(self.assertlist)

        return self.response
