# HttpCase
通过yaml定义测试用例
## 使用说明：
```
# coding: utf-8
from httpcase.project import Project

testcase = "httpcase.yml"
project = Project(testcase)
project.run()
```
## yaml 用例格式
```
# This is HttpCase code mode
project: 我的HttpCase项目  #项目名称
variables:  # 定义的全局变量
    username: wangwei
    password: 1111
HttpRequestDefaults: # http请求默认值
    protocol: http
    ip: 127.0.0.1
    port: 5000
HttpHeaderDefaults: # 请求头默认值
    Content-Type: application/json
    token: 1ytd234567qwert
testsuites:   # 测试套件列表（测试模块列表）
    -
        name: 用户登录模块    # 套件（模块）名称
        variables: {}   # 套件（模块）变量
        testcases: # 用例列表（一个套件中多条用例）
            -
                name: 登录后进行查询     # 测试用例名称
                description: 测试xx情况下，功能是否正常     # 测试用例描述
                variables: {}   # 用例变量
                httpsteps:  # http请求列表（操作步骤，一条用例含一个或多个http请求）
                    -
                        name: 登录平台      # 测试步骤名称
                        protocol:           # 协议，为空时使用全局参数
                        ip:                 # ip或servername
                        port:               # 端口
                        method: POST        # 请求方法
                        path: /login        # uri
                        params:             # 请求参数 ,exp:/query?name=wangwei
                            t: ${__timeStamp()}
                        body:               # 请求体，json或其他格式
                            username: ${username}   # 按照 “用例变量->套件变量->全局变量”的顺序查找变量定义
                            password: ${password}
                        extract:    # 提取器，从响应中提取数据给指定变量
                            ret: $.ret      # 变量存储在用例变量中
                            token: $.token
                        assertion:     # 断言，步骤执行成功或失败的判断条件
                            - eq:
                                  - status_code
                                  - 200
                            - eq:
                                  - ${ret}
                                  - 0
                    - name: 查询用户
                      protocol:
                      ip:
                      port:
                      method: GET
                      path: /query
                      params:
                          t: ${__timeStamp()}
                          token: ${token}
                      body:
                      extract:
                          ret: $.ret
                      assertion:
                          - eq:
                                - status_code
                                - 200
                          - eq:
                                - ${ret}
                                - 0
```