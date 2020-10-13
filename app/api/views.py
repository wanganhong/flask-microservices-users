#!/usr/bin/env python
# -*- coding:utf-8 -*-


from flask import Blueprint, jsonify, request, render_template
from sqlalchemy import exc

from app import db
from app.api.models import User

users_blueprint = Blueprint('users', __name__, template_folder='./templates')


@users_blueprint.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong'
    })


@users_blueprint.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    if not data:
        response_data = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_data), 400

    username = data.get('username')
    email = data.get('email')
    try:
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username, email=email)
            db.session.add(user)
            db.session.commit()
            response_data = {
                'status': 'success',
                'message': '{} was added'.format(username)
            }
            return response_data, 201

        response_data = {
            'status': 'fail',
            'message': 'Sorry. user {} already exists.'.format(username)
        }
        return response_data, 400
    except exc.IntegrityError:
        db.session.rollback()
        response_data = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_data), 400


@users_blueprint.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    response_data = {
        'status': 'fail',
        'message': 'User not exists.'
    }
    code = 404
    try:
        user = User.query.filter_by(id=int(user_id)).first()
        if user:
            response_data = {
                'status': 'success',
                'data': {
                    'username': user.username,
                    'email': user.email,
                    'create_at': user.create_at
                }
            }
            code = 200
    except ValueError:
        response_data = {
            'status': 'fail',
            'message': 'Param id error.'
        }
        code = 400
    return jsonify(response_data), code


@users_blueprint.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    us = []
    for user in users:
        us.append(
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'create_at': user.create_at
            }
        )
    response_data = {
        'status': 'success',
        'data': {
            'users': us
        }
    }
    return jsonify(response_data), 200


@users_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        db.session.add(User(username=username, email=email))
        db.session.commit()
    users = User.query.order_by(User.create_at.desc()).all()
    return render_template('index.html', users=users)
