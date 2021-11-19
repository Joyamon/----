"""
coding=utf-8
@author:周彦明
projectName:领筑云链自动化接口
time:2021-11-10
"""
import yaml


def read_data(file):
    """
    读取yaml文件内容
    :param file: 读取目标文件
    :return:读取的数据
    """
    f = open(file, 'r', encoding='utf-8')
    data = yaml.load(f, Loader=yaml.SafeLoader)
    return data
