import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter, Retry
from selenium import webdriver
from openpyxl import load_workbook
import xlsxwriter

workbook = xlsxwriter.Workbook("America_giaohoi.xlsx")
worksheet = workbook.add_worksheet("data")

with open('html_america.txt', encoding="utf8") as f:
    lines = f.read()
    soup = BeautifulSoup(lines, 'html.parser')
    # print(soup.prettify())
    # print(soup.children)
    mydivs = soup.find("table", {"class": "tb"})
    children = mydivs.findChildren("tr", recursive=False)
    # print(mydivs)
    arr = []
    iaf = 1
    for child in children:
        a = child.findChildren("a")[0]
        link = "http://www.gcatholic.org/dioceses/" + a["href"][3:]

        session = requests.Session()
        retry = Retry(connect=6, backoff_factor=6)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        r = session.get(link)
        r.encoding = r.apparent_encoding
        soup_child = BeautifulSoup(r.text, 'html.parser')

        mydiv_child = soup_child.find("div", {"class": "entries"})


        image_div = soup_child.find("div", {"id": "mapthumb"})
        image_link = image_div.findChildren("img")
        image = "http://www.gcatholic.org" + image_link[0]['src']
        list_att = mydiv_child.findChildren("a")

        list_att_1 = mydiv_child.findChildren("p")
        name_spec = list_att_1[3].findChildren("span")

        continent = list_att[0].string
        rite = list_att[1].string
        type = list_att[2].string
        detail_name = name_spec[2].string
        suffaran_see = list_att[3:len(list_att) - 1]
        suffan = ""
        if len(suffaran_see) == 1:
            suffan = suffaran_see[0].string
        else:
            for sf in suffaran_see:
                suffan = suffan + sf.string + ","
        depen_on = list_att[-1].string

        church_div = soup_child.find("div", {"id": "churches"})
        church_tag = church_div.findChildren("h3")
        church_number = ""
        if len(church_tag) >= 2:
            church_number = church_tag[1].findChildren("span")[0].string
        item = {
            "continent": continent,
            "rite": rite,
            "type": type,
            "name": a.string,
            "detail_name": detail_name,
            "suffan": suffan,
            "church": church_number,
            "depen": depen_on,
            "image": image
        }
        arr.append(item)
        print(continent, rite, type, a.string, detail_name, suffan, church_number, depen_on, image)

# ghi danh sach giao hoi
worksheet.write(0, 0, "Continent")
worksheet.write(0, 1, "Rite")
worksheet.write(0, 2, "Type")
worksheet.write(0, 3, "Name")
worksheet.write(0, 4, "DetailName")
worksheet.write(0, 5, "Suffragan Sees")
worksheet.write(0, 6, "Depends on")
worksheet.write(0, 7, "Church")
worksheet.write(0, 8, "Image")
arr.append(item)
for index, entry in enumerate(arr):
    worksheet.write(index + 1, 0 , entry["continent"])
    worksheet.write(index + 1, 1, entry["rite"])
    worksheet.write(index + 1, 2, entry["type"])
    worksheet.write(index + 1, 3, entry["name"])
    worksheet.write(index + 1, 4, entry["detail_name"])
    worksheet.write(index + 1, 5, entry["suffan"])
    worksheet.write(index + 1, 6, entry["depen"])
    worksheet.write(index + 1, 7, entry["church"])
    worksheet.write(index + 1, 8, entry["image"])
workbook.close()