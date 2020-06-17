import json

from flask import Response


def response_wrapper(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        r = Response(json.dumps(response), mimetype='application/json')
        return r
    return wrapper


@response_wrapper
def bad_json_response(reason: str) -> str:
    return {
        'success': False,
        'reason': reason
    }


@response_wrapper
def good_json_response(data: dict=None) -> str:
    response = {
        'success': True
    }
    if data is not None:
        response['data'] = data
    return response

__all__ = ('bad_json_response', 'good_json_response')

