import json
import datetime

current_date = datetime.date.today()

product_list = []
product_dict = dict()
def read_json_data(json_file):
    with open(json_file,"r") as file:
        json_data = json.load(file)
        return json_data
def extract_json_data(raw_json_data):
    for i in raw_json_data['data']['cards']:
        for j in i['card']['card']['gridElements']['infoWithStyle']['items']:
            for p_id in j['variations']:
                product_dict['product_name'] = p_id['displayName']
                product_dict['Product ID'] = p_id.get('skuId')
                product_dict['Product Price'] = float(p_id['price']['offerPrice']['units'])
                product_dict['Product quantity'] = p_id.get('quantityDescription')
                base_url = "https://instamart-media-assets.swiggy.com/"
                product_dict['Product Image Url'] = p_id.get('imageIds')
                product_dict['Product Image Url'] = [base_url + image for image in product_dict['Product Image Url']]
                product_dict['Discount percentage'] = int(str(p_id['price']['offerApplied']["listingDescription"]).split("%")[0])
                product_dict['Product Mrp'] = float(p_id['price']['mrp']['units'])
                product_dict['is_available'] = p_id['inventory']['inStock']
                product_list.append(product_dict)
    return product_list
                
def convert_json_file(extract_json):
    with open(f"SWIGGY_{current_date}.json","w") as files:
        json.dump(extract_json,files,indent=4)
    
file = input("enter file name: ")    
raw_json_data = read_json_data(file)
extract_json = extract_json_data(raw_json_data)
convert_json_file(extract_json)
    