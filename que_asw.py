import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import re
url_base = "https://www.thebump.com/real-answers/v1/categories/33/questions?"
# url_base = "https://www.thebump.com/real-answers/v1/categories/"
js = requests.get("https://www.thebump.com/real-answers/v1/categories/33/questions?page_num=1&page_size=10&filter=ranking").json()
total_que = js["total"]

def get_que_page(page_num, page_size):
    pargram = {
        "page_num" : page_num,
        "page_size" : page_size,
        "filter" : "ranking"
    }
    # url_par = url_base + page_id + "/"
    url = url_base + urlencode(pargram)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print("Error", e.args)

def parse_page(json):
    if json:
        items = json.get("questions")
        for item in items:
            questions = {}
            questions["title"] = item.get("title")
            questions["create_at"] = item.get("create_at")
            questions["user_id"] = item.get("user_id")
            yield questions


if __name__ == "__main__":
       json = get_que_page(1, 2000)
       results = parse_page(json)
       for result in results:
           print(result)

