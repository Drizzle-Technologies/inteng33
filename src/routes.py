from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask import current_app as app
import datetime

from .database.dao import add_device, delete_device, add_user, get_user_devices ,retrieve_max_people,\
                         search_by_username, validate_password, update_area, insert_occupancy, update_current_occupancy

from .helper.helper import calculate_max_people, is_not_logged_in


# This is how Flask routes work. The app.route decorator sets a route to our site. For example: imagine our app is
# google.com. We can add a route "/images" (google.com/images) to create a new page for image search.

@app.route('/login')
def login():
    """Login page"""
    return render_template("login.html")


@app.route('/authenticate', methods=["POST"])
def authenticate():
    """This route authenticates the information inserted in the login page."""

    # Getting username and password from form
    username = request.form['username']
    password = request.form['password']

    # Searching user object by the username
    user = search_by_username(username)

    # If the user exists
    if user:
        # Checking password
        if validate_password(user, password):

            # Creating session for the user.
            session["logged_in"] = user.ID
            session["user_name"] = user.name

            # Which should be the next page to be redirected?
            next_page = request.form["next_page"]

            # Flash success login message
            flash(f"{user.name} fez login", "alert-success")
            return redirect(next_page)
        else:
            # Password is wrong. Flash 'incorrect password' message
            flash("Senha incorreta. Tente novamente.", "alert-danger")
            return redirect(url_for("login"))
    else:
        # User does not exist. Flashing 'user does not exist' message
        flash("Usuario nao existe. Tente novamente.", "alert-danger")
        return redirect(url_for("login"))


@app.route('/logout')
def logout():
    # Clearing session
    session.clear()
    return redirect('/')


@app.route('/dashboard')
def dashboard():
    """This route displays the user's dashboard with a form to add new devices and a table showing all of the user's
    devices."""

    # Can't access if not logged in
    if is_not_logged_in(session):
        # Redirected to login with next_page being the dashboard
        return redirect(url_for('login', next_page='dashboard'))
    else:
        # User is logged in, so he can access the dashboard

        # Gets user's devices list to display on table
        devices = get_user_devices(session["logged_in"])
        return render_template("dashboard.html", devices=devices, user_name=session["user_name"],
                               user_id=session["logged_in"])


@app.route('/create_user', methods=['POST'])
def create_user():
    """This route creates a new user."""

    # Gets name, username, and password assigned to new user
    name = request.form['new_name']
    username = request.form['new_username']
    password = request.form['new_password']

    values = (name, username, password)

    success = add_user(values)

    # Flashes success message
    if success:
        flash("Usuário foi criado.", "alert-success")

    return redirect(url_for('dashboard'))


@app.route('/save_device', methods=["POST"])
def save_device():
    """This route is used to save new devices on the database. It cannot be directly accessed."""

    # Each form input is saved in a different variable.
    ID_user = session["logged_in"]
    shop_name = request.form['shop_name']
    area = int(request.form['area'])
    max_people = calculate_max_people(area)

    # We then form a tuple, which is roughly an immutable vector.
    new_device = (ID_user, shop_name, area, max_people)

    # Finally we add the device to the database
    device_added = add_device(new_device)
    if device_added:
        flash("O dispositivo foi adicionado!", "alert-success")

    # And we are redirected to our index page.
    return redirect(url_for('dashboard'))


@app.route('/edit_area', methods=["POST"])
def edit_area():
    """This route is used to edit a device's area"""

    # Get device's ID and new area
    ID = int(request.form["device_ID_editArea"])
    new_area = int(request.form["new_area"])

    update_success = update_area(ID, new_area)

    if update_success:
        flash("O valor da área foi atualizado.", "alert-success")

    return redirect(url_for('dashboard'))


@app.route('/delete', methods=["POST"])
def delete():
    """This route is used to delete a device"""

    # Gets device's ID
    ID = request.form['device_ID_delete']

    device_deleted = delete_device(ID)
    if device_deleted:
        flash("O dispositivo foi deletado", "alert-danger")

    return redirect(url_for('dashboard'))


@app.route('/get_max_people/<ID>')
def get_max_people(ID):
    """This route is used as an API to the devices information. A GET request is done in this URL, such as
    localhost/controladores/1) and it retrieves the maximum capacity of the building."""

    # Gets device's max number of people
    max_people = retrieve_max_people(ID).max_people
    max_dict = {'max_people': max_people}

    # Transforms dictionary into json and sends it
    return jsonify(max_dict)


@app.route('/add_occupancy', methods=["POST"])
def add_occupancy():
    """This route adds a new occupancy record to the DeviceOccupancy table and updates current_occupancy in the Device
    table."""

    # Gets the json
    occupancy_json = request.get_json()

    # Accesses each of the information provided
    ID_device = occupancy_json['id']
    occupancy = occupancy_json['occupancy']
    timestamp = datetime.datetime.now().isoformat()

    # Inserts values in DeviceOccupancy and updates Device's current_occupancy column
    insert_values = (ID_device, timestamp, occupancy)
    update_values = (ID_device, occupancy)

    insert_occupancy(insert_values)
    update_current_occupancy(update_values)

    # Returns the json to confirm the success
    return jsonify(occupancy_json)


