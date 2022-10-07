from flask import Flask, render_template, redirect, url_for
import urllib.request
import requests
from bs4 import BeautifulSoup
import json


app = Flask(__name__)

@app.route("/tospring", methods=['GET'])
def spring():

    url = "https://www.megabox.co.kr/on/oh/ohc/Brch/schedulePage.do"
    parameters = {
    "masterType": "brch",
    "detailType": "area",
    "brchNo": "1372",
    "firstAt": "N",
    "brchNo1": "1372",
    "crtDe": "20220903",
    "playDe": "20220903"
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
        tuples = []
        for movie in movies:
            time = movie["playStartTime"]
            seats = movie["restSeatCnt"]
            th = movie["theabExpoNm"]
            tuple = (th,time, seats)
            tuples.append(tuple)

        return tuples

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