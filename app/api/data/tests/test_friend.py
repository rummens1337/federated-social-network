from flask import Blueprint, request
from app.api.utils import good_json_response, bad_json_response
import requests

# blueprint.route('/add', methods=['POST'])
def test_register():
	url = 'http://localhost:5000/json'    
    resp = requests.get(url)           
    assert resp.status_code == 200
    assert resp.json()["code"] == 1
    print(resp.text)

# blueprint.route('/delete', methods=['POST'])
def test_delete():
    pass

__all__ = ('blueprint')
