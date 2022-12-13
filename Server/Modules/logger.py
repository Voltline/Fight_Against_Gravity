import logging
import time
import os

"""
日志记录器
记录格式 y-m-d h-m-s,ms LEVEL:info
可以选择日志记录在文件/控制台/文件和控制台
可以选择记录目录，会自动在目录下生成/log/[time.time].log文件中记录
可选择日志记录等级，仅大于等于该等级的日志消息会被记录，DEBUG会记录所有消息
"""


# logging.basicConfig(format='%(asctime)s|[%(levelname)s]%(message)s',level=logging.DEBUG)


class Flogger:
    FILE = 1
    """仅在文件记录"""
    CONSOLE = 2
    """仅在控制台输出"""
    FILE_AND_CONSOLE = 3
    """同时记录在控制台和文件"""
    L_DEBUG = logging.DEBUG
    L_INFO = logging.INFO
    L_WARNING = logging.WARNING
    L_ERROR = logging.ERROR
    L_CRITICAL = logging.CRITICAL

    def __init__(self, models, logpath=None, level=logging.INFO):
        """
        models:记录模式,FILE,CONSOLE,FILE_AND_CONSOLE
        logpath:日志记录的根目录，默认工作目录
        level:日志记录等级，顺序为DEBUG,INFO,WARNING,ERROR,CRITICAL,默认INFO
        """
        self.logger = logging.getLogger("Fight Against Gravity logger")
        self.form = logging.Formatter('{asctime} {levelname:>8}: {message}', style='{')
        if models & self.FILE:
            #用户未指定目录默认工作目录
            filename = str(int(time.time())) + ".log"
            #TODO：filename
            if logpath is None:
                logpath = os.path.dirname(os.path.realpath(__file__))
                logpath = os.path.dirname(logpath)
            self.path = logpath + "/logs/"
            print(self.path)
            # 检查目录是否存在
            if not os.path.exists(self.path):
                # 如果目录不存在，创建它
                os.makedirs(self.path)
            file_handler = logging.FileHandler(self.path)
            file_handler.setFormatter(self.form)
            self.logger.addHandler(file_handler)
        if models & self.CONSOLE:
            con_handler = logging.StreamHandler()
            con_handler.setFormatter(self.form)
            self.logger.addHandler(con_handler)
        self.logger.setLevel(level)

    def debug(self, msg: str):
        self.logger.debug(msg)

    def info(self, msg: str):
        self.logger.info(msg)

    def warning(self, msg: str):
        self.logger.info(msg)

    def error(self, msg: str):
        self.logger.error(msg)

    def critical(self, msg: str):
        self.logger.critical(msg)


if __name__ == "__main__":
    logger = Flogger(Flogger.FILE, logpath=".", level=Flogger.L_DEBUG)
    logger.debug("debug")
    # time.sleep(1)
    logger.info("info")
    # time.sleep(1)
    logger.warning("warning")
    # time.sleep(1)
    logger.error("error")
    # time.sleep(1.1)
    logger.critical("critical")
