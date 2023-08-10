import pandas
import requests
from PIL import Image
df = pandas.read_excel('Image_GiaoHoi.xls')

#print the column names
print (df.columns)
#get the values for a given column
values = df['Image'].values
#get a data frame with selected columns
for item in values:
    name = item.split("/")[-1]
    print(name)
    img_data = requests.get(item).content
    with open("C:/Users/WBPC.VN/PycharmProjects/scrapDataWeb/Images_GiaoHoi/" + name, 'wb') as handler:
        handler.write(img_data)
print(values)