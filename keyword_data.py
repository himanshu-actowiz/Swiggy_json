import json
from datetime import datetime
import mysql.connector

products=[]
base_path = r"C:\Users\hemanshu.marwadi\Desktop\Swiggy_json_data\keyword.json"
basepath="https://instamart-media-assets.swiggy.com/swiggy/image/upload/fl_lossy,f_auto,q_auto,h_600/"

def input_file(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
        # pprint(data)
        return data

def parser(d):
    for i in d["data"]["cards"]:
        key="gridElements"
        if key in i["card"]["card"]:
            for j in i["card"]["card"]["gridElements"]["infoWithStyle"]["items"]:
                for k in j["variations"]:
                    product={}
                    product["name"]=k.get("displayName")
                    product["Prod_id"]=k.get("skuId")
                    product["Prod_price"]=float(k.get("price").get("offerPrice").get("units"))
                    product["Prod_quantity"]=k.get("quantityDescription")
                    product["Image_URL"]=k.get("imageIds")
                    product["Image_URL"]=[basepath+image for image in product["Image_URL"]]
                    if not k.get("price").get("offerApplied").get("listingDescription"):
                        product["Discount_per"]=None
                    else:
                        product["Discount_per"]=int(k.get("price").get("offerApplied").get("listingDescription").split("%")[0])
                    product["mrp"]=float(k.get("price").get("mrp").get("units"))
                    product["In_stock"]=k.get("inventory").get("inStock")

                    products.append(product)
    return products


def convert_to_json(processed_data):
    with open(f"Keyword_{datetime.now().date()}.json","w") as f:
        json.dump(processed_data,f,indent=4)

    print("data extracted successfully")



d=input_file(base_path)
extracted=parser(d)
convert_to_json(extracted)

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database="Extract_Json_Databse"
)

cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS Swiggy_instamart2(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    Prod_id VARCHAR(50) UNIQUE,
    Prod_price DECIMAL(10,2),
    Prod_quantity VARCHAR(100),
    Image_URL JSON,
    Discount_per INT,
    mrp FLOAT,
    In_stock BOOLEAN
    )
""")

for row in extracted:
    cursor.execute("""
    INSERT IGNORE INTO Swiggy_instamart2(
        name,
        Prod_id,
        Prod_price,
        Prod_quantity,
        Image_URL,
        Discount_per,
        mrp,
        In_stock
    ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
    """ ,(
        row.get('name'),
        row.get('Prod_id'),
        row.get('Prod_price'),
        row.get('Prod_quantity'),
        json.dumps(row.get('Image_URL')),
        row.get('Discount_per'),
        row.get('mrp'),
        row.get('In_stock')
    ))

conn.commit()
print("Data Inserted")