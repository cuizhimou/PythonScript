from urllib import urlopen
import json

def getdata():
    f= urlopen('http://192.168.1.30:59000/health')
    data=f.read()
    return json.loads(data)

def dataformat():
    data=getdata()
    serverstatus=data['status'].encode('utf8')
    mail=data['mail']['status'].encode('utf8')
    diskspace=data['diskSpace']['status'].encode('utf8')
    redis=data['redis']['status'].encode('utf8')
    db=data['db']['status'].encode('utf8')
    return {'sertatus': serverstatus,'mail': mail,'diskspace': diskspace,'redis': redis,'db': db}

def monitor():
    result=[]
    dic=dataformat()
    print type(dic)
    for k,v in dataformat():
        if v !='UP':
            result.append(k)
    return result
if __name__ == '__main__':
    print dataformat()
    monitor()

