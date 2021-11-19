"""
coding=utf-8
@author:周彦明
projectName:领筑云链自动化接口
time:2021-11-10
"""
import requests
from common.readYaml import read_data
from common.settings import base_path

#
# def get_token(self, data_path, save_path):
#     """
#     获取登录的token
#     """
#     data = read_data(base_path + data_path)
#     res = requests.post(url=self.url + data['url'], params=data['payloads'])
#     access_token = res.json()['result']['access_token']
#     headers = access_token
#     print(res.text)
#
#     # 将读取的 companyToken，loginToken写入headers文件中
#     file = open(base_path + save_path, 'w', encoding='utf-8')
#     file.write(headers)
