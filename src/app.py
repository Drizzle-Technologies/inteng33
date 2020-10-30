from flask import Flask, render_template, request, redirect, url_for, flash, session 
from database.database import db
from database.dao import add_device, delete_device, get_user_devices ,retrieve_max_people, search_by_username,\
    validate_password
from database.credentials import access_credentials
from helper.helper import calculate_max_people, is_not_logged_in
import json


# Instanciating Flask class. It will allow us to start our webapp.
app = Flask(__name__, instance_relative_config=True)

# We need the database URI to access the Arduino data in Postgres. This function gets the enviroment variable.
app.config['SQLALCHEMY_DATABASE_URI'] = access_credentials()
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {"pool_pre_ping": True}
app.config['SECRET_KEY'] = 'mandalorian'

# Database connected to the app
db.init_app(app)


# This is how Flask routes work. The app.route decorator sets a route to our site. For example: imagine our app is
# google.com. We can add a route "/images" (google.com/images) to create a new page for image search.

# This is our index, or home page.


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/authenticate', methods=["POST"])
def authenticate():

    username = request.form['username']
    password = request.form['password']

    user = search_by_username(username)

    if user:
        if validate_password(user, password):
            session["logged_in"] = user.ID
            session["user_name"] = user.name

            next_page = request.form["next_page"]

            # Add success login message
            return redirect(next_page)
        else:
            # Add fail login message
            return redirect(url_for("login"))
    else:
        # Add fail login message
        return redirect(url_for("login"))


@app.route('/logout')
def logout():
    session.clear()

    # Change later for index
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():

    if is_not_logged_in(session):
        return redirect(url_for('login', next_page='dashboard'))
    else:
        devices = get_user_devices(session["logged_in"])
        return render_template("dashboard.html", devices=devices)


# This route is used to save new devices on the database. It cannot be directly accessed.

@app.route('/save_device', methods=["POST"])
def save_device():

    # Each form input is saved in a different variable.
    shop_name = request.form['shop_name']
    owner = request.form['owner']
    area = int(request.form['area'])
    max_people = calculate_max_people(area)

    # We then form a tuple, which is roughly an immutable vector.
    new_device = (owner, shop_name, area, max_people)

    # Finally we add the device to the database
    device_added = add_device(new_device)
    if device_added:
        flash("O dispositivo foi adicionado!", "alert-success")

    # And we are redirected to our index page.
    return redirect(url_for('dashboard'))


@app.route('/delete', methods=["POST"])
def delete():
    ID = request.form['device_ID']
    device_deleted = delete_device(ID)
    if device_deleted:
        flash("O dispositivo foi deletado", "alert-danger")

    return redirect(url_for('dashboard'))


# This route is used as an API to the devices information. A GET request is done in this URL, such as
# (localhost/controladores/1) and it retrieves the maximum capacity of the building.

@app.route('/controladores/<ID>')
def get_max_people(ID):
    max_people = retrieve_max_people(ID).max_people
    max_dict = {'max_people': max_people}
    max_poeple_json = json.dumps(max_dict)

    return max_poeple_json


if __name__ == '__main__':

    app.run(debug=True)

