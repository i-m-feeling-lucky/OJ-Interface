# OJ Interface

在线面试平台代码运行接口部分

## 构建

在服务器中安装docker

使用Dockerfile 创建docker image，运行命令

    docker build -t ubuntugccpy:v2.0 .

默认带有简单前端界面用于测试，若不需要，请删除OJInterface/Interface/urls.py 中 `path('', views.index)`

若使用前端界面，需要安装相关依赖，运行命令

    cd static
    npm install

进入虚拟环境

    source ./env/bin/activate

运行django项目

    python manage.py runserver


## 接口说明

POST参数

- lang : [string] 代码所使用编程语言，限于c/cpp/python
- code : [string] 用户输入代码
- input : [string] 程序的输入

Response 参数

- message : [string] 返回代码运行信息，若代码能正常运行，则返回 "Run Success"，否则返回对应的错误，错误信息如下表。
- result : [string] 代码正常运行时返回程序输出结果，否则返回 "Error"

| message           |              meaning               |
| :---------------- | :--------------------------------: |
| Run Success       |            代码运行成功            |
| Time Limit Exceed |            程序运行超时            |
| Compile Error     | 程序编译错误，c/cpp/python均有可能 |
| Runtime Error     |     程序运行错误，c/cpp有可能      |
| System Error      |    系统错误，无法创建docker容器    |

## 参数修改

可修改参数有：（在 `./myapp/view.py` 文件 TODO 标志处修改）

- RUN_DIR: 临时文件文件夹，用于存放代码文件、输入文件、可执行文件，运行后自动删除
- TIME_LIMIT_C: c/cpp 程序运行时间限制
- TIME_LIMIT_PY: python 程序运行时间限制
