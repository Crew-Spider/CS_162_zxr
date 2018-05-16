import requests
from bs4 import BeautifulSoup


def sy_page_1(soup):
    news = soup.find_all(name="div", attrs={"class" : "result"})
    for new in news:
        time = new.p.text.split("\xa0")[2]
        url = new.a["href"]
        title = new.a.text
        with open("F:/out.txt", mode="a", encoding="utf-8") as f:
            f.write(time + " " + title + " " + url + "\n")

def sy_n_page(soup, n):
    for i in range(n):
        news = soup.find_all(name="div", attrs={"class" : "result"})
        for new in news:
            time = new.p.text.split("\xa0")[2]
            url = new.a["href"]
            title = new.a.text
            with open("F:/out2.txt", mode="a", encoding="utf-8") as f:
                f.write(time + " " + title + " " + url + "\n")
        next_page_link = "http://news.baidu.com" + soup.find(attrs={"class" : "n"})["href"]
        print(next_page_link)
        html1 = requests.get(next_page_link, "lxml")
        soup = BeautifulSoup(html1.text, "lxml")

if __name__ == "__main__":
    html = requests.get("http://news.baidu.com/ns?ct=1&rn=20&ie=utf-8&bs=http%3A%2F%2Fnews.baidu.com%2Fns%3Fct%3D0%26rn%3D20%26ie%3Dutf-8%26bs%3D%25E4%25B8%258A%25E6%25B5%25B7%25E6%25B5%25B7%25&rsv_bp=1&sr=0&cl=2&f=8&prevct=no&tn=news&word=%E4%B8%8A%E6%B5%B7%E6%B5%B7%E4%BA%8B%E5%A4%A7%E5%AD%A6&rsv_sug3=18&rsv_sug4=815&rsv_sug1=10&inputT=4739")
    soup = BeautifulSoup(html.text, "lxml")
    sy_n_page(soup, 5)


