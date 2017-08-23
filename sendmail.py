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
    sql = "select cmp.company_name as \'公司名称\',inv.name as \'姓名\',case inv.pay_type when 0 then \'企业支付\' when 1 then \'员工自付\' when 2 then \'检后全额报销\' when 3 then \'检后固定报销\' else \'未知\' end as \'支付类型\',case inv.board_status when 0 then \'待处理\' when 1 then \'入职\' when 2 then \'拒绝入职\' else \'未知\' end as \'入职状态\',inv.reserve_id as \'预约id\',inst.name as  \'体检机构\' from tbl_cmp_he_invitation inv left join tbl_company cmp on inv.cmp_id = cmp.company_id left join tbl_he_reserve rsv on rsv.he_id = inv.reserve_id left join tbl_institution inst on inst.inst_id = rsv.inst_id where date(inv.update_time)=date_sub(date(now()), interval 1 day) and inv.cmp_id>=8"
    cur = conn.cursor()
    num = cur.execute(sql)
    info = cur.fetchmany(num)
    return info, num


def dataformat(alist, num):
    yesterday = today - datetime.timedelta(days=1)
    data = []
    data = map(list, alist)
    content = "<table border=\"1\"> <caption>" + str(yesterday) + "统计数据</caption> "
    content = content + " <tr><th>公司名称</th><th>姓名</th><th>支付类型</th><th>入职状态</th><th>预约id</th><th>体检机构</th></tr>"
    for i in range(num):
        for j in range(len(data[i])):
            if data[i][j] is None:
                data[i][j] = "  "
        content = content + " <tr><td>" + data[i][0].encode("utf8") + "</td><td>" + data[i][1].encode(
            "utf8") + "</td><td>" + data[i][2].encode("utf8") + "</td><td>" + data[i][3].encode(
            "utf8") + "</td><td>" + str(data[i][4]).encode("utf8") + "</td><td>" + data[i][5].encode(
            "utf8") + "</td></tr>"
    content = content + " </table>"
    return content


if __name__ == '__main__':
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    sdata = getdata()
    sub = str(today) + "塔希提统计结果"
    scontent = "您好:  " + str(today) + " 塔希提统计结果:\n\n" + str(dataformat(sdata[0], sdata[1]))
    send_mail(mailto_list, sub, scontent)
