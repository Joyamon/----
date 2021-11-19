# coding=utf-8
# @author周彦明
# projectName:经营SAAS系统业务接口测试
# time:2021-08-21
import os
import smtplib  # 邮箱服务器
from email.mime.text import MIMEText  # 邮件模版类
from email.mime.multipart import MIMEMultipart  # 邮件附件类
from email.header import Header  # 邮件头部模版
from common.readYaml import read_data
from common.settings import base_path


# 发送带邮件的函数 动作
def send_mail(file_new):
    f = open(file_new, 'r', encoding='utf-8')
    mail_body = f.read()
    f.close()

    data = read_data(base_path + "/config/config.yaml")
    # 基本信息
    smtpserver = data['smtpserver']
    pwd = data['pwd']  # 邮箱授权码

    # 定义邮件主题
    msg = MIMEMultipart()
    msg['subject'] = Header('接口自动化测试报告', 'utf-8')
    msg['from'] = data['from']  # 必须加 不加报错  发送者的邮箱
    # 510807146 @ qq.com
    msg['to'] = data['to']  # 必须加 不加报错  接收者的邮箱
    msg['Content-Disposition'] = 'attachment,filename=test_report.html'
    # "510807146@qq.com"
    # HTML邮件正文 直接发送附件的代码片段
    body = MIMEText(mail_body, "html", "utf-8")
    msg.attach(body)
    att = MIMEText(mail_body, "base64", "utf-8")
    att["Content-Type"] = "application/octet-stream"
    att.add_header("Content-Disposition", 'attachment; filename=test_report.html')
    msg.attach(att)

    # 链接邮箱服务器发送邮件
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(msg['from'], pwd)
    smtp.sendmail(msg['from'], msg['to'], msg.as_string())
    print("邮件发送成功")


# 查找最新邮件
def new_file(test_dir):
    result_dir = test_dir
    lists = os.listdir(result_dir)  # print(lists)  #列出测试报告目录下面所有的文件
    lists.sort()  # 从小到大排序 文件
    file = [x for x in lists if x.endswith('.html')]  # for循环遍历以.html格式的测试报告
    file_path = os.path.join(result_dir, file[-1])  # 找到测试报告目录下面最新的测试报告
    return file_path  # 返回最新的测试报告
