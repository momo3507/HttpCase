# coding: utf-8
"""
解析变量和函数
"""
import re
from httpcase import functions
from httpcase.logger import logger

P_VARIABLES = r"\${(\w+)}"  # 变量正则
P_FUNCTIONS = r"\${(\w+)\((.*?)\)}"     # 函数正则


class Parse:
    def __init__(self, parse_obj, *findObjs):

        self.parse_obj = parse_obj
        self.findObjs = findObjs
        logger.debug(self.parse_obj)
        logger.debug(self.findObjs)
        self.run()
        logger.debug(self.parse_obj)

    def run(self):
        self.var2value()
        self.fun2value()

    def var2value(self):
        if isinstance(self.parse_obj, dict):
            for key, value in self.parse_obj.items():
                if isinstance(value, str):
                    self.resOfParseValue = re.sub(P_VARIABLES, self.varInfindObj, value)
                    self.parse_obj[key] = self.resOfParseValue
                elif isinstance(value, list):
                    self.parselist = []
                    for e in value:
                        self.resOfParseValue = re.sub(P_VARIABLES, self.varInfindObj, str(e))
                        self.parselist.append(self.resOfParseValue)
                    self.parse_obj[key] = self.parselist
        elif isinstance(self.parse_obj,str):
            self.resOfParseValue = re.sub(P_VARIABLES, self.varInfindObj, self.parse_obj)
            self.parse_obj = self.resOfParseValue


    def varInfindObj(self, matched):
        self.varname = matched.group(1)
        for findObj in self.findObjs:
            self.value = findObj.get(self.varname, None)
            if self.value is not None:
                return str(self.value)
        else:
            return ""

    def fun2value(self):  # 解析函数并执行，需要先执行解析变量并执行
        if isinstance(self.parse_obj, dict):
            for key, value in self.parse_obj.items():
                if isinstance(value, str):
                    self.resOfParseValue = re.sub(P_FUNCTIONS, self.funInfindObj, value)
                    self.parse_obj[key] = self.resOfParseValue
                elif isinstance(value, list):
                    parselist = []
                    for e in value:
                        resOfParseValue = re.sub(P_FUNCTIONS, self.funInfindObj, str(e))
                        parselist.append(resOfParseValue)
                    self.parse_obj[key] = parselist
        elif isinstance(self.parse_obj,str):
            self.resOfParseValue = re.sub(P_FUNCTIONS, self.funInfindObj, self.parse_obj)
            self.parse_obj = self.resOfParseValue


    def funInfindObj(self, matched):
        self.funname = matched.group(1)
        self.strfunparams = matched.group(2)
        self.fun = getattr(functions, self.funname)
        if self.strfunparams == "":
            return self.fun()
        else:
            self.funparams = self.strfunparams.split(",")
            return self.fun(*self.funparams)


if __name__ == '__main__':
    jsonobj = [{}, {}, {'username': 'wangwei', 'password': '1111'}]
    aaa = {'username': '${username}', 'password': '${password}'}
    bbb = '{"username":"${username}","password":1111}'.encode("utf-8")
    ccc = "${__randInt(a,b,c)}"
    ddd = "2020-11-10"
    p = Parse(bbb, *jsonobj)
    p.run()
    print(p.parse_obj)
