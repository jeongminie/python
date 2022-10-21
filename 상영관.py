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

    # print(movie_no_list)

    return movie_no_list

def get_time_table(movies):
    movie_th_list = []

    for item in movies:
        thea = item["theabEngNm"]
        if thea not in movie_th_list:
            movie_th_list.append(thea)
    # print(movie_th_list)
       
    th_list = movie_th_list
    # print(th_list)

    dic={}

    for movie_th in th_list:
        
        movie = [item for item in movies if item["theabEngNm"] == movie_th]
        # print(movie)
        # dic = movie_th
        # print(dic)
        tuples = []
        for i in range(len(movie)):
            time = movie[i]["playStartTime"]
            seats = movie[i]["restSeatCnt"]
            # print(time ,seats)
            tuple = (time, seats)
            tuples.append(tuple)
        # print(tuples)
        # print(movie_th)
        dic[movie_th] = tuples
    
    # print(dic)

    return dic

def split_movies_by_no(response):
    movie_no_list = get_movie_no_list(response)
    
    for movie_no in movie_no_list:
        #print(movie_no)
        movies = [item for item in response if item["movieNo"] == movie_no]
        #print(movies)
        title = movies[0]["movieNm"].replace('&#40;', '(').replace('&#41;', ')')
        #print(title)

        timetable = get_time_table(movies)
        
        # z = zip([title],[timetable]) 
        # for i in z:
	    #     print(i, end = ', ')

        dic[(title, movie_no)] = timetable
    print(dic)

    
        

split_movies_by_no(movie_response)