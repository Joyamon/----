"""
coding=utf-8
@author:周彦明
projectName:领筑云链自动化接口
time:2021-11-10
"""
import requests


def post(url, data, head):
    """
    重写post方法
    :param url: 请求url
    :param data: 请求数据
    :param head: 请求头
    :return: 响应信息
    """
    return requests.post(url=url, json=data, headers=head)


def get(url, params, head):
    """
    重写get方法
    :param url: 请求url
    :param params: 请求数据
    :param head: 请求头
    :return: 响应信息
    """
    return requests.get(url=url, params=params, headers=head)
