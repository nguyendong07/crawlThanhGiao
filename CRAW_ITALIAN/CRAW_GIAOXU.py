# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter, Retry
from selenium import webdriver
from openpyxl import load_workbook
import xlsxwriter
import COMMON_URL
import DOWNLOAD_IMAGE


workbook = xlsxwriter.Workbook("../DATA_ITALIAN/GIAOXU.xlsx")
worksheet = workbook.add_worksheet("data")

def remove_firstindex(str):
    if str != "":
        return str.replace(str[0], "")
    else:
        return str


with open('../DATA_ITALIAN/html.txt', encoding="utf8") as f:
    lines = f.read()
    soup = BeautifulSoup(lines, 'html.parser')
    mydivs = soup.find("table", {"class": "tb"})
    children = mydivs.findChildren("tr", recursive=False)
    arr = []
    for child in children:
        try:
            a = child.findChildren("a")[0]
            retry = Retry(connect=6, backoff_factor=6)
            adapter = HTTPAdapter(max_retries=retry)
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

            church_div = soup_child.find("div", {"id": "churches"})
            church_tag = church_div.findChildren("h3")
            church_number = ""
            if len(church_tag) >= 2:
                church_number = church_tag[1].findChildren("span")[0].string
                church_link = church_tag[1].findChildren("a")[0]["href"].replace("../../", "http://www.gcatholic.org/")

                print(church_link)
                r = requests.get(church_link)
                session_detail = requests.Session()
                retry_detail = Retry(connect=6, backoff_factor=2)
                adapter = HTTPAdapter(max_retries=retry_detail)
                session_detail.mount('http://', adapter)
                session_detail.mount('https://', adapter)
                r = session_detail.get(church_link)
                r.encoding = r.apparent_encoding
                sp = BeautifulSoup(r.text, 'html.parser')
                tble = sp.find("table", {"class": "tb"})
                list_church = tble.findChildren("tr", recursive=False)
                item_not_link = tble.findChildren("tr", {"class": "tbhd"})
                # print(len(item_not_link))
                for i in item_not_link:
                    list_church.remove(i)
                # list_church.remove(list_church[0]);
                # print(len(list_church))
                for church in list_church:
                    id = church["id"]
                    city = church.findChildren("span")[0].string
                    link_church_deltail = church.findChildren("a")[0]["href"].replace("../","http://www.gcatholic.org/churches/")
                    Name = church.findChildren("a")[1].string
                    chuch_detail = requests.get(link_church_deltail)
                    chuch_detail.encoding = chuch_detail.apparent_encoding
                    chuch_detail_html = BeautifulSoup(chuch_detail.text, 'html.parser')

                    div_name = chuch_detail_html.find("div", {"class": "hd"})
                    Name_Church = div_name.findChildren("h1")[0].string

                    if "Region" in str(chuch_detail_html.findChildren("span", {"class" :"label"})):
                        print("Adayroi",link_church_deltail)



                    div_thumb = chuch_detail_html.find("div", {"id": "mapthumbbig"})
                    if div_thumb:
                        Link_Thumb = "http://www.gcatholic.org" + div_thumb.findChildren("img")[0]["src"]
                        DOWNLOAD_IMAGE.download(Link_Thumb,COMMON_URL.LIST_IMAGES_GIAOXU.get("ITALIAN"))

                    div_entries = chuch_detail_html.find("div", {"class": "entries"})

                    list_att_p = div_entries.findChildren("p")

                    for p in list_att_p:
                        if p.string == "&nbsp;":
                            list_att_p = list_att_p.remove(p)
                    # for p in list_att_p :
                    #     if not p.content:
                    #         list_att_p.remove(p)

                    print(len(list_att_p))
                    Region = ""
                    Deanery = ""
                    Served_By = ""
                    Type = ""
                    BasilicaDecree = ""

                    Rite = ""
                    Lists = ""
                    History = ""
                    Patron = ""
                    Location = ""
                    Address = ""
                    Country = ""
                    Telephone = ""
                    Website = ""
                    GCatholicChurchID = ""
                    MetropolitanArchbishop = ""

                    Jurisdiction = list_att_p[0].contents[1] + list_att_p[0].find("a").string

                    for att_detail in list_att_p:
                        # print("Served by" in str(att_detail.findChildren("span", {"class":"label"})))
                        if "Served by" in str(att_detail.findChildren("span", {"class": "label"})):
                            if att_detail.find("a"):
                                for att in att_detail.findChildren("a"):
                                    Served_By = Served_By + "," + att.string
                                    # Served_By = remove_firstindex(Served_By)
                        if "Type" in str(att_detail.findChildren("span", {"class": "label"})):
                            if att_detail.find("a"):
                                for att in att_detail.findChildren("a"):
                                    Type = Type + "," + att.string
                                    Type = remove_firstindex(Type)
                        if "Deanery" in str(att_detail.findChildren("span", {"class": "label"})):
                            if att_detail.find("a"):
                                for att in att_detail.findChildren("a"):
                                    Deanery = Deanery + "," + att.string
                                    Deanery = remove_firstindex(Deanery)

                        if "Basilica Decree" in str(att_detail.findChildren("span", {"class": "label"})):
                            BasilicaDecree = att_detail.contents[1].string

                        if "Region" in str(att_detail.findChildren("span", {"class": "label"})):
                            Region = att_detail.contents[1].string

                        if "Rite" in str(att_detail.findChildren("span", {"class": "label"})):
                            if att_detail.find("a"):
                                for att in att_detail.findChildren("a"):
                                    Rite = Rite + "," + att.string
                                    Rite = remove_firstindex(Rite)
                        if "Lists" in str(att_detail.findChildren("span", {"class": "label"})):
                            if att_detail.find("a"):
                                for att in att_detail.findChildren("a"):
                                    Lists = Lists + "," + att.string
                        if "History" in str(att_detail.findChildren("span", {"class": "label"})):
                            if att_detail.findChildren("span", {"class": "znote"}):
                                History = att_detail.findChildren("span", {"class": "znote"})[0].contents[0]
                                # print(att_detail.findChildren("span", {"class": "znote"})[0].contents[0])
                        if "Patron" in str(att_detail.findChildren("span", {"class": "label"})):
                            Patron = att_detail.contents[1]
                        if "Location" in str(att_detail.findChildren("span", {"class": "label"})):
                            if att_detail.find("a"):
                                for att in att_detail.findChildren("a"):
                                    Location = Location + "," + att.string
                                    Location = remove_firstindex(Location)
                        if "Address" in str(att_detail.findChildren("span", {"class": "label"})):
                            if att_detail.contents[1]:
                                Address = att_detail.contents[1] + "," + att_detail.find("span",
                                                                                         {"class": "zregion"}).string
                            else:
                                Address = att_detail.find("span", {"class": "zregion"}).string
                        if "Country" in str(att_detail.findChildren("span", {"class": "label"})):
                            if att_detail.find("a"):
                                Country = att_detail.findChildren("a")[0].string
                        if "Telephone" in str(att_detail.findChildren("span", {"class": "label"})):
                            Telephone = att_detail.contents[1]
                        if "Website" in str(att_detail.findChildren("span", {"class": "label"})):
                            Website = att_detail.find("a")["href"]
                        if "GCatholic Church ID" in str(att_detail.findChildren("span", {"class": "label"})):
                            GCatholicChurchID = att_detail.find("a").string
                        # if "Metropolitan Archbishop" in str(att_detail.findChildren("span", {"class": "label"})):
                        #     MetropolitanArchbishop = att_detail.find("a",{"class":"prelA"}).contents[0]
                        item = {
                            "Region": Region,
                            "Deanery": Deanery,
                            "Name": Name_Church,
                            "Jurisdiction": Jurisdiction,
                            "Served_By": Served_By,
                            "Type": Type,
                            "BasilicaDecree": BasilicaDecree,
                            "Link_Thumb": Link_Thumb,
                            "Rite": Rite,
                            "Lists": Lists,
                            "History": History,
                            "Patron": Patron,
                            "Location": Location,
                            "Address": Address,
                            "Country": Country,
                            "Telephone": Telephone,
                            "Website": Website,
                            "GCatholicChurchID": GCatholicChurchID,
                            "MetropolitanArchbishop": MetropolitanArchbishop
                        }
                    arr.append(item)

                    print(Region,Deanery, Name_Church,Jurisdiction, Served_By, Type, BasilicaDecree, Link_Thumb, Rite, Lists, History, Patron,
                          Location,
                          Address, Country, Telephone, Website, GCatholicChurchID, MetropolitanArchbishop)
        except Exception:
            worksheet.write(0, 0, "Jurisdiction")
            worksheet.write(0, 1, "Served_By")
            worksheet.write(0, 2, "Type")
            worksheet.write(0, 3, "BasilicaDecree")
            worksheet.write(0, 4, "Link_Thumb")
            worksheet.write(0, 5, "Rite")
            worksheet.write(0, 6, "Lists")
            worksheet.write(0, 7, "History")
            worksheet.write(0, 8, "Patron")
            worksheet.write(0, 9, "Location")
            worksheet.write(0, 10, "Address")
            worksheet.write(0, 11, "Country")
            worksheet.write(0, 12, "Telephone")
            worksheet.write(0, 13, "Website")
            worksheet.write(0, 14, "GCatholicChurchID")
            worksheet.write(0, 15, "MetropolitanArchbishop")
            worksheet.write(0, 16, "Name")
            worksheet.write(0, 17, "Region")
            worksheet.write(0, 18, "Deanary")

            for index, entry in enumerate(arr):
                worksheet.write(index + 1, 0, entry["Jurisdiction"])
                worksheet.write(index + 1, 1, entry["Served_By"])
                worksheet.write(index + 1, 2, entry["Type"])
                worksheet.write(index + 1, 3, entry["BasilicaDecree"])
                worksheet.write(index + 1, 4, entry["Link_Thumb"])
                worksheet.write(index + 1, 5, entry["Rite"])
                worksheet.write(index + 1, 6, entry["Lists"])
                worksheet.write(index + 1, 7, entry["History"])
                worksheet.write(index + 1, 8, entry["Patron"])
                worksheet.write(index + 1, 9, entry["Location"])
                worksheet.write(index + 1, 10, entry["Address"])
                worksheet.write(index + 1, 11, entry["Country"])
                worksheet.write(index + 1, 12, entry["Telephone"])
                worksheet.write(index + 1, 13, entry["Website"])
                worksheet.write(index + 1, 14, entry["GCatholicChurchID"])
                worksheet.write(index + 1, 15, entry["MetropolitanArchbishop"])
                worksheet.write(index + 1, 16, entry["Name"])
                worksheet.write(index + 1, 17, entry["Region"])
                worksheet.write(index + 1, 18, entry["Deanery"])
            workbook.close()
            print(
                '\nSection: Function to Create Instances of WebDriver\nCulprit: random.choice(ua_strings)\nIndexError: {}\n'.format(
                    Exception))

