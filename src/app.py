from flask import Flask, render_template, request, redirect, url_for
from database.database import db
from database.dao import add_device, get_max_people
from database.credentials import access_credentials
from helper.helper import calculate_max_people
import json

app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = access_credentials()
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}

db.init_app(app)

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/save_device', methods=["POST"])
def save_device():
    shop_name = request.form['shop_name']
    owner = request.form['owner']
    area = int(request.form['area'])
    max_people = calculate_max_people(area)

    new_device = (owner, shop_name, area, max_people)
    add_device(new_device)

    return redirect(url_for('index'))


@app.route('/controladores/<id>', methods=["POST"])
def get_max_people(id):
    max_people = get_max_people()
    max_poeple_json = json.dumps(f'"max": {max_people}')

    return max_poeple_json


if __name__ == '__main__':

    app.run(debug=True)