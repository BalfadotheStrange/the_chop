import csv
from flask import Flask, render_template, request, redirect, jsonify
from geopy.geocoders import MapBox
from geojson import Point, Feature, FeatureCollection, dump

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

 # final list to contain all geocoding addresssssesssss
def your_apartment(num, nsew, name, street): # take in 4 strings seperately to handle formatting
    adlist = [num, nsew, name, street]
    address = ' '.join(adlist).upper()
    with open('good_index.csv', 'r') as file: # all the denver data that wasn't corrupted
        data = csv.reader(file, delimiter=',', quotechar='*')
        for row in data:
            row_address_list = [row[14], row[15], row[16], row[17]]
            row_address = ' '.join(row_address_list)
            if address == row_address:
                tax_address_list = [row[6], row[7], row[8], row[9]]
                tax_address = ' '.join(tax_address_list)
                return tax_address
                



def find_all_owned(tax_addy):
    all_owned = []
    with open('good_index.csv', 'r') as file: # all the denver data
        data = csv.reader(file, delimiter=',', quotechar='*')
        for row in data:
            string_row = ' '.join(row)
            where_you = string_row.find(tax_addy)
            if where_you == -1:  #if your tax address isnt in the row throw it out
                pass
            else:
                all_owned.append(row)
                
        return all_owned


def make_json(properties):
    features = []
    denver = ' Denver, CO'
    for row in properties:
        row_address_list = [row[14], row[15], row[16], row[17], denver]
        print(row_address_list)
        row_address = ' '.join(row_address_list)
        tax_address_list = [row[6], row[7], row[8], row[9], row[10], row[11], row[12]]
        tax_address = ' '.join(tax_address_list)
        locator = MapBox('pk.eyJ1IjoiYmFsZmFkb3J0aGVzdHJhbmdlIiwiYSI6ImNrZmNyNTJvYjB6cnQydXBlZWd4dGN2OHkifQ.fGHNFT7Aqk-dzH_7dp0tUg')
        location = locator.geocode(row_address)   
        map_location = Point((location.longitude, location.latitude))
        features.append(Feature(geometry=map_location, properties={'property_name': ' '.join(row[4]),
                                                                   'property_address' : row_address,
                                                                   'tax_address' : tax_address}))
        feature_collection = FeatureCollection(features)

    with open('static/properties.geojson', 'w') as f:
       dump(feature_collection, f)
        
        

@app.route('/')
def main_page():
    return render_template('index.html')


@app.route('/string:page_name')
def html_page(page_name):
    return render_template(page_name)

@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        data = request.form.to_dict()
        number = data['num']
        nsew = data['nsew']
        street_name = data['street_name']
        street_type = data['street_type']
        make_json(find_all_owned(your_apartment(number, nsew, street_name, street_type)))
        
        return render_template('map.html')
    else:
        return 'whoops'
    

    
