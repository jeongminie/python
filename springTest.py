from flask import Flask, render_template, redirect, jsonify, url_for
from flask import request
import urllib.request
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

@app.route("/tospring", methods=['POST'])

# def connect():
#     date = request.form['date']
#     print(date)

#     return jsonify({'result':'success'})

def spring():
    date = request.form['date']
    brchNo = request.form['brchNo']
    print(date)
    print(brchNo)

    url = "https://www.megabox.co.kr/on/oh/ohc/Brch/schedulePage.do"
    parameters = {
    "masterType": "brch",
    "detailType": "area",
    "brchNo": brchNo,
    "firstAt": "N",
    "brchNo1": brchNo,
    "crtDe": date,
    "playDe": date
    }
    
    dic = {}

    response = requests.post(url, data = parameters).json()

    movie_response = response['megaMap']['movieFormList']

    def get_movie_no_list(response) :
        movie_no_list = []
        for item in response:
            movie_no = item["movieNo"]
            if movie_no not in movie_no_list:
                movie_no_list.append(movie_no)
        return movie_no_list

    def get_time_table(movies):
        movie_th_list = []

        for item in movies:
            thea = item["theabNo"].replace("0", "")
            if thea not in movie_th_list:
                movie_th_list.append(thea)
        
        th_list = movie_th_list

        dic={}

        for movie_th in th_list:
            
            movie = [item for item in movies if item["theabNo"].replace("0", "") == movie_th]
            
            tuples = []
            for i in range(len(movie)):
                time = movie[i]["playStartTime"]
                seats = movie[i]["restSeatCnt"]
                tuple = (time, seats)
                tuples.append(tuple)
            
            dic[movie_th] = tuples
        
        print(dic)

        return dic

    def split_movies_by_no(response):
        movie_no_list = get_movie_no_list(response)
        for movie_no in movie_no_list:
            movies = [item for item in response if item["movieNo"] == movie_no]
            title = movies[0]["movieNm"].replace('&#40;', '(').replace('&#41;', ')')
            timetable = get_time_table(movies)
            dic[title] = timetable
            
        print(dic, "\n")

    split_movies_by_no(movie_response)

    #render = render_template('test.html', data=dic)
    
    return json.dumps(dic, ensure_ascii=False)


if __name__ == '__main__':
    app.run(debug=True,host="127.0.0.1",port=5000)