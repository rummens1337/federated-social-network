import json
from flask import Response


def bad_json_response(reason: str) -> str:
    response = {
        'success': False,
        'reason': reason
    }
    r = Response(json.dumps(response), mimetype='application/json')
    r.headers['Access-Control-Allow-Origin'] = '*'
    return r




def good_json_response(data: dict=None) -> str:
    response = {
        'success': True
    }
    if data is not None:
        response['data'] = data
    
    r = Response(json.dumps(response), mimetype='application/json')
    r.headers['Access-Control-Allow-Origin'] = '*'
    return r
