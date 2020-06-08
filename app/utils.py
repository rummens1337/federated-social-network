import functools
import os


@functools.lru_cache()
def server_type() -> str:
    if 'FLASK_SERVER_TYPE' not in os.environ:
        raise KeyError('FLASK_SERVER_TYPE not set.')
    result = os.environ['FLASK_SERVER_TYPE'].upper()
    if result not in ('CENTRAL', 'DATA'):
        raise ValueError('Unsupported FLASK_SERVER_TYPE.')
    return result

