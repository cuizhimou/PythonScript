from urllib import urlopen
import json
import smtplib
from email.mime.text import MIMEText

mailto_list = ["cuizhimou@feellike21.com"]
mail_host = "smtp.exmail.qq.com"
mail_user = "seafile@feellike21.com"
mail_pass = "xxxx"


def send_mail(to_list, sub, content):
    me = "OP<" + mail_user + ">"
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
    f= urlopen('http://192.168.1.30:59000/health')
    data=f.read()
    if f.code==200:
        return json.loads(data)
    else:
        return 404
def dataformat():
    data=getdata()
    if data !=404:
        serverstatus=data['status'].encode('utf8')
        mail=data['mail']['status'].encode('utf8')
        diskspace=data['diskSpace']['status'].encode('utf8')
        redis=data['redis']['status'].encode('utf8')
        db=data['db']['status'].encode('utf8')
        return {'sertatus': serverstatus,'mail': mail,
                'diskspace': diskspace,'redis': redis,'db': db}
if __name__ == '__main__':
    with open('./tmp.txt','r') as f1:
        num=f1.read().strip()
    result=dataformat()
    print(result)
    if getdata()==404:
        send_mail(mailto_list, "BTV interface Down", str(result))
    elif 'DOWN' in result.values():
        if num >='2':
            num='0'
            with open('./tmp.txt','w') as f2:
                f2.write(num)
            send_mail(mailto_list, "BTV interface Down", str(result))
        else:
            num=int(num)+1
            with open('./tmp.txt','w') as f3:
                f3.write(str(num))
    else:
        if num !='0':
            num='0'
            with open('./tmp.txt', 'w') as f4:
                f4.write(num)