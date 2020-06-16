import enum
import functools
import os


class ServerType(enum.Enum):
    """Defined server types.

    The currenctly defined server types are:
     * CENTRAL
     * DATA
    """
    CENTRAL = enum.auto()
    DATA = enum.auto()


@functools.lru_cache()
def get_server_type() -> str:
    """Return the type of the server.

    Two types of are defined in enum `ServerType`.

    Returns:
        int: The type of server.
    """
    if 'FLASK_SERVER_TYPE' not in os.environ:
        raise KeyError('FLASK_SERVER_TYPE not set.')
    return ServerType[os.environ['FLASK_SERVER_TYPE'].upper()]

