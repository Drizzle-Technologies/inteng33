def calculate_max_people(area):
    return area/3


def is_not_logged_in(session):
    return 'logged_in' not in session or session['logged_in'] is None
