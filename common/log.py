import os
import logging

# 日志目录
log_dir = "/Users/zhangpc/IdeaProjects/playwright-pytest-demo/log/"
os.makedirs(log_dir, exist_ok=True)

# 创建日志记录器
logger = logging.getLogger("my_logger")
logger.setLevel(logging.DEBUG)

# 创建文件处理程序
log_file = os.path.join(log_dir, "2023-05-25--10_42_20.log")
fh = logging.FileHandler(log_file, 'a', encoding='utf-8')
fh.setLevel(logging.DEBUG)

# 创建控制台处理程序
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# 定义日志格式
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 添加处理程序到日志记录器
logger.addHandler(fh)
logger.addHandler(ch)

# 测试日志记录
logger.info("开始测试✨✨✨！")
