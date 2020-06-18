import os
import random
import string
import typing
import requests


def percent_type(d: typing.Union[str, int]) -> str:
    """"""
    return '%s'
    #if type(d) is str:
    #    return '%s'
    #if type(d) is int:
    #    return '%i'


def random_string(length: int=8) -> str:
    return ''.join(random.choices(string.hexdigits, k=length))


def ping(host):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    try:
        requests.get(host + "/index")
        return True
    except:
        return False
