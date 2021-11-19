"""
coding=utf-8
@author:周彦明
projectName:领筑云链自动化接口
time:2021-11-10
"""
import os

"""
os.sep：一般在在Windows上，文件的路径分隔符是'\'，在Linux上是'/'。
使用os.sep可以根据你所处的平台，自动采用相应的分隔符号。
"""
# 全局路由
base_path1 = os.path.abspath(os.path.join(os.path.dirname(__file__), '../'))
base_path = base_path1.replace(r'\/'.replace(os.sep, ''), os.sep)
# report 文件路由
report_path1 = os.path.join(base_path,'report')
report_path = report_path1.replace(r'\/'.replace(os.sep, ''), os.sep)



