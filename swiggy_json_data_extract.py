import mysql.connector
import json
import datetime

current_date = datetime.date.today()
base_path = r'C:\Users\hemanshu.marwadi\Desktop\Swiggy_json_data\data.json'
base_url = "https://instamart-media-assets.swiggy.com/"
product_list = []

def read_json_data(json_file):
    with open(json_file,"r") as file:
        json_data = json.load(file)
        return json_data
def extract_json_data(raw_json_data):
    for i in raw_json_data['data']['cards']:
        for j in i['card']['card']['gridElements']['infoWithStyle']['items']:
            for p_id in j['variations']:
                product_dict= {
                'product_name' : p_id['displayName'],
                'Product ID' : p_id.get('skuId'),
                'Product Price' : float(p_id['price']['offerPrice']['units']),
                'Product quantity' : p_id.get('quantityDescription'),
                'Product Image Url' : [base_url + image for image in p_id['imageIds']],
                'Discount percentage' : int(p_id['price']['offerApplied']["listingDescription"].split("%")[0]),
                'Product Mrp' : float(p_id['price']['mrp']['units']),
                'is_available' : p_id['inventory']['inStock']
                }
                
                product_list.append(product_dict)
    return product_list
                
def convert_json_file(extract_json):
    with open(f"SWIGGY_{current_date}.json","w") as files:
        json.dump(extract_json,files,indent=4)
    

raw_json_data = read_json_data(base_path)
extract_json = extract_json_data(raw_json_data)
convert_json_file(extract_json)

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database="Extract_Json_Databse"
)

cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS Swiggy_instamart1(
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(255),
    product_id VARCHAR(50) UNIQUE,
    product_price DECIMAL(10,2),
    product_quantity VARCHAR(100),
    product_image_urls JSON,
    discount_percentage INT,
    product_mrp FLOAT,
    is_available BOOLEAN
    )
""")

for row in extract_json:
    cursor.execute("""
    INSERT IGNORE INTO Swiggy_instamart1(
        product_name,
        product_id,
        product_price,
        product_quantity,
        product_image_urls,
        discount_percentage,
        product_mrp,
        is_available
    ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
    """ ,(
        row.get('product_name'),
        row.get('Product ID'),
        row.get('Product Price'),
        row.get('Product quantity'),
        json.dumps(row.get('Product Image Url')),
        row.get('Discount percentage'),
        row.get('Product Mrp'),
        row.get('is_available')
    ))

conn.commit()
print("Data Inserted")

    