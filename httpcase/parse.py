# coding: utf-8
"""
解析变量和函数
"""
import re
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')

from httpcase import functions

P_VARIABLES = r"\${(\w+)}"
P_FUNCTIONS = r"\${(\w+)\((.*?)\)}"
class Parse:
    def __init__(self,parsejson,*findObjs):
        self.parsejson = parsejson
        self.findObjs = findObjs

    def run(self):
        self.var2value()
        self.fun2value()

    def var2value(self):
        if isinstance(self.parsejson,dict):
            for key,value in self.parsejson.items():
                self.resOfParseValue = re.sub(P_VARIABLES,self.varInfindObj,value)
                self.parsejson[key] = self.resOfParseValue


    def varInfindObj(self,matched):
        self.varname = matched.group(1)
        for findObj in self.findObjs:
            self.value = findObj.get(self.varname)
            if self.value:
                return str(self.value)
        else:
            #raise Exception("变量 %s 未定义"%self.varname)
            return ""

    def fun2value(self):    # 解析函数并执行，需要先执行解析变量并执行
        if isinstance(self.parsejson,dict):
            for key,value in self.parsejson.items():
                resOfParseValue = re.sub(P_FUNCTIONS,self.funInfindObj,value)
                self.parsejson[key] = resOfParseValue

    def funInfindObj(self,matched):
        self.funname = matched.group(1)
        self.strfunparams = matched.group(2)
        self.fun = getattr(functions, self.funname)
        if self.strfunparams == "":
            return self.fun()
        else:
            self.funparams = self.strfunparams.split(",")
            return self.fun(*self.funparams)



if __name__ == '__main__':

    jsonobj = {"ip":"192.168.1.2","port":7000}
    aaa = {"url":"http://${ip}:${__randInt(1,${port})}","abc":"2020-01-01"}
    bbb = "${__randInt(a,b,c)}"
    ccc = "2020-11-10"
    Parse(aaa,jsonobj).run()
    print(aaa)