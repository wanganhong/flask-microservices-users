#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime

from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    active = db.Column(db.Boolean(), default=False, nullable=False)
    create_at = db.Column(db.DateTime(), nullable=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.create_at = datetime.datetime.utcnow()
