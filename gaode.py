import requests
import pymysql


def geocode(address):
         parameters = {'address': address, 'key': 'cb649a25c1f81c1451adbeca73623251'}
         base = 'http://restapi.amap.com/v3/geocode/geo'
         response = requests.get(base, parameters)
         answer = response.json()
         #print(answer['geocodes'][0]['location'])
         return answer['geocodes'][0]['location'].split(',')
def flush_data():
    conn = pymysql.connect(host='192.168.1.30', port=3306,
                           user='root', passwd='Admin@123',
                           db='tahiti',
                           charset='utf8')
    sql='select address,inst_id from tahiti.tbl_institution where inst_id >= 1381;'
    upsql='update tbl_institution set longitude={0},latitude={1} where inst_id={2};'
    cur = conn.cursor()
    num = cur.execute(sql)
    for atuple in cur.fetchmany(num):
        alist=geocode(atuple[0])
        upnewsql=upsql.format(alist[0],alist[1],atuple[1])
        cur.execute(upnewsql)
        print(atuple[0],atuple[1],alist)
    conn.commit()

if __name__=='__main__':
        #address = '上海市张杨路560号中融恒瑞大厦6楼西区'
        #print(geocode(address))
        #flush_data()
        flush_data()