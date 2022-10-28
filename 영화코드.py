from flask import Flask, render_template, redirect, jsonify, url_for
from flask import request
import requests
from bs4 import BeautifulSoup
import json

app = Flask(__name__)

@app.route("/movieNo", methods=['GET', 'POST'])
def MovieNo():
    movieNm = request.form['movieNm']

    url = "https://www.megabox.co.kr/on/oh/oha/Movie/selectMovieList.do"
    parameters = {
    "currentPage": "1",
    "recordCountPerPage": "100",
    "pageType": "ticketing",
    "ibxMovieNmSearch": movieNm,
    "onairYn": "Y",
    "specialType": "",
    "specialYn": "N"
    }

    response = requests.post(url, data = parameters).json()

    movie_response = response['movieList']

    for movie in movie_response:
        rpstMovieNo = movie["rpstMovieNo"]

    return json.dumps(rpstMovieNo, ensure_ascii=False)

@app.route("/dd", methods=['GET','POST'])
def test():
    # movieNo = request.form['movieNo']
    # print(movieNo)

    url = "https://www.megabox.co.kr/on/oh/ohc/Brch/schedulePage.do"
    parameters = {
    "masterType": "brch",
    "detailType": "area",
    "brchNo": "0019",
    "firstAt": "N",
    "brchNo1": "0019",
    "crtDe": "20220903",
    "playDe": "20220903"
    }

    dic = {}

    response = requests.post(url, data = parameters).json()

    movie_response = response['megaMap']['movieFormList']

    def get_movie_no_list(response) :
        movie_no_list = []
        for item in response:
            movie_no = item["rpstMovieNo"]
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

        for movie_th in th_list:
            
            movie = [item for item in movies if item["theabNo"].replace("0", "") == movie_th]
            
            tuples = []
            for i in range(len(movie)):
                time = movie[i]["playStartTime"]
                seats = movie[i]["restSeatCnt"]
                playkind = movie[i]["playKindNm"]
                playSchdlNo = movie[i]["playSchdlNo"]
                tuple = (time, seats, playkind, playSchdlNo)
                tuples.append(tuple)
            
            dic[movie_th] = tuples
        
        return dic

    def split_movies_by_no(response):
        movie_no_list = get_movie_no_list(response)
        for movie_no in movie_no_list:
            movies = [item for item in response if item["rpstMovieNo"] == movie_no]
            title = movies[0]["movieNm"].replace('&#40;', '(').replace('&#41;', ')')
            timetable = get_time_table(movies)
            dic[title] = timetable
            
        # print(dic, "\n")
    split_movies_by_no(movie_response)

    return json.dumps(dic, ensure_ascii=False)

if __name__ == '__main__':
    app.run(debug=True,host="127.0.0.1",port=5000)