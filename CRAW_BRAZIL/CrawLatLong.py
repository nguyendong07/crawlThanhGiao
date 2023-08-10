import time
import webbrowser

import requests
import timeunit
from requests.adapters import HTTPAdapter
from urllib3 import Retry
from bs4 import BeautifulSoup
import pandas
import xlsxwriter
from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from selenium.webdriver.chrome.options import Options
import math

new = 2 # open in a new tab, if possible
import bs4
import webbrowser
workbook = xlsxwriter.Workbook("../DATA_BRAZIL/GIAOXU.xlsx")
worksheet = workbook.add_worksheet("data4")
df = pandas.read_excel('../DATA_BRAZIL/location_split.xls')
values = df['Location'].values
list_toa_do = []


try:
    for value in values:
            # options = Options()
            # ua = UserAgent()
            # userAgent = ua.random
            # print(userAgent)
            # options.add_argument(f'user-agent={userAgent}')
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
            lat = ""
            long = ""
            # driver.get("https://www.google.co.in")

            id = ""
            res=isinstance(value, str)
            if str(res) == "True":
                if value != "":
                    if len(value.split(",")) > 1:
                        print(value.split(","))
                        id = value.split(',')[1]
                    else:
                        id = value
            if id != "":
                print(id)
                my_url = 'https://www.google.com/maps/place/' + id.split("+")[0] + "%2B" + id.split("+")[1]
                print(my_url)
                session = requests.Session()
                retry = Retry(connect=6, backoff_factor=6)
                adapter = HTTPAdapter(max_retries=retry)
                session.mount('http://', adapter)
                session.mount('https://', adapter)
                driver.implicitly_wait(10)
                r = driver.get(my_url)
                time.sleep(10)
                print(driver.current_url)
                if len(driver.current_url.split("/"))  > 5 :
                    current_url_lat_long = driver.current_url.split("/")[6].split(',')
                    print(current_url_lat_long)
                    lat = current_url_lat_long[0].replace("@","")
                    long = current_url_lat_long[1]
                    item = {
                            "lat": lat,
                            "long": long,
                            "index" : value
                        }
                    list_toa_do.append(item)
                    print(lat, long)
                elif len(id) < 2 :
                    lat = "1"
                    long = "1"
                    item = {
                        "lat": lat,
                        "long": long,
                        "index" : value
                    }
                    list_toa_do.append(item)
                    print(lat, long)

                driver.quit()
except Exception:
    worksheet.write(0, 0, "lat")
    worksheet.write(0, 1, "long")
    worksheet.write(0, 2, "index")
    for index, entry in enumerate(list_toa_do):
        worksheet.write(index + 1, 0, entry["lat"])
        worksheet.write(index + 1, 1, entry["long"])
        worksheet.write(index + 1, 2, entry["index"])
    workbook.close()


            # # r.encoding = r.apparent_encoding
            # soup_child = BeautifulSoup(r.text, 'html.parser')
            # print(soup_child.prettify())
            # meta_list = soup_child.findChildren("meta")
            # toado = ""
            # print(meta_list)
            # found_meta_type_0 = []
            # found_meta_type_1 = []
            # for meta_tag in meta_list:
            #     print(found_meta_type_0)
            #     if "https://maps.google.com/maps/api/staticmap?center=" in str(meta_tag):
            #         found_meta_type_0.append(found_meta_type_0)
            #     elif "//geo0.ggpht.com/cbk?cb_client=" in str(meta_tag):
            #         found_meta_type_1.append(meta_tag)
            #
            # if len(found_meta_type_0)==2:
            #     toado = str(found_meta_type_0[0]['content']).split('/')[-1].split("?")[1].split("&")[0].split("=")[1].split("%2C")
            #     print(toado)
            #     lat = toado[0]
            #     long = toado[1]
            #     item = {
            #         "lat": lat,
            #         "long": long
            #     }
            #     list_toa_do.append(item)
            #     print(lat, long)
            # elif len(found_meta_type_1)==2:
            #     toado = str(found_meta_type_1[0]['content']).split('/')[-1].split("?")[1].split("&")[0].split("=")[1].split("%2C")
            #     print(toado)
            #     lat = toado[0]
            #     long = toado[1]
            #     item = {
            #         "lat": lat,
            #         "long": long
            #     }
            #     list_toa_do.append(item)
            #     print(lat, long)






worksheet.write(0, 0, "lat")
worksheet.write(0, 1, "long")
worksheet.write(0, 2, "index")

for index, entry in enumerate(list_toa_do):
    worksheet.write(index + 1, 0 , entry["lat"])
    worksheet.write(index + 1, 1, entry["long"])
    worksheet.write(index + 1, 2, entry["index"])
workbook.close()

