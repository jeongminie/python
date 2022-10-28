from flask import Flask, render_template, redirect, jsonify, url_for
from flask import request
from turtle import title
import requests
from bs4 import BeautifulSoup
from collections import ChainMap
import json
from apscheduler.schedulers.background import BackgroundScheduler
import telegram
import datetime

token = "5648875021:AAEsc8Q86tJhk4hwu2ohLmGQD9gpeYKPRJI"
id = "5669537551"
 
bot = telegram.Bot(token)

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
dic2 = {}

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

    dic={}

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

def check():
    any(key in 'Dolby' for key in dic['블랙 아담'])
    for i in dic['블랙 아담']:
       any(key in 'Dolby' for key in dic['블랙 아담'][i])
    # for key,val in dic.items():
    #     if '블랙아담'.replace(' ','') in key.replace(' ',''):
    #         print({key:val    })

check()

