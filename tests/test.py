from flask_testing import TestCase
from datetime import datetime
import json

from wsgi import app
from src import db
from src.database.dao import add_user, add_device, insert_occupancy


class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app.config.from_object('config.TestConfig')
        return app

    def setUp(self):

        add_user(("test", "test", "test123"))
        add_user(("admin", "admin", "admin123"))
        add_device((1, 'test_shop', 100, 120))
        insert_occupancy((1, datetime.now().isoformat(), 3))

    def tearDown(self):
        meta = db.metadata
        for table in reversed(meta.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()


class AppTestCase(BaseTestCase):
    def login(self, username, password):
        return self.client.post('/authenticate',
                                data={'username': username, 'password': password, 'next_page': '/dashboard'},
                                follow_redirects=True)

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_login_page_load(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_login_auth_correct(self):
        response = self.login('test', 'test123')
        self.assertIn(b'fez login', response.data)

    def test_login_auth_username_incorrect(self):
        response = self.login('test' + 'x', 'test123')
        self.assertIn(b'Usuario nao existe', response.data)

    def test_login_auth_password_incorrect(self):
        response = self.login('test', 'test123' + 'x')
        self.assertIn(b'Senha incorreta.', response.data)

    def test_logout(self):
        response = self.client.get('/logout', follow_redirects=True)
        self.assertIn(b'Contribua no GitHub', response.data)

    def test_dashboard_protection(self):
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assertIn(b'Senha', response.data)

    def test_dashboard_content(self):
        self.login('test', 'test123')
        response = self.client.get('/dashboard')
        self.assertIn(b'test_shop', response.data)

    def test_create_new_user(self):
        self.login('admin', 'admin123')
        self.client.get('/edit_area',
                        data={'new_name': 'test1', 'new_username': 'test1', 'new_password': 'test1'},
                        follow_redirects=True)
        response = self.client.get('dashboard')
        self.assertIn(b'admin', response.data)

    def test_save_device(self):
        self.login('test', 'test123')
        response = self.client.post('/save_device',
                                    data={
                                          'shop_name': 'test_shop_2',
                                          'area': 100,
                                    },
                                    follow_redirects=True)
        self.assertIn(b'test_shop_2', response.data)

    def test_edit_area(self):
        self.login('test', 'test123')
        response = self.client.post('/edit_area',
                                    data={'device_ID_editArea': 1, 'new_area': '200'},
                                    follow_redirects=True)
        self.assertIn(b'240', response.data)

    def test_delete_device(self):
        self.login('test', 'test123')
        response = self.client.post('/delete',
                                    data={'device_ID_delete': 1},
                                    follow_redirects=True)
        self.assertIn(b'O dispositivo foi deletado', response.data)

    def test_get_max_people(self):
        response = self.client.get('/get_max_people/1')
        max_people = response.json['max_people']
        self.assertEqual(max_people, 120)

    def test_add_occupancy(self):
        data = {'id': 1, 'occupancy': 5}
        response = self.client.post('/add_occupancy',
                                    data=json.dumps(data),
                                    content_type='application/json')
        self.assertEqual(5, response.json["occupancy"])
