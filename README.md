# inteng33

Web application developed for the Introduction to Electrical Engineering final project.

Link to heroku demo: https://inteng33.herokuapp.com/

## Introduction to the Problem

As we write this document (Nov 5th 2020) the pandemic is slowly ending. People are starting
to get back to their normal lives and want to seize the moments they couldn't during lockdown.
However, a small porcentage of these people are causing big crowds in shops, restaurants, and bars,
which still can't serve clients at its full capacity. The maximum capacity of each building is
currently defined depending on the level of reopening each city is.

See https://www.saopaulo.sp.gov.br/planosp/ for more information. The project would be limited for
the city of São Paulo for now since the group has not collected information about the level of reopening
of other cities.

## Solution

With this problem in mind, our group decided to create a device that could read how many poeple
were inside a building. It uses two laser beams and two light dependent resistors (LDRs). When
a person goes through the building's, he or she interrupts the beam consecutively. Therefore, the
device can tell in which direction the person is going and compute the data. By having the area of
the building, we can tell what is the max capacity and create warnings for the user.

In order to provide a better UI for configs to the possible users of this system, we developed this webapp
in Flask and Dash (Python). The index displays tables and graphs about each device for any person who accesses
it. This may be useful for clients who are hoping to go to a certain restaurant, but find out that
they are already full, preventing crowds. There is also a dashboard for the users of the system,
who can create new devices, edit the area

## Arduino Integration

The routes */get_max_people/<ID>* and /add_occupancy exchange data between an Arduino device.
and the webapp. The first route gets the max number of people that can stay in the building. The second
route receives the number of people that are in the building.

## Other routes

- /login, /authenticate, /logout deal with user login.
- /save_device, /edit_area, /delete deal with devices management
- /create_user creates new users. Only avaiable if you log in with admin.
- /dashboard displays the dashboard

## Database and Data Access Object (DAO)

The database is also hosted in Heroku. Its access string is stored as an environment variable. There are
three tables stored: user, device, and occupancy.

- User: (name, username, password).
- Device: (ID, user ID, shop name, area, max occupancy, and current_occupancy).
- Occupancy log (hash ID, device ID, timestamp, occupancy).

The group opted to use SQLAlchemy and Flask-SQLAlchemy to access the database. In the DAO, there are
functions to deal with user log in, user management, device management, device consultancy, and
occupancy log consultancy. 

## Index - Plotly Dash

The index does not use Flask. The display of data is done through Plotly's Dash. There is one Dropdown
associated with the graph, which displays the last 100 observations of the occupancy record. The user
chooses a device ID and the graph is rendered. The data table displays information of all devices. If
an occupancy gets close to max_occupancy, the table may be painted yellow or red, 90% and 100%< of the
max occupancy respectively.

