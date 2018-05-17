import requests
from urllib.parse import urlencode
import csv
from bs4 import BeautifulSoup
import re
# url_base = "https://www.thebump.com/real-answers/v1/categories/33/questions?"
url_base = "https://www.thebump.com/real-answers/v1/categories/"
#得到总数
def get_total(chl_json):
    return chl_json["total"]

#返回父类和子类的js
def get_page(page_id, page_num, page_size):
    page_num = "" + str(page_num)
    page_id = "" + str(page_id)
    pargram = {
        "page_num" : page_num,
        "page_size" : page_size,
        "filter" : "ranking"
    }
    #37 , 47中子分类可能为空
    url_par = url_base + page_id
    url_chl = url_base + page_id + "/" + "questions?"  + urlencode(pargram)
    try:
        response_par = requests.get(url_par)
        response_chl = requests.get(url_chl)
        if response_par.status_code == 200 and response_chl.status_code == 200:
            par_json = response_par.json()
            chl_json = response_chl.json()
            return par_json, chl_json
        else:
            print("接收错误")
    except requests.ConnectionError as e:
        print("Error" + e.args)
#整合json
def parse_page(par_json, chl_json):
    if par_json and chl_json:
        chl_items = chl_json.get("questions")
        for chl_item in chl_items:
            questions = {}
            if par_json["id"] <= 35 and par_json["id"] >= 33:
                questions["category_name"] = "PREGNANCY"
                questions["subcategory_name"] = par_json.get("name")
            elif par_json["id"] >= 37 and par_json["id"] <= 47:
                questions["category_name"] = "PARENTING"
                questions["subcategory_name"] = par_json.get("name")
            elif par_json["id"] == 23 or par_json["id"] == 24:
                questions["category_name"] = "PREGNANCY"
                questions["subcategory_name"] = par_json.get("name")

            questions["title"] = chl_item.get("title")
            questions["create_at"] = chl_item.get("created_at")
            questions["user_id"] = chl_item.get("user_id")
            questions["user_name"] = chl_item.get("user")["username"]
            yield questions

if __name__ == "__main__":
    #init_num 为一页爬取的条数
    #page_id 为分类的id
    #page_num 为当前分类的页数
    headers = ["category_name", "subcategory_name", "title", "create_at", "user_id", "user_name"]
    with open("F:/questions7.csv", mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, headers)
        for i in range(33, 48):   #分类的id号
            init_num = 1000
            page_id = i
            page_num = 1
            if get_page(page_id, page_num, 1):
                par_json, chl_json = get_page(page_id, page_num, 1)
                total = get_total(chl_json)
            else:
                continue
            print(total)
            if get_page(page_id, page_num, 1): #改为total
                print("爬取中....")
                while total > 0:
                    if get_page(page_id, page_num, 1):
                        par_json, chl_json = get_page(page_id, page_num, init_num)
                        results = parse_page(par_json, chl_json)
                        print("写入中....")
                        for result in results:
                            writer.writerow(result)
                        if total - init_num > 0:
                           total -= init_num
                           print("1total " + str(total))
                           print("1init_num" + str(init_num))
                        elif total - init_num//10 > 0:
                            total -= init_num//10
                            init_num //= 10
                            print("2total :" + str(total))
                            print("2init_num/10" + str(init_num))
                            if init_num == 0:
                                break
                        else:
                            break
                        page_num += 1
                    else:
                        continue
            else:
                 continue


