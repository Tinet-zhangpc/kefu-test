from common.config import *

"""
运行测试配置
"""


class RunConfig:

    # 运行测试用例的目录或文件-登录授权
    cases_path = os.path.join(case_path, "test_kefu_login.py")
    # 运行测试用例的目录或文件-基础会话
    # cases_path = os.path.join(case_path, "test_kefu_session.py")
    # 运行测试用例的目录或文件-基础会话-基础其他
    # cases_path = os.path.join(case_path, "test_session_other.py")
    # 单元测试
    # cases_path = os.path.join(case_path, "test_baidu.py")

    # 配置浏览器驱动类型(chromium, firefox, webkit)。
    browser = "chromium"

    # 运行模式（headless, headful）
    # mode = "headless"
    mode = "headful"

    # 配置运行的 URL
    baseUrl = "http://sandbox.kefu.easemob.com/"

    # 失败重跑次数
    rerun = "0"

    # 当达到最大失败数，停止执行
    max_fail = "5"

    # 报告路径（不需要修改）
    NEW_REPORT = None
