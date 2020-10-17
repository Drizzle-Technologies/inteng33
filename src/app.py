from flask import Flask, render_template, request
from src.database.database import db
from src.database.dao import add_device, get_max_people
from src.helper.helper import calculate_max_people
import json

app = Flask(__name__, instance_relative_config=True)
db.init_app(app)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/save_device')
def save_device():
    shop_name = request.form['shop_name']
    owner = request.form['owner']
    area = request.form['area']
    max_people = calculate_max_people(area)

    new_device = (shop_name, owner, area, max_people)
    add_device(new_device)


@app.route('/controladores/<id>', methods=["POST"])
def get_max_people(id):
    max_people = get_max_people()
    max_poeple_json = json.dumps(f'"max": {max_people}')

    return max_poeple_json


if __name__ == '__main__':

    app.run(debug=True)