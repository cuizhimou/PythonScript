# coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import pymysql
import types
import datetime
from datetime import datetime
from datetime import date
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

from prettytable import PrettyTable

mailto_list = ["cuizhimou@feellike21.com"]
# mailto_list = ["cuizhimou@feellike21.com","luzuoqi@feellike21.com","zheng@feellike21.com","kaiz@feellike21.com","siyanliu@feellike21.com","zhaoye@feellike21.com","haohongpei@feellike21.com","liuyu@feellike21.com"]
mail_host = "smtp.exmail.qq.com"  # 设置服务器
mail_user = "xxxx@xxx.com"  # 用户名
mail_pass = "xxxxxx"  # 口令


def send_mail(to_list, sub, content):
    exname = datetime.now().strftime('%Y-%m-%d')
    me = "op<" + mail_user + ">"
    msgRoot = MIMEMultipart('related')
    msgRoot['subject'] = sub
    msgRoot['From'] = me
    msgRoot['To'] = ";".join(to_list)
    msgText = MIMEText(content, _subtype='html', _charset='utf-8')
    msgRoot.attach(msgText)
    # 构造附件
    att = MIMEText(open('./table.xls', 'r').read(), 'base64', 'utf-8')
    att["Content-Type"] = 'application/octet-stream'
    att["Content-Disposition"] = 'attachment; filename="{0}.xls"'.format(str(exname))
    msgRoot.attach(att)

    server = smtplib.SMTP()
    server.connect(mail_host)
    server.login(mail_user, mail_pass)
    server.sendmail(me, to_list, msgRoot.as_string())
    server.close()


def getdata():
    conn = pymysql.connect(host='192.168.1.30', port=3306,
                           user='root', passwd='Admin@123',
                           db='tahiti',
                           charset='utf8')
    sql = "SELECT date(rsv.create_time) as '预约日期'," \
          "date(reserve_time) as '体检日期', " \
          "usr.name as '姓名'," \
          "case usr.sex " \
          "when 1 then '男' " \
          "when 2 then '女' " \
          "else concat('未知性别:', usr.sex) end as '性别'," \
          "usr.identity_number as '身份证'," \
          "usr.mobile as '手机号码'," \
          "case rsv.status " \
          "when 0 then '已预约' " \
          "when 1 then '已到检' " \
          "when 2 then '已出报告' " \
          "when 3 then '已出报告' " \
          "when 4 then '已过期' " \
          "when 5 then '已取消' " \
          "else concat('未知状态:', rsv.status) end as '预约状态'," \
          "cmp.company_name as '公司名称'," \
          "inst.name as '机构名称'," \
          "pack.name as '套餐名称' " \
          "FROM tahiti.tbl_he_reserve rsv " \
          "join tahiti.tbl_user usr on usr.user_id = rsv.user_id " \
          "join tahiti.tbl_institution inst on inst.inst_id = rsv.inst_id " \
          "join tahiti.tbl_invitation_code code " \
          "on code.invitation_code = rsv.invitation_code " \
          "join tahiti.tbl_invitation inv on inv.invitation_id = code.invitation_id " \
          "join tahiti.tbl_company cmp on inv.company_id = cmp.company_id " \
          "join tahiti.tbl_he_package pack on pack.pack_id = inv.pack_id " \
          "where upper(rsv.invitation_code) != 'UJK22B2U';"
    cur = conn.cursor()
    num = cur.execute(sql)
    info = cur.fetchmany(num)
    # todo:关闭连接； num没有用到
    conn.close()
    return info


def dataformat(alist):  # num没有用到
    # yesterday = today - datetime.timedelta(days=1)
    today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    #data = map(list, alist)
    table_border = "<table border=\"1\"> <caption>" + str(today) + "统计数据</caption> "
    table_title = " <tr><th>预约日期</th><th>体检日期</th>" \
                  "<th>姓名</th><th>性别</th><th>身份证</th>" \
                  "<th>手机号</th><th>预约状态</th><th>公司名称</th>" \
                  "<th>机构名称</th><th>套餐名称</th></tr>"

    content = table_border + table_title + draw_table_content(alist)
    content = content
    return content


# 根据数据绘制表格内容
def draw_table_content(matrix):
    content = ''
    for row in matrix:
        content = "{0}<tr>".format(content is None and '' or content)
        for ele in row:
            if ele is None:
                ele = " "
            # 以下几种类型写入excel时，需要先转为str
            if not isinstance(ele, str):
                ele = str(ele)
            content = "{0}<td>{1}</td>".format(content, ele.encode("utf8"))
        content = "{0}</tr>".format(content)
    return content + " </table>"


def drawExcle(sdata):
    from xlwt import Workbook
    file = Workbook(encoding='utf-8')
    # 指定file以utf-8的格式打开
    table = file.add_sheet('table.xls')
    # 指定打开的文件名
    alist = list(sdata)
    alist.insert(0, ('预约日期', '体检日期', '姓名', '性别', '身份证',
                     '手机号', '预约状态', '公司名称', '机构名称', '套餐名称'))
    for i, t in enumerate(alist):
        for j, p in enumerate(t):
            table.write(i, j, str(p))
    file.save('table.xls')


if __name__ == '__main__':
    hours = datetime.now().strftime('%H:%M:%S')
    today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    sdata = getdata()
    drawExcle(sdata[0])
    sub = str(today) + "团检统计结果"
    scontent = "您好:  " + str(hours) + " 团检统计结果:\n\n" + str(dataformat(sdata[0], sdata[1]))
    send_mail(mailto_list, sub, scontent)
