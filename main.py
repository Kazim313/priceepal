from flask import Flask, render_template, redirect, request
from api import download_data
import json
import os

app = Flask(__name__)

def update_image_paths(data):
    for item in data['result']['resultList']:
        if 'item' in item and 'image' in item['item']:
            image_url = (item['item']['image']).replace('//ae01.alicdn.com', 'https://ae04.alicdn.com')
            item['item']['image'] = image_url
    return data

@app.route('/search', methods=['POST']) 
def search():
    if request.method == 'POST':
        search_term = request.form['search']
        download_data(search_term)
    return redirect('/')

@app.route('/')
def index():
    #------------------------------------------------
    # Amazon
    path = os.path.dirname(__file__)
    json_file_path = os.path.join(f'{path}\static', 'amazon.json')

    with open(json_file_path, 'r') as file:
        amazon_data = json.load(file)
    # End of Amazon
    #------------------------------------------------
    # Ali Express
    path = os.path.dirname(__file__)
    json_file_path = os.path.join(f'{path}\static', 'ali_express.json')

    with open(json_file_path, 'r') as file:
        ali_express = json.load(file)
    # End of Ali Express
    #------------------------------------------------


    amazon_products = amazon_data['data']['products']
    ali_express = update_image_paths(ali_express)
    ali_express_products = ali_express['result']['resultList']
    

    return render_template('index.html', amazon_products=amazon_products, ali_express_products=ali_express_products)

if __name__ == '__main__':
    app.run(debug=True)
