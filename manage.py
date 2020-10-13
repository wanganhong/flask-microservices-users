#!/usr/bin/env python
# -*- coding:utf-8 -*-


import unittest

import coverage
from flask_script import Manager

from app import create_app, db
from app.api.models import User

app = create_app()
manager = Manager(app)


@manager.command
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@manager.command
def test():
    tests = unittest.TestLoader().discover('app/tests', pattern='test_*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def seed_db():
    db.session.add(User('cnych', email='123@qq.com'))
    db.session.add(User('cnych1', email='1234@qq.com'))
    db.session.commit()


cov_ = coverage.Coverage(
    branch=True,
    include='app/*',
    omit=[
        'app/tests/*'
    ]
)

cov_.start()


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('app/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        cov_.stop()
        cov_.save()
        print('Coverage Summary:')
        cov_.report()
        cov_.html_report()
        cov_.erase()
        return 0
    return 1


if __name__ == '__main__':
    manager.run()
