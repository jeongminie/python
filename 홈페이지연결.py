from time import time
import requests
from bs4 import BeautifulSoup
import webbrowser
import json


url = "https://www.megabox.co.kr/on/oh/ohz/PcntSeatChoi/selectSeatList.do"
parameters = {
  "playSchdlNo": "2210211372004",
  "brchNo": "1372"
}
response = requests.post(url = url, data = json.dumps(parameters))

resp = requests.get(url=url, data=json.dumps(parameters))
webbrowser.open("https://www.megabox.co.kr/booking?playSchdlNo=2210211372004")
