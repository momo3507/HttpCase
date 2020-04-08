# coding: utf-8
import yaml
import logging
from httpcase.testsuite import TestSuite
from httpcase.testcase import TestCase
from httpcase.httpsampler import HttpSampler

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

class Project:
    def __init__(self,file_testcase):
        self.file_testcase = file_testcase
        with open(self.file_testcase,"r",encoding="utf-8") as f:
            self.file_obj = f.read()
        self.file_json = yaml.load(self.file_obj,Loader=yaml.FullLoader)    # 测试文件转结构体
        self.project_name = self.file_json.get("project", "My Project")  # 获取项目名称
        self.variables = self.file_json.get("variables", {})     # 获取项目的变量表
        self.HttpRequestDefaults = self.file_json.get("HttpRequestDefaults", {})    # 获取项目的默认值
        self.HttpHeaderDefaults = self.file_json.get("HttpHeaderDefaults", {})      # 获取项目的默认请求头
        self.testsuites = []     # 测试套件列表

        self.__package()    # 元素装箱，组装测试计划对象

    def run(self):
        logging.info("Start Testing : ---------------  {project_name}  ---------------".format(project_name=self.project_name))
        for testsuite in self.testsuites:
            testsuite.run()


    def __package(self):
        # 组装项目的测试用例
        self.testsuites_list = self.__get_testsuites()
        for testsuite_json in self.testsuites_list:
            self.testsuite = TestSuite(testsuite_json)    # 创建testsuite对象
            self.testsuites.append(self.testsuite)
            for testcase_json in testsuite_json.get("testcases",[]):    # 获取用例json列表
                self.testcase = TestCase(testcase_json)
                self.testsuite.addTestcase(self.testcase)
                for http_json in testcase_json.get("httpsteps", []):    # 获取测试步骤json列表
                    self.httpsampler = HttpSampler(http_json)
                    self.httpsampler.setSession(self.testcase.session)
                    self.httpsampler.project_variables = self.variables
                    self.httpsampler.project_HttpHeaderDefaults = self.HttpHeaderDefaults
                    self.httpsampler.project_HttpRequestDefaults = self.HttpRequestDefaults
                    self.testcase.addHttpsampler(self.httpsampler)

    def __get_testsuites(self):
        # 返回测试套件列表
        self.__testsuites = self.file_json.get("testsuites",[])
        return self.__testsuites