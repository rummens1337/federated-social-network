import json
import os
import random
import string
import typing
import flask

from flask import current_app, request
import requests


def percent_type(d: typing.Union[str, int]) -> str:
    """"""
    return '%s'


def random_string(length: int=8) -> str:
    return ''.join(random.choices(string.hexdigits, k=length))


def ping(host):
    try:
        pub_key = requests.get(host + '/api/server/pub_key').json()['data']
        if pub_key is None or pub_key is "":
            return False
        return pub_key
    except:
        return False


def get_own_ip():
    """Returns the IP of the current data server"""
    return flask.request.url_root


def get_central_ip():
    """Returns the IP of the central server"""
    return current_app.config['CENTRAL_IP']


def get_user_ip(username):
    """Returns the IP of a data server for a given username"""
    response = requests.get(
        get_central_ip() + '/api/user/address',
        params={
            'username': username
        }
    )

    try:
        return response.json()['data']['address']
    except:
        return False
