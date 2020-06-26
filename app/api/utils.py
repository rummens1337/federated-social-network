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
    """ Returns a negative response wrapper to
        send to a user when a function fails.
    """
    return {
        'success': False,
        'reason': reason
    }


@response_wrapper
def good_json_response(data: dict = None) -> str:
    """ Returns a positive response wrapper to
        send to a user when a function succeeds.
    """
    response = {
        'success': True
    }
    if data is not None:
        response['data'] = data
    return response


__all__ = ('bad_json_response', 'good_json_response')
