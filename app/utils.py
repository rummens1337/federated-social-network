import os
import random
import string
import typing


def percent_type(d: typing.Union[str, int]) -> str:
    """"""
    if type(d) is str:
        return '%s'
    if type(d) is int:
        return '%i'


def random_string(length: int=8) -> str:
    return ''.join(random.choices(string.hexdigits, k=length))

