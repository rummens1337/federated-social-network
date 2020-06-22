import json
import tempfile
import typing
import zipfile

from app.database import cursor
from app.upload import get_file
from app.type import get_server_type, ServerType

EXPORT_FORMAT = typing.Dict[str, typing.Union[str, int]]
EXPORT_FORMAT_MULTI = typing.Tuple[EXPORT_FORMAT]

if get_server_type() == ServerType.DATA:
    from app.database import users, posts, friends, uploads


def _store_in_zip(tablename: str, data: EXPORT_FORMAT_MULTI, f: typing.BinaryIO,
                  primary: str='id',
                  file_data: typing.BinaryIO=None) -> typing.Tuple[int]:
    if type(f) is not zipfile.ZipFile:
        if f.tell() > 0:
            raise ValueError('Bad file format.')
        f = zipfile.ZipFile(f)
    result = []
    for d in data:
        filename = os.path.join(tablename, d[primary])
        if file_data is not None:
            result.append(f.writestr(filename, file_data.read()))
        filename += '.json'
        if filename in f.namelist():
            raise KeyError('Filename already in zip.')
        result.append(f.writestr(filename, bytes(json.dumps(data), 'utf8')))
    return tuple(result)


#def _import_data(tablename: str, data: EXPORT_FORMAT) -> typing.Tuple[int]:
#    if tablename not in globals():
#        raise KeyError('Table does not exist.')
#    table = globals()[tablename]
#    return table.insert(**d)


#def import_zip(f: typing.Union[str, typing.BinaryIO]):
#    if type(f) is not zipfile.ZipFile:
#        f = zipfile.ZipFile(f)
#    for filename in f.namelist():
#        data = json.loads(str(f.read(filename), 'utf8'))
#        if 'id' in data:
#            del data['id']
#        tablename = filename.rsplit('/', 2)[-2]
#        _import_data(tablename, data)


def export(username: str) -> typing.BinaryIO:
    f = zipfile.ZipFile(tempfile.NamedTemporaryFile(suffix='.zip'))
    data = users.export(username=username, as_dict=True)
    _store_in_zip('users', data, f, primary='username')
    if data['uploads_id'] is not None:
        data = uploads.export(id=data['uploads_id'], as_dict=True)
        _store_in_zip('uploads', data, f,
                      file_data=get_file(data['id'], output='fp')[1])
    _store_in_zip('friends', friends.export(username=username, as_dict=True), f)
    _store_in_zip('posts', posts.export(username=username, as_dict=True), f)
    return f

if get_server_type == ServerType.CENTRAL:
    __all__ = ()
else:
    __all__ = ('export',)