worksheet.write(0, 0, "Jurisdiction")
worksheet.write(0, 1, "Served_By")
worksheet.write(0, 2, "Type")
worksheet.write(0, 3, "BasilicaDecree")
worksheet.write(0, 4, "Link_Thumb")
worksheet.write(0, 5, "Rite")
worksheet.write(0, 6, "Lists")
worksheet.write(0, 7, "History")
worksheet.write(0, 8, "Patron")
worksheet.write(0, 9, "Location")
worksheet.write(0, 10, "Address")
worksheet.write(0, 11, "Country")
worksheet.write(0, 12, "Telephone")
worksheet.write(0, 13, "Website")
worksheet.write(0, 14, "GCatholicChurchID")
worksheet.write(0, 15, "MetropolitanArchbishop")
worksheet.write(0, 16, "Name")
worksheet.write(0, 17, "Region")
worksheet.write(0, 18, "Deanary")
for index, entry in enumerate(arr):
    worksheet.write(index + 1, 0, entry["Jurisdiction"])
    worksheet.write(index + 1, 1, entry["Served_By"])
    worksheet.write(index + 1, 2, entry["Type"])
    worksheet.write(index + 1, 3, entry["BasilicaDecree"])
    worksheet.write(index + 1, 4, entry["Link_Thumb"])
    worksheet.write(index + 1, 5, entry["Rite"])
    worksheet.write(index + 1, 6, entry["Lists"])
    worksheet.write(index + 1, 7, entry["History"])
    worksheet.write(index + 1, 8, entry["Patron"])
    worksheet.write(index + 1, 9, entry["Location"])
    worksheet.write(index + 1, 10, entry["Address"])
    worksheet.write(index + 1, 11, entry["Country"])
    worksheet.write(index + 1, 12, entry["Telephone"])
    worksheet.write(index + 1, 13, entry["Website"])
    worksheet.write(index + 1, 14, entry["GCatholicChurchID"])
    worksheet.write(index + 1, 15, entry["MetropolitanArchbishop"])
    worksheet.write(index + 1, 16, entry["Name"])
    worksheet.write(index + 1, 17, entry["Region"])
    worksheet.write(index + 1, 18, entry["Deanery"])
