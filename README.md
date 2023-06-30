# playwright-ts

> 基于 playwright 和 pytest 单元测试框架的自动化项目

> 1、安装依赖


```
pip3 install pytest-playwright
pip3 install playwright
python3 -m playwright install  # 或者直接playwright install
--------------上面大家都要自己安装，下面是even环境，如果你在IDE打开有enev目录那么忽略下面步骤， even环境以及自动下载好所有依赖了
正常git拉下后上自带even环境的除非你用IDE打开时自己勾选没了以下是处理办法
1.创建虚拟环境
python3 -m venv even
2.激活虚拟环境：
在 macOS/Linux 上：
source even/bin/activate
在 Windows 上：
even\Scripts\activate
3.安装依赖项：
pip install -r requirements.txt

```


> 2、修改执行配置config.py文件



> 3、运行测试  python3 myRunner.py

> 4、查看报告 
> 
> allure报告：test_report找html文件
> 
> trace日志：python3 -m playwright show-trace trace.zip



