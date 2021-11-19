"""
coding=utf-8
@author:周彦明
projectName:领筑云链自动化接口
time:2021-11-10
"""
import random
import time
import unittest
import warnings
import requests
from common.readYaml import read_data
from common.settings import base_path
from faker import Faker
from log.makelog import makelogs


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        warnings.simplefilter('ignore', ResourceWarning)
        cls.domain = read_data(base_path + '/common/domain.yaml')
        # "修改环境路由"
        cls.url = cls.domain['uat_url']
        cls.now_time = time.strftime("%Y-%m-%d", time.localtime())
        cls.access_token = None
        cls.user_id = None
        cls.domainUrl = None
        cls.censusRegion = None
        cls.nativeRegion = None
        # 客户号
        cls.userNum = None
        cls.head = None
        cls.name = None
        cls.idcardNo = None
        cls.mobile = None
        cls.accountManagerToken = None
        cls.kh_projectApplyUri = None
        cls.kh_taskId = None
        # 风控经理的登录token
        cls.riskControlManagerToken = None
        cls.fk_projectApplyUri = None
        cls.fk_taskId = None
        # 风控总监的登录token
        cls.directorOfRiskControlToken = None
        cls.fkzj_projectApplyUri = None
        cls.fkzj_taskId = None
        # 总经理的登录token
        cls.generalManagerToken = None
        cls.zjl_projectApplyUri = None
        cls.zjl_taskId = None
        # 财务经理的登录token
        cls.financialManagerToken = None
        cls.cwjl_projectApplyUri = None
        cls.cwjl_taskId = None
        # 财务总监的登录token
        cls.financialDirectorToken = None
        cls.cwzj_projectApplyUri = None
        cls.cwzj_taskId = None
        # 总裁的登录token
        cls.presidentToken = None
        cls.zc_projectApplyUri = None
        cls.zc_taskId = None
        cls.lt_150W = 16000
        cls.gt_300W_and_lt_150W = 2000000
        cls.gt_300W = 3600000
        cls.applyMoney = cls.gt_300W

    @classmethod
    def tearDownClass(cls):
        pass

    def test_01_login(self):
        """
        登录
        :return:
        """
        data = read_data(base_path + '/Data/1_login_user/login_user.yaml')
        res = requests.post(url=self.url + data['url'], params=data['payloads'])
        Test.access_token = res.json()['result']['access_token']
        Test.user_id = res.json()['result']['user_id']

    def test_02_01_get_domainUrl(self):
        """
        获取domainUrl 作为getUser的请求参数
        :return:
        """
        data = read_data(base_path + '/Data/2_fileManagement/get_domainUrl.yaml')
        head = {'token': self.access_token}
        res = requests.get(url=self.url + data['url'], headers=head)
        Test.domainUrl = res.json()['result']['userDomainList'][0]['fkDomain']
        Test.censusRegion = res.json()['result']['userDomainList'][1]['censusRegion']
        Test.nativeRegion = res.json()['result']['userDomainList'][1]['nativeRegion']

    def test_02_getUser(self):
        """
        获取客户号
        :return:
        """
        data = read_data(base_path + '/Data/2_fileManagement/getUser.yaml')
        Test.head = {'Accept': 'application/json, text/plain, */*',
                     'Accept-Encoding': 'gzip, deflate',
                     'Accept-Language': 'zh-CN,zh;q=0.9',
                     'Connection': 'keep-alive',
                     'Host': 'uat.eco.lingzhuyun.com:30101',
                     'Origin': 'http://uat.eco.lingzhuyun.com:7080',
                     'Referer': 'http://uat.eco.lingzhuyun.com:7080/',
                     'token': self.access_token}
        payloads = self.domainUrl
        res = requests.get(url=self.url + data['url'], params=payloads, headers=Test.head)
        Test.userNum = res.json()['result']['personalInfo']['userNum']
        Test.name = res.json()['result']['authenticationInfo']['name']
        Test.idcardNo = res.json()['result']['authenticationInfo']['idcardNo']
        Test.mobile = res.json()['result']['personalInfo']['mobile']

    def test_03_01_createOrUpdate(self):
        """
        授信申请
        :return:
        """
        fake = Faker(locale='zh_CN')
        data = read_data(base_path + '/Data/3_creditApplication/createOrUpdate.yaml')
        payloads = {"userInfo": {"name": self.name, "userNum": self.userNum, "idcardNo": self.idcardNo,
                                 "mobile": self.mobile, "userName": '', "nativeRegion": self.nativeRegion,
                                 "censusRegion": self.censusRegion, "cooperationYears": 4,
                                 "userRemarks": "{\"a1\":1,\"a4\":1,\"a5\":1,\"a7\":1}"},
                    "projectInfo": {"num": 'xmbh' + fake.phone_number(), "projectName": fake.street_name() + "项目",
                                    "partnerName": fake.company_prefix(),
                                    "beginDate": self.now_time, "endDate": "2022-12-21",
                                    "process": round(random.uniform(1, 100), 2),
                                    "ownerName": fake.name(), "managerName": fake.name(),
                                    "managerPhone": fake.phone_number(),
                                    "cooperationAmount": random.randint(1111111, 9999999),
                                    "insuranceType": "[{\"type\":1,\"value\":\"团体意外险\"}]",
                                    "reportNum": 'xmbbbh' + fake.phone_number()},
                    "paySource": "[{\"type\":1,\"value\":\"自行筹措，到期还款\"}]",
                    "applyAmount": random.randint(111111, 999999),
                    "businessType": "[{\"type\":1,\"value\":\"开商票\"}]",
                    "purpose": "[{\"type\":1,\"value\":\"支付材料款\"},{\"type\":2,\"value\":\"支付人工费\"}]", "attachments": [
                {"category": 1, "title": "身份证（正、反面）", "note": "验原件、留电子扫描件", "files": [
                    {"name": "批量导入—个人.xlsx", "streamid": "jsi_at1636165307546274",
                     "url": "https://ucfileserver-test.obs.cn-south-1.myhuaweicloud.com:443/jsi_at1636165307546274?AWSAccessKeyId=VGODQRABKWVSUQWW4YJC&Expires=1793845307&Signature=QgFuDKniGmdQMD0pX0PhZJVGalU%3D"}],
                 "attachmentCategoryUri": "e38b1851dddbc9e4c7ae5ed46217d725", "type": 1, "status": 1},
                {"category": 2, "title": "户口本（户主页和本人页）", "note": "验原件、留电子扫描件", "files": [],
                 "attachmentCategoryUri": "53849576b586293aa5a82c1c5d6b5dd6", "type": 1, "status": 0},
                {"category": 3, "title": "结婚证/离婚证", "note": "验原件、留电子扫描件", "files": [],
                 "attachmentCategoryUri": "5c2f556a7beaab6eea65e5de62f4526c", "type": 1, "status": 0},
                {"category": 4, "title": "配偶身份证（正、反面）", "note": "验原件、留电子扫描件", "files": [],
                 "attachmentCategoryUri": "8ed3d86037d87fb345302236e720501a", "type": 1, "status": 0},
                {"category": 5, "title": "配偶户口本（户主页和本人页）", "note": "验原件、留电子扫描件", "files": [],
                 "attachmentCategoryUri": "b216caa9f7abf08262b5d6fa7adef4f9", "type": 1, "status": 0},
                {"category": 6, "title": "本人工资、工程结算、销售收付等主要银行账户近1年银行流水（excel版）",
                 "note": "1.从网上银行直接下载excel电子版，部分不支持查询近一年流水的银行，可提交纸质版银行流水；<br/>2.通过配偶账户走账的，提供配偶银行流水", "files": []},
                {"category": 7, "title": "个人及配偶人行征信报告（两个月内有效）", "note": "1.累计申请授信金额50万（不含）以上需提交的资料<br/>2.验原件，留电子扫描件",
                 "files": []},
                {"category": 8, "title": "本人及配偶名下房产证", "note": "1.累计申请授信金额50万（不含）以上需提交的资料<br/>2.验原件，留电子扫描件",
                 "files": []},
                {"category": 9, "title": "本人及配偶名下车辆行使证", "note": "1.累计申请授信金额50万（不含）以上需提交的资料<br/>2.验原件，留电子扫描件",
                 "files": []}, {"category": 10, "title": "《授信申请书》", "note": "原件（可提供已签名加盖指纹的扫描件，原件放款前后补）", "files": []},
                {"category": 11, "title": "《项目合同》关键页",
                 "note": "1.授信项目的合同的电子扫描件；<br/>2.关键页至少应包含基础条款（专用条款）、支付条款和双方签字盖章页；<br/>3.如工程SaaS系统中合同扫描件符合上述要求，可不用重复提供。",
                 "files": []},
                {"category": 12, "title": "《项目台账》", "note": "1.提交excel电子版；<br/>2.所有300万元以上在建项目的总台账，根据提供的格式填写",
                 "files": []},
                {"category": 13, "title": "《项目预算表》", "note": "提交需要授信的项目的预算表电子版（word/ excel），无固定格式，根据实际情况提供",
                 "files": []},
                {"category": 14, "title": "《保险单》", "note": "授信项目的保单电子扫描件（含保险单、批单、缴费发票和被保人名单）", "files": []},
                {"category": 15, "title": "《商务经理业务经营责任书》", "note": "电子版，在有效期内，申请人已签署", "files": []},
                {"category": 16, "title": "《项目内部承包经营责任书》", "note": "电子版，在有效期内，申请人已签署", "files": []},
                {"category": 17, "title": "《商务经理资信评估表》", "note": "原件，大区经理签名，6个月内有效", "files": []},
                {"category": 18, "title": "《项目评估表》", "note": "原件，一项目一表", "files": []},
                {"category": 19, "title": "工程项目现场管理督察评定表", "note": "授信项目的评定表的电子扫描件，暂未进行评定的，可后补", "files": []},
                {"category": 21, "title": "《采购计划表》", "note": "", "files": []},
                {"category": 22, "title": "《施工计划表》", "note": "", "files": []},
                {"category": 20, "title": "其他资料", "note": "", "files": []}],
                    "status": 2, "explains": fake.sentence(),
                    "domainUri": self.domainUrl,
                    "projectApplyUri": ""}
        res = requests.post(url=self.url + data['url'], json=payloads, headers=self.head)
        self.assertEqual(res.json()['message'], 'success', msg='授信申请失败')
        makelogs('授信申请成功，响应信息为：' + res.json()['message'])

    def test_04_accountManagerLogin(self):
        """
        客户经理登录，并获取token
        :return:
        """
        head = {'Content-Type': 'application/json;charset=UTF-8'}
        data = read_data(base_path + '/Data/4_accountManagerLogin/accountManagerLogin.yaml')
        res = requests.post(url=self.url + data['url'], params=data['payloads'], headers=head)
        Test.accountManagerToken = res.json()['access_token']

    def test_05_01_getProjectApplyUriAndTaskId(self):
        """
        获取客户经理的projectApplyUri和taskId
        :return:
        """
        head = {'Content-Type': 'application/json;charset=UTF-8',
                'token': self.accountManagerToken
                }
        payloads = f'currentPage=1&pageSize=10&domainUri={self.domainUrl}&status='

        data = read_data(base_path + '/Data/5_accountManagerAudit/getTaskId.yaml')
        res = requests.get(url=self.url + data['url'], params=payloads, headers=head)
        Test.kh_projectApplyUri = res.json()['result']['records'][0]['projectApplyUri']
        Test.kh_taskId = res.json()['result']['records'][0]['currentTaskId']

    def test_05_accountManagerAudit(self):
        """
        客户经理审批
        :return:
        """
        head = {'Content-Type': 'application/json;charset=UTF-8',
                'token': self.accountManagerToken
                }
        payloads = {"applyMoney": 25063,
                    "extend": "{\"applyMoney\":25063,\"remarks\":\"\"}",
                    "flag": 0,
                    "roleFlag": 1, "upFiles": [],
                    "projectApplyUri": self.kh_projectApplyUri,
                    "taskId": self.kh_taskId,
                    "domainUri": self.domainUrl}
        data = read_data(base_path + '/Data/5_accountManagerAudit/accountManagerAudit.yaml')
        res = requests.post(url=self.url + data['url'], json=payloads, headers=head)
        self.assertEqual(res.json()['message'], 'success', msg='客户经理审批失败')

    def test_06_riskControlManagerLogin(self):
        """
        风控经理登录，并获取token
        :return:
        """
        head = {'Content-Type': 'application/json;charset=UTF-8'}
        data = read_data(base_path + '/Data/6_riskControlManagerLogin/riskControlManagerLogin.yaml')
        res = requests.post(url=self.url + data['url'], params=data['payloads'], headers=head)
        Test.riskControlManagerToken = res.json()['access_token']

    def test_07_01_getProjectApplyUriAndTaskId(self):
        """
        获取风控经理的fk_projectApplyUri和fk_taskId
        :return:
        """
        head = {'Content-Type': 'application/json;charset=UTF-8',
                'token': self.riskControlManagerToken
                }
        payloads = f'currentPage=1&pageSize=10&domainUri={self.domainUrl}&status=5'
        data = read_data(base_path + '/Data/7_riskControlManagerAudit/getTaskId.yaml')
        res = requests.get(url=self.url + data['url'], params=payloads, headers=head)
        Test.fk_projectApplyUri = res.json()['result']['records'][0]['projectApplyUri']
        Test.fk_taskId = res.json()['result']['records'][0]['currentTaskId']

    def test_07_riskControlManagerAudit(self):
        """
        风控经理审批
        :return:
        """
        head = {'Content-Type': 'application/json;charset=UTF-8',
                'token': self.riskControlManagerToken
                }
        payloads = {"applyMoney": 25063,
                    "extend": "{\"applyMoney\":25063,\"remarks\":\"\",\"riskForm\":{\"validityDate\":\"2023-11-29\",\"applyType\":0,\"isLoop\":1,\"controlList\":[]}}",
                    "flag": 0,
                    "roleFlag": 2,
                    "upFiles": [],
                    "projectApplyUri": self.fk_projectApplyUri,
                    "taskId": self.fk_taskId,
                    "domainUri": self.domainUrl}
        data = read_data(base_path + '/Data/7_riskControlManagerAudit/riskControlManagerAudit.yaml')
        res = requests.post(url=self.url + data['url'], json=payloads, headers=head)
        self.assertEqual(res.json()['message'], 'success', msg='风控经理审批失败')

    def test_08_directorOfRiskControlLogin(self):
        """
        风控总监登录，并获取token
        :return:
        """
        head = {'Content-Type': 'application/json;charset=UTF-8'}
        data = read_data(base_path + '/Data/8_directorofRiskControlLogin/directorofRiskControlLogin.yaml')
        res = requests.post(url=self.url + data['url'], params=data['payloads'], headers=head)
        # 风控总监：cszh00008 的登录token
        Test.directorOfRiskControlToken = res.json()['access_token']

    def test_09_01_getProjectApplyUriAndTaskId(self):
        """
        获取风控总监的fkzj_projectApplyUri和fkzj_taskId
        :return:
        """
        head = {'Content-Type': 'application/json;charset=UTF-8',
                'token': self.directorOfRiskControlToken
                }
        payloads = f'currentPage=1&pageSize=10&domainUri={self.domainUrl}&status=5'
        data = read_data(base_path + '/Data/9_directorofRiskControl/getTaskId.yaml')
        res = requests.get(url=self.url + data['url'], params=payloads, headers=head)
        Test.fkzj_projectApplyUri = res.json()['result']['records'][0]['projectApplyUri']
        Test.fkzj_taskId = res.json()['result']['records'][0]['currentTaskId']

    def test_09_directorOfRiskControlAudit(self):
        """
        风控总监审批
        :return:
        """
        head = {'Content-Type': 'application/json;charset=UTF-8',
                'token': self.directorOfRiskControlToken}

        payloads = {"applyMoney": self.applyMoney,
                    "extend": "{\"applyMoney\":'"+str(self.applyMoney)+"',\"remarks\":\"\",""\"riskForm\":{\"validityDate\":\"2023-11-29\",\"applyType\":0,\"isLoop\":1,\"controlList\":[]}}",
                    "flag": 0,
                    "roleFlag": 3,
                    "upFiles": [],
                    "projectApplyUri": self.fkzj_projectApplyUri,
                    "taskId": self.fkzj_taskId,
                    "domainUri": self.domainUrl}

        data = read_data(base_path + '/Data/9_directorofRiskControl/directorofRiskControlAudit.yaml')
        res = requests.post(url=self.url + data['url'], json=payloads, headers=head)
        self.assertEqual(res.json()['message'], 'success', msg='风控经理审批失败')
        makelogs('风控经理审批完成，响应信息为：' + res.json()['message'])

    def test_10_generalManagerLogin(self):
        """
        总经理登录，并获取token
        :return:
        """
        head = {'Content-Type': 'application/json;charset=UTF-8'}
        data = read_data(base_path + '/Data/10_generalmanagerLogin/generalmanagerLogin.yaml')
        res = requests.post(url=self.url + data['url'], params=data['payloads'], headers=head)
        # 总经理：cszh00006  的登录token
        Test.generalManagerToken = res.json()['access_token']

    def test_11_01_getProjectApplyUriAndTaskId(self):
        """
        获取总经理的zjl_projectApplyUri和zjl_taskId
        :return:
        """
        head = {'Content-Type': 'application/json;charset=UTF-8',
                'token': self.generalManagerToken
                }
        payloads = f'currentPage=1&pageSize=10&domainUri={self.domainUrl}&status=5'
        data = read_data(base_path + '/Data/11_generalmanager/getTaskId.yaml')
        res = requests.get(url=self.url + data['url'], params=payloads, headers=head)
        Test.zjl_projectApplyUri = res.json()['result']['records'][0]['projectApplyUri']
        Test.zjl_taskId = res.json()['result']['records'][0]['currentTaskId']

    def test_11_03_generalManagerAudit(self):
        """
        总经理审批
        :return:
        """
        head = {'Content-Type': 'application/json;charset=UTF-8',
                'token': self.generalManagerToken
                }
        payloads = {"applyMoney": self.applyMoney,
                    "extend": "{\"applyMoney\":'"+str(self.applyMoney)+"',\"remarks\":\"\",\"riskForm\":{\"validityDate\":\"2023-11-29\",\"applyType\":0,\"isLoop\":1,\"controlList\":[]}}",
                    "flag": 0,
                    "roleFlag": 4, "upFiles": [],
                    "projectApplyUri": self.zjl_projectApplyUri,
                    "taskId": self.zjl_taskId,
                    "domainUri": self.domainUrl}
        data = read_data(base_path + '/Data/11_generalmanager/generalmanagerAudit.yaml')
        res = requests.post(url=self.url + data['url'], json=payloads, headers=head)
        self.assertEqual(res.json()['message'], 'success', msg='风控经理审批失败')
        makelogs('风控经理审批成功，响应信息为：' + res.json()['message'])

    def test_12_01_financialManagerLogin(self):
        """
        财务经理登录，获取登录token
        :return:
        """
        head = {'Content-Type': 'application/json;charset=UTF-8'}
        data = read_data(base_path + '/Data/12_Financial manager/FinancialmanagerLogin.yaml')
        res = requests.post(url=self.url + data['url'], params=data['payloads'], headers=head)
        Test.financialManagerToken = res.json()['access_token']

    def test_12_02_getProjectApplyUriAndTaskId(self):
        """
        获取财务经理的zjl_projectApplyUri和zjl_taskId
        :return:
        """
        head = {'Content-Type': 'application/json;charset=UTF-8',
                'token': self.financialManagerToken
                }
        payloads = f'currentPage=1&pageSize=10&domainUri={self.domainUrl}&status=5'
        data = read_data(base_path + '/Data/12_Financial manager/getTaslId.yaml')
        res = requests.get(url=self.url + data['url'], params=payloads, headers=head)

        Test.cwjl_projectApplyUri = res.json()['result']['records'][0]['projectApplyUri']
        Test.cwjl_taskId = res.json()['result']['records'][0]['currentTaskId']

    def test_12_03_financialManagerAudit(self):
        """
        财务经理审批
        :return:
        """
        head = {'Content-Type': 'application/json;charset=UTF-8',
                'token': self.financialManagerToken
                }
        payloads = {"applyMoney": self.applyMoney,
                    "extend": "{\"applyMoney\":'"+str(self.applyMoney)+"',\"remarks\":\"\",\"riskForm\":{\"validityDate\":\"2023-11-29\",\"applyType\":0,\"isLoop\":1,\"controlList\":[]}}",
                    "flag": 0, "roleFlag": 5, "upFiles": [], "projectApplyUri": self.cwjl_projectApplyUri,
                    "taskId": self.cwjl_taskId, "domainUri": self.domainUrl}

        data = read_data(base_path + '/Data/12_Financial manager/financialManagerAudit.yaml')
        res = requests.post(url=self.url + data['url'], json=payloads, headers=head)
        self.assertEqual(res.json()['message'], 'success', msg='财务经理审批失败')
        makelogs('财务经理审批成功，响应信息为：' + res.json()['message'])

    def test_12_04_update(self):
        """
        财务经理update
        :return:
        """
        head = {'Content-Type': 'application/json;charset=UTF-8',
                'token': self.financialManagerToken
                }
        payloads = {"applyType": 0, "isLoop": 1, "projectApplyUri": self.cwjl_projectApplyUri,
                    "realAmount": self.applyMoney, "realBusinessType": "[{\"type\":1,\"value\":\"开商票\"}]",
                    "validityDate": "2023-11-29", "fkDomain": self.domainUrl}
        data = read_data(base_path + '/Data/12_Financial manager/update.yaml')
        res = requests.post(url=self.url + data['url'], json=payloads, headers=head)
        self.assertEqual(res.json()['message'], 'success', msg='财务经理update失败')
        makelogs('财务经理update成功，响应信息为：' + res.json()['message'])

    def test_13_01_financialDirectorLogin(self):
        """
        财务总监登录并获取登录token
        :return:
        """
        head = {'Content-Type': 'application/json;charset=UTF-8'}
        data = read_data(base_path + '/Data/13_financialdirector/financial_directorLogin.yaml')
        res = requests.post(url=self.url + data['url'], params=data['payloads'], headers=head)
        Test.financialDirectorToken = res.json()['access_token']

    def test_13_02_getProjectApplyUriAndTaskId(self):
        """
        获取财务总监的zjl_projectApplyUri和zjl_taskId
        :return:
        """
        head = {'Content-Type': 'application/json;charset=UTF-8',
                'token': self.financialDirectorToken
                }
        payloads = f'currentPage=1&pageSize=10&domainUri={self.domainUrl}&status=5'
        data = read_data(base_path + '/Data/13_financialdirector/getTaslId.yaml')
        res = requests.get(url=self.url + data['url'], params=payloads, headers=head)

        Test.cwzj_projectApplyUri = res.json()['result']['records'][0]['projectApplyUri']
        Test.cwzj_taskId = res.json()['result']['records'][0]['currentTaskId']

    def test_13_03_financialDirectorAudit(self):
        """
        财务总监审批
        :return:
        """
        head = {'Content-Type': 'application/json;charset=UTF-8',
                'token': self.financialDirectorToken
                }

        payloads = {"applyMoney": self.applyMoney,
                    "extend": "{\"applyMoney\":'"+str(self.applyMoney)+"',\"remarks\":\"\",\"riskForm\":{\"validityDate\":\"2023-11-29\",\"applyType\":0,\"isLoop\":1,\"controlList\":[]}}",
                    "flag": 0, "roleFlag": 6, "upFiles": [], "projectApplyUri": self.cwzj_projectApplyUri,
                    "taskId": self.cwzj_taskId, "domainUri": self.domainUrl}
        data = read_data(base_path + '/Data/13_financialdirector/financialDirectorAudit.yaml')
        res = requests.post(url=self.url + data['url'], json=payloads, headers=head)
        self.assertEqual(res.json()['message'], 'success', msg='财务总监审批失败')
        makelogs('财务总监审批成功，响应信息为：' + res.json()['message'])

    def test_13_04_update(self):
        """
        财务总监update
        :return:
        """
        head = {'Content-Type': 'application/json;charset=UTF-8',
                'token': self.financialDirectorToken
                }
        payloads = {"applyType": 0, "isLoop": 1, "projectApplyUri": self.cwzj_projectApplyUri,
                    "realAmount": self.applyMoney, "realBusinessType": "[{\"type\":1,\"value\":\"开商票\"}]",
                    "validityDate": "2023-11-29", "fkDomain": self.domainUrl}
        data = read_data(base_path + '/Data/13_financialdirector/update.yaml')
        res = requests.post(url=self.url + data['url'], json=payloads, headers=head)
        self.assertEqual(res.json()['message'], 'success', msg='财务总监update失败')
        makelogs('财务总监update成功，响应信息为：' + res.json()['message'])

    def test_14_01_presidentLogin(self):
        """
        总裁登录
        :return:
        """
        head = {'Content-Type': 'application/json;charset=UTF-8'}
        data = read_data(base_path + '/Data/14_president/presidentLogin.yaml')
        res = requests.post(url=self.url + data['url'], params=data['payloads'], headers=head)
        Test.presidentToken = res.json()['access_token']

    def test_14_02_getProjectApplyUriAndTaskId(self):
        """
        获取总裁的zjl_projectApplyUri和zjl_taskId
        :return:
        """
        head = {'Content-Type': 'application/json;charset=UTF-8',
                'token': self.presidentToken
                }
        payloads = f'currentPage=1&pageSize=10&domainUri={self.domainUrl}&status=5'
        data = read_data(base_path + '/Data/14_president/getTaslId.yaml')
        res = requests.get(url=self.url + data['url'], params=payloads, headers=head)
        Test.zc_projectApplyUri = res.json()['result']['records'][0]['projectApplyUri']
        Test.zc_taskId = res.json()['result']['records'][0]['currentTaskId']

    def test_14_03_presidentAudit(self):
        """
        总裁审批
        :return:
        """
        head = {'Content-Type': 'application/json;charset=UTF-8',
                'token': self.presidentToken
                }
        payloads = {"applyMoney": self.applyMoney,
                    "extend": "{\"applyMoney\":'"+str(self.applyMoney)+"',\"remarks\":\"\",\"riskForm\":{\"validityDate\":\"2023-11-29\",\"applyType\":0,\"isLoop\":1,\"controlList\":[]}}",
                    "flag": 0, "roleFlag": 7, "upFiles": [], "projectApplyUri": self.zc_projectApplyUri,
                    "taskId": self.zc_taskId, "domainUri": self.domainUrl}
        data = read_data(base_path + '/Data/14_president/presidentAudit.yaml')
        res = requests.post(url=self.url + data['url'], json=payloads, headers=head)
        self.assertEqual(res.json()['message'], 'success', msg='总裁审批失败')
        makelogs('总裁审批成功，响应信息为：' + res.json()['message'])

    def test_14_04_update(self):
        """
        总裁update
        :return:
        """
        head = {'Content-Type': 'application/json;charset=UTF-8',
                'token': self.presidentToken
                }
        payloads = {"applyType": 0, "isLoop": 1, "projectApplyUri": self.zc_projectApplyUri,
                    "realAmount": self.applyMoney, "realBusinessType": "[{\"type\":1,\"value\":\"开商票\"}]",
                    "validityDate": "2023-11-29", "fkDomain": self.domainUrl}
        data = read_data(base_path + '/Data/14_president/update.yaml')
        res = requests.post(url=self.url + data['url'], json=payloads, headers=head)
        self.assertEqual(res.json()['message'], 'success', msg='总裁update失败')
        makelogs('总裁update成功，响应信息为：' + res.json()['message'])


if __name__ == '__main__':
    unittest.main()
