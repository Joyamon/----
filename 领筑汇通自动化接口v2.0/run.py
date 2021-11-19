"""
coding=utf-8
@author:周彦明
projectName:领筑云链自动化接口
time:2021-11-10
"""
import time
import unittest
from BeautifulReport import BeautifulReport as bf
from TestCase.testCases import Test
from TestCase.testCasesTickets import Tickets
from common.sendmail import new_file, send_mail
from common.settings import report_path

if __name__ == '__main__':
    # test = Test()
    now = time.strftime('%Y-%m-%d %H_%M_%S')
    filename = 'report-' + now + '.result.html'
    # 实例化测试套件
    suite = unittest.TestSuite()
    # loader = unittest.TestLoader()
    # 小于150W执行的用例
    tests_lt_150w = [Test('test_01_login'),
                     Test('test_02_01_get_domainUrl'),
                     Test('test_02_getUser'),
                     Test('test_03_01_createOrUpdate'),
                     Test('test_04_accountManagerLogin'),
                     Test('test_05_01_getProjectApplyUriAndTaskId'),
                     Test('test_05_accountManagerAudit'),
                     Test('test_06_riskControlManagerLogin'),
                     Test('test_07_01_getProjectApplyUriAndTaskId'),
                     Test('test_07_riskControlManagerAudit'),
                     Test('test_08_directorOfRiskControlLogin'),
                     Test('test_09_01_getProjectApplyUriAndTaskId'),
                     Test('test_09_directorOfRiskControlAudit'),
                     Test('test_10_generalManagerLogin'),
                     Test('test_11_01_getProjectApplyUriAndTaskId'),
                     Test('test_11_03_generalManagerAudit'),
                     Test('test_12_01_financialManagerLogin'),
                     Test('test_12_02_getProjectApplyUriAndTaskId'),
                     Test('test_12_03_financialManagerAudit'),
                     Test('test_12_04_update'),
                     Tickets('test_01_01_query_projectUrl'),
                     Tickets('test_01_createOrUpdate'),
                     Tickets('test_02_01_query_ticketApplyUri'),
                     Tickets('test_02_02_create'),
                     Tickets('test_02_03_audit'),
                     Tickets('test_03_01_query_ticketApplyUri'),
                     Tickets('test_03_02_query_info'),
                     Tickets('test_03_audit'),
                     Tickets('test_04_01_query_ticketApplyUri'),
                     Tickets('test_04_audit'),
                     Tickets('test_05_01_query_ticketApplyUri'),
                     Tickets('test_05_audit'),
                     Tickets('test_06_01_query_ticketApplyUri'),
                     Tickets('test_06_audit')
                     ]
    # 大于150W小于300W执行用例
    tests_lt_150w_and_gt_300w = [Test('test_01_login'),
                                 Test('test_02_01_get_domainUrl'),
                                 Test('test_02_getUser'),
                                 Test('test_03_01_createOrUpdate'),
                                 Test('test_04_accountManagerLogin'),
                                 Test('test_05_01_getProjectApplyUriAndTaskId'),
                                 Test('test_05_accountManagerAudit'),
                                 Test('test_06_riskControlManagerLogin'),
                                 Test('test_07_01_getProjectApplyUriAndTaskId'),
                                 Test('test_07_riskControlManagerAudit'),
                                 Test('test_08_directorOfRiskControlLogin'),
                                 Test('test_09_01_getProjectApplyUriAndTaskId'),
                                 Test('test_09_directorOfRiskControlAudit'),
                                 Test('test_10_generalManagerLogin'),
                                 Test('test_11_01_getProjectApplyUriAndTaskId'),
                                 Test('test_11_03_generalManagerAudit'),
                                 Test('test_12_01_financialManagerLogin'),
                                 Test('test_12_02_getProjectApplyUriAndTaskId'),
                                 Test('test_12_03_financialManagerAudit'),
                                 Test('test_13_01_financialDirectorLogin'),
                                 Test('test_13_02_getProjectApplyUriAndTaskId'),
                                 Test('test_13_03_financialDirectorAudit'),
                                 Test('test_13_04_update'),
                                 Tickets('test_01_01_query_projectUrl'),
                                 Tickets('test_01_createOrUpdate'),
                                 Tickets('test_02_01_query_ticketApplyUri'),
                                 Tickets('test_02_02_create'),
                                 Tickets('test_02_03_audit'),
                                 Tickets('test_03_01_query_ticketApplyUri'),
                                 Tickets('test_03_02_query_info'),
                                 Tickets('test_03_audit'),
                                 Tickets('test_04_01_query_ticketApplyUri'),
                                 Tickets('test_04_audit'),
                                 Tickets('test_05_01_query_ticketApplyUri'),
                                 Tickets('test_05_audit'),
                                 Tickets('test_06_01_query_ticketApplyUri'),
                                 Tickets('test_06_audit')
                                 ]
    # 大于300W 执行用例
    tests_gt_300W = [Test('test_01_login'),
                     Test('test_02_01_get_domainUrl'),
                     Test('test_02_getUser'),
                     Test('test_03_01_createOrUpdate'),
                     Test('test_04_accountManagerLogin'),
                     Test('test_05_01_getProjectApplyUriAndTaskId'),
                     Test('test_05_accountManagerAudit'),
                     Test('test_06_riskControlManagerLogin'),
                     Test('test_07_01_getProjectApplyUriAndTaskId'),
                     Test('test_07_riskControlManagerAudit'),
                     Test('test_08_directorOfRiskControlLogin'),
                     Test('test_09_01_getProjectApplyUriAndTaskId'),
                     Test('test_09_directorOfRiskControlAudit'),
                     Test('test_10_generalManagerLogin'),
                     Test('test_11_01_getProjectApplyUriAndTaskId'),
                     Test('test_11_03_generalManagerAudit'),
                     Test('test_12_01_financialManagerLogin'),
                     Test('test_12_02_getProjectApplyUriAndTaskId'),
                     Test('test_12_03_financialManagerAudit'),
                     Test('test_12_04_update'),
                     Test('test_13_01_financialDirectorLogin'),
                     Test('test_13_02_getProjectApplyUriAndTaskId'),
                     Test('test_13_03_financialDirectorAudit'),
                     Test('test_13_04_update'),
                     Test('test_14_01_presidentLogin'),
                     Test('test_14_02_getProjectApplyUriAndTaskId'),
                     Test('test_14_03_presidentAudit'),
                     Test('test_14_04_update'),
                     Tickets('test_01_01_query_projectUrl'),
                     Tickets('test_01_createOrUpdate'),
                     Tickets('test_02_01_query_ticketApplyUri'),
                     Tickets('test_02_02_create'),
                     Tickets('test_02_03_audit'),
                     Tickets('test_03_01_query_ticketApplyUri'),
                     Tickets('test_03_02_query_info'),
                     Tickets('test_03_audit'),
                     Tickets('test_04_01_query_ticketApplyUri'),
                     Tickets('test_04_audit'),
                     Tickets('test_05_01_query_ticketApplyUri'),
                     Tickets('test_05_audit'),
                     Tickets('test_06_01_query_ticketApplyUri'),
                     Tickets('test_06_audit')
                     ]
    # 将Test类下的所有用例添加到测试套件
    suite.addTests(tests_gt_300W)
    result = bf(suite)
    result.report(description='自动化接口测试报告', filename=filename, report_dir='./report')
    new_report = new_file(report_path)# 获取最新报告文件
    send_mail(new_report)  # 发送最新的测试报告