workbook.close()

# if list_att_p[1].find("a"):
#     Served_By = list_att_p[1].find("a").string
#     # print("do dai list served by", len(list_att_p[1].find("a")))
#
# if list_att_p[2].find("a") :
#    for type_item in list_att_p[2].find("a"):
#        Type = type_item.string + ","
# Type = remove_lastindex(Type)
#
# if list_att_p[3].find("a"):
#     for basilica_item in list_att_p[3].find("a"):
#         BasilicaDecree = basilica_item.string + ","
# BasilicaDecree = remove_lastindex(BasilicaDecree)
#
# if list_att_p[4].find("a"):
#     for rite_item in list_att_p[4].find("a"):
#         Rite = rite_item.string + ","
# Rite = remove_lastindex(Rite)
#
# if list_att_p[5].find("a"):
#     for lists_item in list_att_p[5].find("a"):
#         Lists = lists_item.string + ","
# Lists = remove_lastindex(Lists)
#
# if list_att_p[6].find("a"):
#     for history_item in list_att_p[6].find("a"):
#         History = history_item.string + ","
# History = remove_lastindex(History)
#
# if list_att_p[7].find("a"):
#     for patron_item in list_att_p[7].find("a"):
#         Patron = patron_item.string + ","
# Patron = remove_lastindex(Patron)
#
# if list_att_p[8].find("a"):
#     for location_item in list_att_p[8].find("a"):
#         Location = location_item.string + ","
# Location = remove_lastindex(Location)
#
# if list_att_p[9].find("a"):
#     for address_item in list_att_p[9].find("a"):
#         Address = address_item.string + ","
# Address = remove_lastindex(Address)
#
# if len(list_att_p)>10:
#     if list_att_p[10].find("a"):
#         for country_item in list_att_p[10].find("a"):
#             Country = country_item.string + ","
#     Country = remove_lastindex(Country)
# if len(list_att_p) > 11:
#     if list_att_p[11].find("a"):
#         for tele_item in list_att_p[11].find("a"):
#             Telephone = tele_item.string + ","
#     Telephone = remove_lastindex(Telephone)
#
# if list_att_p[12].find("a"):
#     for web_item in list_att_p[12].find("a"):
#         Website = web_item.string + ","
# Website = remove_lastindex(Website)
#
# if list_att_p[13].find("a"):
#     for GCatholicChurchID_item in list_att_p[13].find("a"):
#         GCatholicChurchID = GCatholicChurchID_item.string + ","
# GCatholicChurchID = remove_lastindex(GCatholicChurchID)
#
# if list_att_p[14].find("a"):
#     for MetropolitanArchbishop_item in list_att_p[14].find("a"):
#         MetropolitanArchbishop = MetropolitanArchbishop_item.string + ","
# MetropolitanArchbishop = remove_lastindex(MetropolitanArchbishop)


