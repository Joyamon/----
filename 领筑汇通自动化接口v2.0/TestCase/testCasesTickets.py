"""
coding=utf-8
@author:周彦明
projectName:领筑云链自动化接口
time:2021-11-10
"""

import random
import unittest
import requests
from faker import Faker
from TestCase.testCases import Test
from common.readYaml import read_data
from common.settings import base_path
from log.makelog import makelogs


class Tickets(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test = Test()
        cls.head = None
        cls.projectUri = None
        # 客户经理
        cls.khjlticketApplyUri = None
        cls.khjlcurrentTaskId = None
        cls.khjlprojectName = None
        # 风控经理
        cls.fkjlticketApplyUri = None
        cls.fkjlcurrentTaskId = None
        cls.fkjlprojectName = None
        cls.projectNum = None
        cls.applicantName = None
        cls.projectName = None
        # 风控总监
        cls.fkzjticketApplyUri = None
        cls.fkzjcurrentTaskId = None
        # 总经理
        cls.zjlticketApplyUri = None
        cls.zjlcurrentTaskId = None
        # 财务经理
        cls.cwjlticketApplyUri = None
        cls.cwjlcurrentTaskId = None

    @classmethod
    def tearDownClass(cls):
        pass

    def test_01_01_query_projectUrl(self):
        """
        查询授信管理projectUrl
        :return:
        """
        Tickets.head = {'token': self.test.access_token}
        params = f'currentPage=1&flowableStatus=3&pageSize=10&searchWord=&domainUri={self.test.domainUrl}'
        data = read_data(base_path + '/Data/15_createTickets/queryProjectUrl.yaml')
        res = requests.get(url=self.test.url + data['url'], params=params, headers=self.head)
        Tickets.projectUri = res.json()['result']['records'][0]['projectUri']

    def test_01_createOrUpdate(self):
        """
        创建商票
        :return:
        """
        fake = Faker(locale='zh_CN')
        account = fake.credit_card_number()
        payloads = {"attachments": [{"category": 1, "title": "采购合同", "note": "", "files": []},
                                    {"category": 2, "title": "送/收货单", "note": "", "files": []},
                                    {"category": 3, "title": "增值税发票", "note": "", "files": []},
                                    {"category": 4, "title": "其他", "note": "", "files": []}],
                    "companyInfo": {"companyName": fake.company_prefix(), "contractFlag": 'true',
                                    "contractValidityDate": "2023-11-16"},
                    "paymentMode": "",
                    "paymentSource": "[{\"type\":1,\"value\":\"自行筹措，到期付款\"}]",
                    "projectUri": self.projectUri,
                    "status": 2,
                    "ticketInfo": {"companyName": fake.company_prefix(), "contactPhone": fake.phone_number(),
                                   "contactName": fake.name(),
                                   "address": fake.address(), "bankName": "平安银行马家龙支行", "bankCode": "4564556",
                                   "account": account, "amount": self.test.applyMoney,
                                   "marginAmount": random.randint(100, 999),
                                   "isTransfer": 1, "validityDate": "2023-11-16"},
                    "userInfo": {"name": self.test.name, "userNum": self.test.userNum, "idcardNo": self.test.idcardNo,
                                 "mobile": self.test.mobile, "userName": ""},
                    "explains": "", "domainUri": self.test.domainUrl,
                    "ticketApplyUri": ""}
        data = read_data(base_path + '/Data/15_createTickets/createOrUpdate.yaml')
        res = requests.post(url=self.test.url + data['url'], json=payloads, headers=self.head)
        self.assertEqual(res.json()['message'], 'success', msg='商票申请失败')
        makelogs('商票申请成功，响应信息为：' + res.json()['message'])

    def test_02_01_query_ticketApplyUri(self):
        """
        查询客户经理的ticketApplyUri
        :return:
        """
        head = {'token': self.test.accountManagerToken}
        params = f'currentPage=1&pageSize=10&searchWord=&domainUri={self.test.domainUrl}&status=5'
        data = read_data(base_path + '/Data/16_accountManagerAuditTickets/queryTicketApplyUri.yaml')
        res = requests.get(url=self.test.url + data['url'], params=params, headers=head)
        Tickets.khjlticketApplyUri = res.json()['result']['records'][0]['ticketApplyUri']
        Tickets.khjlcurrentTaskId = res.json()['result']['records'][0]['currentTaskId']
        Tickets.khjlprojectName = res.json()['result']['records'][0]['projectName']

    def test_02_02_create(self):
        """
        客户经理create
        :return:
        """
        fake = Faker(locale='zh_CN')
        head = {'token': self.test.accountManagerToken}
        payloads = {"amount": random.uniform(10000, 9999), "attachment": {"category": 1, "files": []},
                    "chargeName": "咨询服务费", "chargeType": 3,
                    "payUser": fake.name(), "ticketApplyUri": self.khjlticketApplyUri}
        data = read_data(base_path + '/Data/16_accountManagerAuditTickets/create.yaml')
        res = requests.post(url=self.test.url + data['url'], json=payloads, headers=head)
        self.assertEqual(res.json()['message'], 'success', msg='客户经理create失败')
        makelogs('客户经理create成功，响应信息为：' + res.json()['message'])

    def test_02_03_audit(self):
        """
        客户经理audit
        :return:
        """
        head = {'token': self.test.accountManagerToken}
        payloads = {
            "extend": "{\"tableData\":[{\"chargeName\":\"咨询服务费\",\"amount\":455,\"chargeType\":3,\"attachment\":{\"category\":1,\"files\":[]},\"payUser\":\"撒反对\"}],\"adviceTable\":{},\"remarks\":\"\"}",
            "flag": 0, "roleFlag": 1, "upFiles": [], "ticketApplyUri": self.khjlticketApplyUri,
            "taskId": self.khjlcurrentTaskId, "domainUri": self.test.domainUrl,
            "projectName": self.khjlprojectName}
        data = read_data(base_path + '/Data/16_accountManagerAuditTickets/audit.yaml')
        res = requests.post(url=self.test.url + data['url'], json=payloads, headers=head)
        self.assertEqual(res.json()['message'], 'success', msg='客户经理audit失败')
        makelogs('客户经理audit成功，响应信息为：' + res.json()['message'])

    def test_03_01_query_ticketApplyUri(self):
        """
        查询风控经理的ticketApplyUri和taskId
        :return:
        """
        head = {'token': self.test.riskControlManagerToken}
        params = f'currentPage=1&pageSize=10&searchWord=&domainUri={self.test.domainUrl}&status=5'
        data = read_data(base_path + '/Data/17_riskControlManagerAuditTickets/queryTicketApplyUri.yaml')
        res = requests.get(url=self.test.url + data['url'], params=params, headers=head)
        Tickets.fkjlticketApplyUri = res.json()['result']['records'][0]['ticketApplyUri']
        Tickets.fkjlcurrentTaskId = res.json()['result']['records'][0]['currentTaskId']
        Tickets.fkjlprojectName = res.json()['result']['records'][0]['projectName']

    def test_03_02_query_info(self):
        """
        获取风控经理请求参数
        :return:
        """
        head = {'token': self.test.riskControlManagerToken}
        params = f'currentPage=1&pageSize=10&searchWord=&domainUri={self.test.domainUrl}&status=5'
        data = read_data(base_path + '/Data/17_riskControlManagerAuditTickets/queryInfo.yaml')
        res = requests.get(url=self.test.url + data['url'], params=params, headers=head)
        Tickets.projectNum = res.json()['result']['records'][0]['projectNum']
        Tickets.applicantName = res.json()['result']['records'][0]['applicantName']
        Tickets.projectName = res.json()['result']['records'][0]['projectName']

    def test_03_audit(self):
        """
        风控经理audit
        :return:
        """
        head = {'token': self.test.riskControlManagerToken}
        payloads = {
            "extend": "{\"tableData\":[],\"adviceTable\":{\"projectName\":\"'" + self.projectName + "'\",\"projectNum\":\"'" + self.projectNum + "'\",\"userInfoName\":\"'" + self.applicantName + "'\",\"beforeDay\":\"12\",\"afterDay\":730,\"year\":\"2023\",\"month\":\"11\",\"day\":\"16\",\"drawBillName\":\"惠派国际公司\",\"getBillName\":\"趋势\",\"getBillAccount\":\"5298234642479955\",\"getBillDepositBank\":\"平安银行马家龙支行\",\"getBillBankNumber\":\"4564556\",\"voucherName\":\"\",\"voucherAddress\":\"\",\"voucherDate\":\"\",\"money\":\"55566\",\"moneyCapital\":\"伍万伍仟伍佰陆拾陆元整\",\"acceptName\":\"惠派国际公司\",\"contractNum\":\"\",\"acceptInfo\":\"\",\"isTransfer\":1,\"voucherName2\":\"\",\"voucherAddress2\":\"\",\"voucherDate2\":\"\",\"gradeBillPerson\":\"\",\"gradeTheme1\":\"\",\"gradelevel1\":\"\",\"gradeDate1\":\"\",\"gradeAcceptPerson\":\"\",\"gradeTheme2\":\"\",\"gradelevel2\":\"\",\"gradeDate2\":\"\"},\"remarks\":\"\"}",
            "flag": 0, "roleFlag": 2, "upFiles": [], "ticketApplyUri": self.fkjlticketApplyUri,
            "taskId": self.fkjlcurrentTaskId, "domainUri": self.test.domainUrl,
            "projectName": self.projectName}
        data = read_data(base_path + '/Data/17_riskControlManagerAuditTickets/audit.yaml')
        res = requests.post(url=self.test.url + data['url'], json=payloads, headers=head)
        self.assertEqual(res.json()['message'], 'success', msg='风控经理audit失败')
        makelogs('风控经理audit成功，响应信息为：' + res.json()['message'])

    def test_04_01_query_ticketApplyUri(self):
        """
        查询风控总监的ticketApplyUri
        :return:
        """
        head = {'token': self.test.directorOfRiskControlToken}
        params = f'currentPage=1&pageSize=10&searchWord=&domainUri={self.test.domainUrl}&status=5'
        data = read_data(base_path + '/Data/18_directorOfRiskAuditTickets/queryTicketApplyUri.yaml')
        res = requests.get(url=self.test.url + data['url'], params=params, headers=head)
        Tickets.fkzjticketApplyUri = res.json()['result']['records'][0]['ticketApplyUri']
        Tickets.fkzjcurrentTaskId = res.json()['result']['records'][0]['currentTaskId']

    def test_04_audit(self):
        """
        风控总监audit
        :return:
        """
        head = {'token': self.test.directorOfRiskControlToken}
        payloads = {
            "extend": "{\"tableData\":[],\"adviceTable\":{\"projectName\":\"'" + self.projectName + "'\",\"projectNum\":\"'" + self.projectNum + "'\",\"userInfoName\":\"'" + self.applicantName + "'\",\"beforeDay\":\"12\",\"afterDay\":730,\"year\":\"2023\",\"month\":\"11\",\"day\":\"16\",\"drawBillName\":\"惠派国际公司\",\"getBillName\":\"趋势\",\"getBillAccount\":\"5298234642479955\",\"getBillDepositBank\":\"平安银行马家龙支行\",\"getBillBankNumber\":\"4564556\",\"voucherName\":\"\",\"voucherAddress\":\"\",\"voucherDate\":\"\",\"money\":\"55566\",\"moneyCapital\":\"伍万伍仟伍佰陆拾陆元整\",\"acceptName\":\"惠派国际公司\",\"contractNum\":\"\",\"acceptInfo\":\"\",\"isTransfer\":1,\"voucherName2\":\"\",\"voucherAddress2\":\"\",\"voucherDate2\":\"\",\"gradeBillPerson\":\"\",\"gradeTheme1\":\"\",\"gradelevel1\":\"\",\"gradeDate1\":\"\",\"gradeAcceptPerson\":\"\",\"gradeTheme2\":\"\",\"gradelevel2\":\"\",\"gradeDate2\":\"\"},\"remarks\":\"\"}",
            "flag": 0, "roleFlag": 3, "upFiles": [], "ticketApplyUri": self.fkzjticketApplyUri,
            "taskId": self.fkzjcurrentTaskId, "domainUri": self.test.domainUrl,
            "projectName": self.projectName}
        data = read_data(base_path + '/Data/18_directorOfRiskAuditTickets/audit.yaml')
        res = requests.post(url=self.test.url + data['url'], json=payloads, headers=head)
        self.assertEqual(res.json()['message'], 'success', msg='风控总监audit失败')
        makelogs('风控总监audit成功，响应信息为：' + res.json()['message'])

    def test_05_01_query_ticketApplyUri(self):
        """
        查询总经理ticketApplyUri
        :return:
        """
        head = {'token': self.test.generalManagerToken}
        params = f'currentPage=1&pageSize=10&searchWord=&domainUri={self.test.domainUrl}&status=5'
        data = read_data(base_path + '/Data/19_generalManagerAuditTickets/queryTicketApplyUri.yaml')
        res = requests.get(url=self.test.url + data['url'], params=params, headers=head)
        Tickets.zjlticketApplyUri = res.json()['result']['records'][0]['ticketApplyUri']
        Tickets.zjlcurrentTaskId = res.json()['result']['records'][0]['currentTaskId']

    def test_05_audit(self):
        """
        总经理audit
        :return:
        """
        head = {'token': self.test.generalManagerToken}
        payloads = {
            "extend": "{\"tableData\":[],\"adviceTable\":{\"projectName\":\"'" + self.projectName + "'\",\"projectNum\":\"'" + self.projectNum + "'\",\"userInfoName\":\"'" + self.applicantName + "'\",\"beforeDay\":\"12\",\"afterDay\":730,\"year\":\"2023\",\"month\":\"11\",\"day\":\"16\",\"drawBillName\":\"惠派国际公司\",\"getBillName\":\"趋势\",\"getBillAccount\":\"5298234642479955\",\"getBillDepositBank\":\"平安银行马家龙支行\",\"getBillBankNumber\":\"4564556\",\"voucherName\":\"\",\"voucherAddress\":\"\",\"voucherDate\":\"\",\"money\":\"55566\",\"moneyCapital\":\"伍万伍仟伍佰陆拾陆元整\",\"acceptName\":\"惠派国际公司\",\"contractNum\":\"\",\"acceptInfo\":\"\",\"isTransfer\":1,\"voucherName2\":\"\",\"voucherAddress2\":\"\",\"voucherDate2\":\"\",\"gradeBillPerson\":\"\",\"gradeTheme1\":\"\",\"gradelevel1\":\"\",\"gradeDate1\":\"\",\"gradeAcceptPerson\":\"\",\"gradeTheme2\":\"\",\"gradelevel2\":\"\",\"gradeDate2\":\"\"},\"remarks\":\"\"}",
            "flag": 0, "roleFlag": 4, "upFiles": [], "ticketApplyUri": self.zjlticketApplyUri,
            "taskId": self.zjlcurrentTaskId, "domainUri": self.test.domainUrl,
            "projectName": self.projectName}
        data = read_data(base_path + '/Data/19_generalManagerAuditTickets/audit.yaml')
        res = requests.post(url=self.test.url + data['url'], json=payloads, headers=head)
        self.assertEqual(res.json()['message'], 'success', msg='总经理audit失败')
        makelogs('总经理audit成功，响应信息为：' + res.json()['message'])

    def test_06_01_query_ticketApplyUri(self):
        """
        查询财务经理ticketApplyUri
        :return:
        """
        head = {'token': self.test.financialManagerToken}
        params = f'currentPage=1&pageSize=10&searchWord=&domainUri={self.test.domainUrl}&status=5'
        data = read_data(base_path + '/Data/20_financialManagerAuditTicket/queryTicketApplyUri.yaml')
        res = requests.get(url=self.test.url + data['url'], params=params, headers=head)
        Tickets.cwjlticketApplyUri = res.json()['result']['records'][0]['ticketApplyUri']
        Tickets.cwjlcurrentTaskId = res.json()['result']['records'][0]['currentTaskId']

    def test_06_audit(self):
        """
        财务经理audit
        :return:
        """
        head = {'token': self.test.financialManagerToken}
        payloads = {
            "extend": "{\"tableData\":[],\"adviceTable\":{\"projectName\":\"'" + self.projectName + "'\",\"projectNum\":\"'" + self.projectNum + "'\",\"userInfoName\":\"'" + self.applicantName + "'\",\"beforeDay\":\"12\",\"afterDay\":730,\"year\":\"2023\",\"month\":\"11\",\"day\":\"16\",\"drawBillName\":\"惠派国际公司\",\"getBillName\":\"趋势\",\"getBillAccount\":\"5298234642479955\",\"getBillDepositBank\":\"平安银行马家龙支行\",\"getBillBankNumber\":\"4564556\",\"voucherName\":\"\",\"voucherAddress\":\"\",\"voucherDate\":\"\",\"money\":\"55566\",\"moneyCapital\":\"伍万伍仟伍佰陆拾陆元整\",\"acceptName\":\"惠派国际公司\",\"contractNum\":\"\",\"acceptInfo\":\"\",\"isTransfer\":1,\"voucherName2\":\"\",\"voucherAddress2\":\"\",\"voucherDate2\":\"\",\"gradeBillPerson\":\"\",\"gradeTheme1\":\"\",\"gradelevel1\":\"\",\"gradeDate1\":\"\",\"gradeAcceptPerson\":\"\",\"gradeTheme2\":\"\",\"gradelevel2\":\"\",\"gradeDate2\":\"\"},\"remarks\":\"\"}",
            "flag": 0, "roleFlag": 5, "upFiles": [], "ticketApplyUri": self.cwjlticketApplyUri,
            "taskId": self.cwjlcurrentTaskId, "domainUri": self.test.domainUrl,
            "projectName": self.projectName}
        data = read_data(base_path + '/Data/20_financialManagerAuditTicket/audit.yaml')
        res = requests.post(url=self.test.url + data['url'], json=payloads, headers=head)
        self.assertEqual(res.json()['message'], 'success', msg='财务经理audit失败')
        makelogs('财务经理audit成功，响应信息为：' + res.json()['message'])


if __name__ == '__main__':
    unittest.main()
