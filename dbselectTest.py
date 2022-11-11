import pymysql


def test():
    conn = pymysql.connect(host="database-1.cxva4q1y2ban.ap-northeast-2.rds.amazonaws.com",
                       port=33062,
                       user="root",
                       password="dhrtms80",
                       db="movie",
                       charset = "utf8")
    sql = "SELECT * FROM openAlarm WHERE state = 1"

    global brchNo
    global rpstMovieNo
    global theabKindCd
    global playDe
    global phone
    selectList = []

    cur = conn.cursor()

    cur.execute(sql)
    result = cur.fetchall()
    for data in result:
        brchNo = data[2]
        rpstMovieNo = data[3]
        theabKindCd = data[5]
        phone = data[6]
        playDe = data[7]
        state = data[8]
        list = [brchNo, rpstMovieNo, theabKindCd, phone, playDe, state]
        selectList.append(list)

test()