# print(id, city , link_church_deltail, name)

# print(sp.prettify())
# church_number = church_number.replace(")","").replace("(","")

# list_att = mydiv_child.findChildren("a")
# list_att_1 = mydiv_child.findChildren("p")
# name_spec = list_att_1[3].findChildren("span")
#
# continent = list_att[0].string
# rite = list_att[1].string
# type = list_att[2].string
# detail_name = name_spec[2].string
# suffaran_see = list_att[3:len(list_att) - 1]
# suffan = ""
# if len(suffaran_see) == 1:
#     suffan = suffaran_see[0].string
# else:
#     for sf in suffaran_see:
#         suffan = suffan + sf.string + ","
# depen_on = list_att[-1].string
# item = {
#     "continent": continent,
#     "rite": rite,
#     "type": type,
#     "name": a.string,
#     "detail_name": detail_name,
#     "suffan": suffan,
#     "church": church_number,
#     "depen": depen_on,
#     "image": image
# }
# arr.append(item)
# print(continent, rite, type, a.string, detail_name, suffan, church_number, depen_on, image)

# ghi danh sach giao hoi
# worksheet.write(0, 0, "Continent")
# worksheet.write(0, 1, "Rite")
# worksheet.write(0, 2, "Type")
# worksheet.write(0, 3, "Name")
# worksheet.write(0, 4, "DetailName")
# worksheet.write(0, 5, "Suffragan Sees")
# worksheet.write(0, 6, "Depends on")
# worksheet.write(0, 7, "Church")
# worksheet.write(0, 8, "Image")
# arr.append(item)
# for index, entry in enumerate(arr) :
#     worksheet.write(index + 1, 0 , entry["continent"])
#     worksheet.write(index + 1, 1, entry["rite"])
#     worksheet.write(index + 1, 2, entry["type"])
#     worksheet.write(index + 1, 3, entry["name"])
#     worksheet.write(index + 1, 4, entry["detail_name"])
#     worksheet.write(index + 1, 5, entry["suffan"])
#     worksheet.write(index + 1, 6, entry["depen"])
#     worksheet.write(index + 1, 7, entry["church"])
#     worksheet.write(index + 1, 8, entry["image"])
# workbook.close()


link = "http://www.gcatholic.org/dioceses/diocese/amar1.htm"
