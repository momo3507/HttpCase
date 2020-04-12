# coding: utf-8
import yaml
import unittest
import os
from httpcase import HTMLTestRunner
from httpcase.testsuite import TestSuite
from httpcase.testcase import TestCase
from httpcase.httpsampler import HttpSampler
from httpcase.logger import logger

class Project:
    def __init__(self,file_or_json):
        self.file_json = file_or_json
        if os.path.isfile(self.file_json):
            with open(self.file_json,"r",encoding="utf-8") as f:
                self.file_obj = f.read()
            self.file_json = yaml.load(self.file_obj,Loader=yaml.FullLoader)    # 测试文件转结构体
        self.project_name = self.file_json.get("project", "My Project")  # 项目名称
        self.description = self.file_json.get("description", None)  # 项目描述
        self.variables = self.file_json.get("variables", {})     # 获取项目的变量表
        self.HttpRequestDefaults = self.file_json.get("HttpRequestDefaults", {})    # 获取项目的默认值
        self.HttpHeaderDefaults = self.file_json.get("HttpHeaderDefaults", {})      # 获取项目的默认请求头
        self.testsuites = []     # 测试套件列表

        self.__package()    # 元素装箱，组装测试计划对象

    def run(self):
        logger.info("Start Testing Project: -----------  {project_name}  -----------".format(project_name=self.project_name))
        suites = unittest.TestSuite()
        for testsuite in self.testsuites:
            suites.addTest(testsuite)
        # unittest.TextTestRunner(verbosity=2).run(suites)
        reportpath = os.getcwd() + "\\report.html"
        f = open(reportpath,"wb")
        runner = HTMLTestRunner.HTMLTestRunner(stream=f,title=self.project_name,description=self.description)
        runner.run(suites)

    def __package(self):
        # 组装项目的测试用例
        self.testsuites_list = self.__get_testsuites()
        for testsuite_json in self.testsuites_list:
            self.testsuite = TestSuite(testsuite_json)    # 创建testsuite对象
            for testcase_json in testsuite_json.get("testcases",[]):    # 获取用例json列表
                self.testcase = TestCase(testcase_json)     # 创建testcase对象
                for http_json in testcase_json.get("httpsteps", []):    # 获取测试步骤json列表
                    self.httpsampler = HttpSampler(http_json)   # 创建请求对象
                    self.httpsampler.setSession(self.testcase.session)
                    self.httpsampler.project_variables = self.variables
                    self.httpsampler.testsuite_variables = self.testsuite.variables
                    self.httpsampler.testcase_variables = self.testcase.variables
                    self.httpsampler.project_HttpHeaderDefaults = self.HttpHeaderDefaults
                    self.httpsampler.project_HttpRequestDefaults = self.HttpRequestDefaults
                    self.testcase.addHttpsampler(self.httpsampler)
                self.testsuite.addTestcase(self.testcase())
            self.testsuites.append(self.testsuite())


    def __get_testsuites(self):
        # 返回测试套件列表
        self.__testsuites = self.file_json.get("testsuites",[])
        return self.__testsuites
