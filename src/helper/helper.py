def calculate_max_people(area):
    stadard_capacity = area*2

    # This numbers are defined for the 4th level of flexibilization of São Paulo state quarantine
    pandemic_capacity = stadard_capacity * 0.6
    return int(pandemic_capacity)


def is_not_logged_in(session):
    return 'logged_in' not in session or session['logged_in'] is None
