# pytest 执行方式
1. 打开Terminal，进入pytest.ini文件目录
```shell script
    cd /conf/
```
2. 执行pytest命令，执行测试用例后在该目录下生成report目录
```shell script
    pytest
```
3. 将json转为html
```shell script
    allure generate report/ -o report/html --clean
```
4. 打开报告
```shell script
    allure serve report/
```

# 基于minitest+pytest+unittest+allure框架
## minitest
### 框架依赖运行环境部署
1. 首先你要先下载框架压缩包
    https://git.weixin.qq.com/minitest/minium-doc/raw/master/minium/Python/dist/minium-0.0.2.zip
2. 打开微信开发者工具的安全模式
3. 安装Minium
```shell script
pip3 install minium-0.0.2.zip
```
### 使用
1. 通过命令行启动开发者工具提供了命令行
命令行通过命令行调用安装完成的工具可执行文件，完成登录、预览、上传、自动化测试等操作。调用返回码为 0 时代表正常，为 -1 时错误。
2. 命令行工具所在位置
- macOS: /Contents/MacOS/cli
- Windows: /cli.bat
3. 命令行启动工具
-o, --open `[projectpath]`: 打开工具，如果不带 projectpath，只是打开工具。
如果带 project path，则打开路径中的项目，每次执行都会自动编译刷新，并且自动打开模拟器和调试器。
projectpath 不能是相对路径。项目路径中必须含正确格式的 project.config.json 且其中有 appid 和 projectname 字段。
4. 示例
- 打开工具
  - cli -o
- 打开路径 /Users/username/demo 下的项目
  - cli -o /Users/username/demo
5. 命令
```
path/to/cli --auto /miniprogram/project/path --auto-port 9420
# path/to/cli 是命令行工具所在位置：
# macOS: <安装路径>/Contents/MacOS/cli
# Windows: <安装路径>/cli.bat windows版本在安装之后默认会把cli加入到系统路径，可以先测试cli命令是否可用，如果可用，path/to/cli可以直接用cli替换
# /miniprogram/project/path 是小程序工程的路径( Windows下面用 \\ 代替 \ )
```
6. tips
- --auto-port请填写 9420，不是开发者工具安全模式的端口
- 请确保开发者工具登陆的微信号具备被测小程序的开发者权限
- 如果没有Open project with automation enabled success的输出，否则请检查IDE版本（开发者工具调试基础库版本 >= 2.7.3），或者检查命令行参数

## pytest+unittest+allure
1. 安装依赖包
```
pip install -r requirements.txt
```
2. minitest默认支持unittest,且有良好的集成环境
3. pytest支持数据驱动更为合理
4. 集成allure进行测试报告的输出

## jenkins + allure
1. 目前简单做法，将allure报告发布到jenkins中，使用jenkins的allure插件查看本地报告
2. jenkins查看报告方法：
   - 查看报告路径 http://192.168.9.173:10800/job/M3_UI_TEST_REPORT/
   - 用户名 root
   - 密码 root123

