# coding: utf-8
import pymysql
import datetime
import smtplib
from email.mime.text import MIMEText
from prettytable import PrettyTable

mailto_list = ["xxx@xxx.com"]
mail_host = "smtp.exmail.qq.com"  # 设置服务器
mail_user = "xxx@xxx"  # 用户名
mail_pass = "xxxxx"  # 口令


def send_mail(to_list, sub, content):
    me = "张三<" + mail_user + ">"
    msg = MIMEText(content, _subtype='html', _charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)

    server = smtplib.SMTP()
    server.connect(mail_host)
    server.login(mail_user, mail_pass)
    server.sendmail(me, to_list, msg.as_string())
    server.close()


def getdata():
    conn = pymysql.connect(host='192.168.1.20', port=3306,
                           user='root', passwd='xxx',
                           db='tahiti',
                           charset='utf8')
    sql ="SELECT date(reserve_time) as \'日期\',usr.name as \'姓名\',case usr.sex " \
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
         "when 5 then '已取消'" \
         "else concat('未知状态:', rsv.status) end as '预约状态'," \
         "inst.name as '机构名称'," \
         "pack.name as '套餐名称'" \
         "FROM tahiti.tbl_he_reserve rsv" \
         "join tahiti.tbl_user usr on usr.user_id = rsv.user_id " \
         "join tahiti.tbl_institution inst on inst.inst_id = rsv.inst_id " \
         "join tahiti.tbl_invitation_code code on code.invitation_code = rsv.invitation_code " \
         "join tahiti.tbl_invitation inv on inv.invitation_id = code.invitation_id " \
         "join tahiti.tbl_he_package pack on pack.pack_id = inv.pack_id " \
         "where date(rsv.update_time) = date(now());"
    cur = conn.cursor()
    num = cur.execute(sql)
    info = cur.fetchmany(num)
    return info, num


def dataformat(alist, num):
    yesterday = today - datetime.timedelta(days=1)
    data = []
    data = map(list, alist)
    content = "<table border=\"1\"> <caption>" + str(yesterday) + "统计数据</caption> "
    content = content + " <tr><th>日期</th><th>姓名</th><th>性别</th><th>身份证</th><th>手机号</th>" \
                        "<th>手机号</th><th>预约状态</th><th>机构名称</th><th>套餐名称</th></tr>"
    # content = content + draw_table(data)
    for i in range(num):
        for j in range(len(data[i])):
            if data[i][j] is None:
                data[i][j] = "  "
        content = content + " <tr><td>" + \
                  data[i][0].encode("utf8") + "</td><td>" + \
                  data[i][1].encode("utf8") + "</td><td>" + \
                  data[i][2].encode("utf8") + "</td><td>" + \
                  data[i][3].encode("utf8") + "</td><td>" + \
                  data[i][4].encode("utf8") + "</td><td>" + \
                  data[i][5].encode("utf8") + "</td><td>" + \
                  data[i][6].encode("utf8") + "</td><td>" + \
                  data[i][7].encode("utf8") + \
                  "</td></tr>"
    content = content + " </table>"
    return content

# 根据数据绘制表格内容
def draw_table(matrix):
    content = ''
    for row in matrix:
        content = "{0}<tr>".format(content is None and '' or content)
        for ele in row:
            if ele is None:
                ele = " "
                # print ele
            content = "{0}<td>{1}</td>".format(content, type(ele) is types.LongType and ele or ele.encode("utf8"))
        content = "{0}</tr>".format(content)
    return content

if __name__ == '__main__':
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    sdata = getdata()
    sub = str(today) + "塔希提统计结果"
    scontent = "您好:  " + str(today) + " 塔希提统计结果:\n\n" + str(dataformat(sdata[0], sdata[1]))
    send_mail(mailto_list, sub, scontent)
