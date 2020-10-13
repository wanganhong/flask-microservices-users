#!/usr/bin/env python
# -*- coding:utf-8 -*-


import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    settings = os.getenv('APP_SETTINGS')
    # app.config.from_object('app.config.DevelopmentConfig')
    app.config.from_object(settings)

    db.init_app(app)

    from app.api.views import users_blueprint
    app.register_blueprint(users_blueprint)

    return app
