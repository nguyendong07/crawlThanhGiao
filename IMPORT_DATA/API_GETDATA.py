import pyodbc
from fastapi import FastAPI

from fastapi.responses import JSONResponse
app = FastAPI()

cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                        "Server=10.10.10.50,1469;"
                        "Database=TD.ThanhGiao;"
                        "uid=tdcongdan;pwd=Tandan@123")
cursor = cnxn.cursor()


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]


@app.get("/giaoxu/{typecountry}/")
async def danhsachgiaoxu(typecountry, giaophan: str = ""):
    rs = {}
    table_name = typecountry + "_GiaoXu"
    cursor.execute(f"select * from {table_name} where Jurisdiction LIKE '%{giaophan}%'")
    list_giaoxu = []
    for row in cursor.fetchall():
        gx = {
            "ID":row[0],
            "Jurisdiction": row[1],
            "Served_By": row[2],
            "Type": row[3],
            "BasilicaDecree": row[4],
            "Link_Thumb": row[5],
            "Rite": row[6],
            "Lists": row[7],
            "History": row[8],
            "Patron": row[9],
            "Location": row[10],
            "Address": row[11],
            "Country": row[12],
            "Telephone": row[13],
            "Website": row[14],
            "GCatholicChurchID": row[15],
            "MetropolitanArchbishop": row[16],
            "Name" : row[17],
            "Region" :row[18],
            "Deanery": row[19]
        }
        list_giaoxu.append(gx)

    rs = {
        "data" : list_giaoxu,
        "count" : len(list_giaoxu),
        "success" : "true"
    }
    return rs

@app.get("/giaoxu/{typecountry}/{id}")
async def danhsachgiaoxu(typecountry, id:str):
    table_name = typecountry + "_GiaoXu"
    cursor.execute(f"select * from {table_name} where ID={id}")
    rs = []
    for row in cursor.fetchall():
        gx = {
            "ID": row[0],
            "Jurisdiction": row[1],
            "Served_By": row[2],
            "Type": row[3],
            "BasilicaDecree": row[4],
            "Link_Thumb": row[5],
            "Rite": row[6],
            "Lists": row[7],
            "History": row[8],
            "Patron": row[9],
            "Location": row[10],
            "Address": row[11],
            "Country": row[12],
            "Telephone": row[13],
            "Website": row[14],
            "GCatholicChurchID": row[15],
            "MetropolitanArchbishop": row[16],
            "Name": row[17],
            "Region": row[18],
            "Deanery": row[19]
        }
        rs.append(gx)
    return rs[0]

@app.get("/giaophan/{typecountry}")
async def danhsachgiaohoi(typecountry):
    table_name = typecountry + "_GiaoPhan"
    cursor.execute(f"select * from {table_name}")
    list_giaohoi = []
    for row in cursor.fetchall():
        gx = {
            "ID": row[0],
            "Continent": row[1],
            "Type": row[2],
            "Rite": row[3],
            "Name": row[4],
            "DetailName": row[5],
            "SuffraganSees": row[6],
            "DependsOn": row[7],
            "Church": row[8],
            "Image": row[9],

        }
        list_giaohoi.append(gx)

    rs = {
        "data": list_giaohoi,
        "count": len(list_giaohoi),
        "success": "true"
    }
    return rs


@app.get("/giaophan/{typecountry}/{id}")
async def danhsachgiaohoi(typecountry, id):
    table_name = typecountry + "_GiaoPhan"
    cursor.execute(f"select * from {table_name} where ID={id}")
    rs = []
    for row in cursor.fetchall():
        gx = {
            "ID": row[0],
            "Continent": row[1],
            "Type": row[2],
            "Rite": row[3],
            "Name": row[4],
            "DetailName": row[5],
            "SuffraganSees": row[6],
            "DependsOn": row[7],
            "Church": row[8],
            "Image": row[9],

        }
        rs.append(gx)
    return rs[0]

#
#
#
