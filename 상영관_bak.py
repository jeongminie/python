from time import time
import requests
from bs4 import BeautifulSoup
from collections import ChainMap

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

    #print(movie_no_list)

    return movie_no_list

def get_th_no_list(response) :
    movie_th_list = []
    for item in response:
        movie_no = item["movieNo"]
        th_no = item["theabPopupNo"]
        if th_no not in movie_th_list:
            movie_th_list.append(th_no)
            
    #print(movie_th_list)

    return movie_th_list




def get_time_table(movies):
    tuples = []
    temp = []
    for movie in movies:
        time = movie["playStartTime"]
        seats = movie["restSeatCnt"]
        th = movie["theabExpoNm"]
        tuple = (th)
        tuples.append(tuple)

    print(tuples[0])


    return tuples

def split_movies_by_no(response):
    movie_no_list = get_movie_no_list(response)
    movie_th_list = get_th_no_list(response)
    
    for movie_no in movie_no_list:
        # print(movie_no)
        movies = [item for item in response if item["movieNo"] == movie_no]
        #print(movies)
        title = movies[0]["movieNm"].replace('&#40;', '(').replace('&#41;', ')')
        #print(title)

        tuples = []

        for i,v in enumerate(movies) :
            theabExpoNm = v["theabExpoNm"]
            # print(v)
            tuple = theabExpoNm
            tuples.append(tuple)

        dict1 = {}
        dict1[title] = tuples
        #print(dict1)

        key = list(dict1.keys())[0]
        # print(len(dict1[key]))
        # print(dict1[key][0])
        timetable = get_time_table(movies)

        for i in range(len(dict1[key])):
            #print(dict1[key][i])
            test = {dict1[key][i] : timetable }
            #print(test)
            dict2 = {}
            dict2[dict1[key][i]] = timetable
        #print("-------")  
        #print(dict2)

        
        

split_movies_by_no(movie_response)