from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

client = MongoClient('mongodb+srv://lxegydya:admin@cluster0.s4ymqoi.mongodb.net/?retryWrites=true&w=majority')
db = client['lxdb']

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_place', methods=['POST'])
def save_place():
    doc = {
        "place_name" : request.form['place_name'],
        "city_location" : request.form['city_location'],
        "place_categories" : list(map(lambda elm : elm.strip(), request.form['place_categories'].split(","))),
        "longitude" : float(request.form['longitude']),
        "latitude" : float(request.form['latitude'])
    }

    insert_result = db.mymaps.insert_one(doc)
    if(insert_result.inserted_id):
        return jsonify({'isSuccess' : True})
    
    return jsonify({'isSuccess' : False})

@app.route('/places')
def get_places():
    places = list(db.mymaps.find({}, {'_id' : False}))

    return jsonify({'places' : places})

if __name__ == '__main__':
    app.run("0.0.0.0", port=5000, debug=True)