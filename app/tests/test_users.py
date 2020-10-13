#!/usr/bin/env python
# -*- coding:utf-8 -*-


import json

from app.tests.base import BaseTestCase
from app import db
from app.api.models import User


def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()


class TestUserService(BaseTestCase):
    def test_users(self):
        response = self.client.get('/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong', data['message'])
        self.assertEqual('success', data['status'])

    def test_add_user(self):
        username = 'cnych'
        email = '123@qq.com'
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict(username=username, email=email)),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('{} was added'.format(username), data['message'])
            self.assertEqual('success', data['status'])

    def test_add_user_invalid_json(self):
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict()),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertEqual('fail', data['status'])

    def test_add_user_invalid_json_keys(self):
        username = 'cnych'
        email = '123@qq.com'
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict(email=email)),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertEqual('fail', data['status'])

        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict(username=username)),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload', data['message'])
            self.assertEqual('fail', data['status'])

    def test_add_user_duplicate_user(self):
        username = 'cnych'
        email = '123@qq.com'
        with self.client:
            self.client.post(
                '/users',
                data=json.dumps(dict(username=username, email=email)),
                content_type='application/json'
            )

            response = self.client.post(
                '/users',
                data=json.dumps(dict(username=username, email=email)),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Sorry. user {} already exists'.format(username), data['message'])
            self.assertEqual('fail', data['status'])

    def test_get_user(self):
        username = 'cnych'
        email = '123@qq.com'
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        with self.client:
            response = self.client.get('/users/{}'.format(user.id))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertTrue('create_at' in data['data'])
            self.assertEqual(username, data['data']['username'])
            self.assertEqual(email, data['data']['email'])
            self.assertEqual('success', data['status'])

    def test_get_user_no_id(self):
        with self.client:
            response = self.client.get('/users/xxx')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Param id error', data['message'])
            self.assertEqual('fail', data['status'])

    def test_get_user_incorrect_id(self):
        with self.client:
            response = self.client.get('/users/-1')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User not exist', data['message'])
            self.assertEqual('fail', data['status'])

    def test_get_users(self):
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual('success', data['status'])
            self.assertTrue('users' in data['data'])

    def test_main_no_users(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No users!', response.data)

    def test_main_with_users(self):
        """有多个用户的场景"""
        add_user('cnych', 'icnych@gmail.com')
        add_user('qikqiak', 'qikqiak@gmail.com')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All Users', response.data)
        self.assertNotIn(b'No users!', response.data)
        self.assertIn(b'cnych', response.data)
        self.assertIn(b'qikqiak', response.data)

    def test_main_add_user(self):
        """前端页面添加一个新的用户"""
        with self.client:
            response = self.client.post(
                '/',
                data=dict(username='cnych', email='cnych@gmail.com'),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'All Users', response.data)
            self.assertNotIn(b'No users!', response.data)
            self.assertIn(b'cnych', response.data)
