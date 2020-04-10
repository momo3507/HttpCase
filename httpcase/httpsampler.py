# coding: utf-8

from httpcase.parse import Parse
from httpcase.jsonextractor import JsonExtractor
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


class HttpSampler():
    def __init__(self, http_json):
        self.http_json = http_json
        self.name = self.http_json.get("name","test step")
        self.method = self.http_json.get("method")
        self.path = self.http_json.get("path")
        self.project_variables = {}     # 整个项目的全局变量表
        self.testsuite_variables = {}   # 所属套件变量表
        self.testcase_variables = {}     # 所属用例的变量表
        self.project_HttpRequestDefaults = {}
        self.project_HttpHeaderDefaults = {}
        self.params = self.http_json.get("params", None)
        self.body = self.http_json.get("body", None)
        self.json = None
        self.data = None
        if self.body:
            if isinstance(self.body,dict):
                self.json = self.body
            else:
                self.data = self.body
        self.extract = self.http_json.get("extract", None)
        self.assertion = self.http_json.get("assertion",[])

    def setSession(self, obj_session):
        self.session = obj_session

    def genurl(self):
        self.protocol = self.http_json.get("protocol") if self.http_json.get(
            "protocol") else self.project_HttpRequestDefaults.get("protocol")
        self.ip = self.http_json.get("ip") if self.http_json.get(
            "ip") else self.project_HttpRequestDefaults.get("ip")
        self.port = self.http_json.get("port") if self.http_json.get(
            "port") else self.project_HttpRequestDefaults.get("port")
        self.url = "{protocol}://{ip}:{port}{path}".format(protocol=self.protocol,ip=self.ip,port=self.port,path=self.path)

    def run(self):
        logging.info(">>> Running test step: %s" % self.name)
        self.genurl()
        self.parselist = [Parse(property, self.testcase_variables,self.testsuite_variables,self.project_variables)
                          for property in [self.params,self.json]]  # 设置http对象的parselist属性
        # self.parsekwargs = [Parse(self.kwargs[key], self.tgvariables, self.tpvariables)for key in self.kwargs.keys()]
        for parse in self.parselist:
            parse.run()

        if self.method == "GET":
            self.response = self.session.get(url=self.url, params=self.params, headers=self.project_HttpHeaderDefaults)
        elif self.method == "POST":
            self.response = self.session.post(self.url, params=self.params, data=self.data, json=self.json,
                                         headers=self.project_HttpHeaderDefaults)
        if self.extract:
            logging.debug("running extractor: %s"%self.extract)
            for varname, path in self.extract.items():
                self.testcase_variables[varname] = JsonExtractor(self.response.json(), path).res
            logging.debug("testcasr_variables：%s"%self.testcase_variables)
        self.assertlist = [Parse(property, self.testcase_variables, self.testsuite_variables, self.project_variables)
                          for property in self.assertion]  # 设置http对象的parselist属性
        for assert_parse in self.assertlist:
            assert_parse.run()


        return self.response