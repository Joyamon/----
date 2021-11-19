"""
coding=utf-8
@author:周彦明
projectName:领筑云链自动化接口
time:2021-11-10
"""
import logging
import os


def dirname(fileName='', filepath='Data'):
    """
    :param fileName: 文件名字
    :param filepath: 写入指定目录
    :return:
    """
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), filepath, fileName)


def makelogs(log_content):
    """
    定义log日志级别
    :param log_content:
    :return:
    """
    # 定义日志文件
    logFile = logging.FileHandler(dirname('log.txt', 'log'), 'a', encoding='utf-8')
    # 设置log格式
    fmt = logging.Formatter(
        fmt='%(asctime)s-%(name)s-%(levelname)s-%(lineno)s-%(module)s:%(message)s')
    logFile.setFormatter(fmt)
    logger1 = logging.Logger('logTest', level=logging.INFO)  # 定义日志
    logger1.addHandler(logFile)
    logger1.info(log_content)
    logFile.close()
