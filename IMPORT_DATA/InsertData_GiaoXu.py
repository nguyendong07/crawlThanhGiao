import pandas as pd
from xlrd import open_workbook
import urllib.parse
import textwrap
import requests
import json
import pyodbc

cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                        "Server=10.10.10.50,1469;"
                        "Database=TD.ThanhGiao;"
                        "uid=tdcongdan;pwd=Tandan@123")
cursor = cnxn.cursor()
def inssertData(list_data):
    for index, row in enumerate(list_data):
        inset_querry = textwrap.dedent('''
        INSERT INTO It_GiaoXu(
            Jurisdiction,
            Served_By,
            Type,
            BasilicaDecree,
            Link_Thumb,
            Rite,
            Lists,
            History,
            Patron,
            Location,
            Address,
            Country,
            Telephone,
            Website,
            GCatholicChurchID,
            MetropolitanArchbishop,
            Name,
            Region,
            Deanery
            )
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''')
        values = (row[0], row[1], row[2], row[3], row[4], row[5], row[6],row[7],row[8], row[9],row[10], row[11],row[12], row[13], row[14],row[15], row[16], row[17], row[18])
        print(inset_querry)
        cursor.execute(inset_querry, values)

    cnxn.commit()
    cursor.execute('SELECT * FROM It_GiaoXu')
    cursor.close()
    cnxn.close()
    print("done")

def readFile(path):
    wwb = open_workbook(path)
    pd.read_excel(path)

    for sheet in wwb.sheets():
        number_of_row = sheet.nrows
        number_of_columns = sheet.ncols
        list_value = []
        for row in range(1, number_of_row):

            values = []
            for col in range(number_of_columns):

                print(number_of_columns)
                value = (sheet.cell(row,col).value)
                values.append(value)
            list_value.append(values)
    return list_value


list_data = readFile("../DATA_ITALIAN/GIAOXU.xlsx")
print(len(list_data))
print(list_data[0])
inssertData(list_data)