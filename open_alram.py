import sched
import requests
import pymysql
import datetime as dt
from apscheduler.schedulers.background import BackgroundScheduler
import time
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException

def test():
    schedule()

def schedule():
    api_key = "NCSRFMHDTQYIKPZP"
    api_secret = "PXNQNRPPTFIG6HTWL6XOH5GTC34SKDLV"

    conn = pymysql.connect(host="database-1.cxva4q1y2ban.ap-northeast-2.rds.amazonaws.com",
                       port=33062,
                       user="root",
                       password="dhrtms80",
                       db="movie",
                       charset = "utf8")

    sql = "SELECT * FROM openAlarm WHERE state = 1"
    sql2 = "UPDATE openAlarm SET state = 0, updatedAt = now() WHERE seq = (%s)"

    global seq
    global brchNo
    global rpstMovieNo
    global theabKindCd
    global playDe
    global phone

    cur = conn.cursor()

    cur.execute(sql)
    result = cur.fetchall()
    
    for data in result:
        arr = []
        arr.clear()

        seq = data[0]
        brchNo = data[2]
        rpstMovieNo = data[3]
        theabKindCd = data[5]
        phone = data[6]
        playDe = data[7]
        state = data[8]

        print("start seq : " + str(seq))
        
        params = dict()
        params['type'] = 'sms' # Message type ( sms, lms, mms, ata )
        params['to'] = phone # Recipients Number '01000000000,01000000001'
        params['from'] = '01025116861' # Sender number

        today = dt.datetime.now().strftime('%Y%m%d')

        url = "https://www.megabox.co.kr/on/oh/ohc/Brch/schedulePage.do"
        parameters = {
            "masterType": "brch",
            "detailType": "spcl",
            "theabKindCd": theabKindCd,
            "brchNo": brchNo,
            "firstAt": "N",
            "brchNo1": brchNo,
            "spclbYn1": "Y",
            "theabKindCd1": theabKindCd,
            "crtDe": today,
            "playDe": playDe
        }

        response = requests.post(url, data = parameters).json()

        movie_response = response['megaMap']['movieFormList']

        if (len(result)) >= 1:
            for item in movie_response:
                if str(rpstMovieNo) == item["rpstMovieNo"]:
                    playSchdlNo = item["playSchdlNo"]
                    if playSchdlNo not in arr:
                        arr.append(playSchdlNo)
            if (len(arr)) != 0:
                for item in movie_response:
                    if arr[-1] == item["playSchdlNo"]:
                        params['text'] = item["movieNm"] + "(" + item["playStartTime"] + ") " + item["theabExpoNm"] + " 예매(" + item["brchNm"].replace('&#40;', '(').replace('&#41;', ')') + ")가 열렸습니다" # Message
                        cur.execute(sql2, seq)
                        sched.pause()
                    
            sched.resume()

        cool = Message(api_key, api_secret)
        try:
            response = cool.send(params)
            print("Success Count : %s" % response['success_count'])
            print("Error Count : %s" % response['error_count'])
            print("Group ID : %s" % response['group_id'])

            if "error_list" in response:
                print("Error List : %s" % response['error_list'])

        except CoolsmsException as e:
            print("Error Code : %s" % e.code)
            print("Error Message : %s" % e.msg)
        
    conn.commit()
    cur.close()
    conn.close()

sched = BackgroundScheduler(timezone='Asia/Seoul')
sched.start()
sched.add_job(schedule, 'interval', seconds=10, id="test1")

while True:
    time.sleep(1)