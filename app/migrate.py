import contextlib
import datetime
import json
import os
import tempfile
import typing
import zipfile

from app.database import cursor
from app.upload import get_file
from app.type import get_server_type, ServerType

EXPORT_FORMAT = typing.Dict[str, typing.Union[str, int]]
EXPORT_FORMAT_MULTI = typing.Tuple[EXPORT_FORMAT]

if get_server_type() == ServerType.DATA:
    from app.database import users, posts, comments, friends, uploads, hobbies, skills, languages


def _store_in_zip(tablename: str, data: EXPORT_FORMAT_MULTI, f: typing.BinaryIO,
                  primary: str='id', file_data: typing.BinaryIO=None):
    if type(f) is not zipfile.ZipFile:
        if f.tell() > 0:
            raise ValueError('Bad file format.')
        f = zipfile.ZipFile(f)
    result = []
    for d in data:
        filename = os.path.join('export', tablename, d[primary])
        if file_data is not None:
            f.writestr(filename, file_data.read())
        filename += '.json'
        if filename in f.namelist():
            raise KeyError('Filename already in zip.')
        for key in d.keys():
            if type(d[key]) is datetime.datetime:
                d[key] = d[key].strftime('%Y-%m-%dT%H:%M:%SZ') # ISO 8601
        f.writestr(filename, bytes(json.dumps(d), 'utf8'))


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
    f = zipfile.ZipFile(tempfile.NamedTemporaryFile(suffix='.zip', delete=False), 'w')
    data = users.export(username=username, as_dict=True)
    _store_in_zip('users', data, f, primary='username')
    if data[0]['uploads_id'] is not None:
        data = uploads.export(id=data[0]['uploads_id'], as_dict=True)
        _store_in_zip('uploads', data, f,
                      file_data=get_file(data[0]['id'], output='fp')[1])
    _store_in_zip('friends', friends.export(username=username, as_dict=True), f)
    _store_in_zip('posts', posts.export(username=username, as_dict=True), f)
    _store_in_zip('comments', comments.export(username=username, as_dict=True), f)
    _store_in_zip('hobbies', hobbies.export(username=username, as_dict=True), f)
    _store_in_zip('skills', skills.export(username=username, as_dict=True), f)
    _store_in_zip('languages', languages.export(username=username, as_dict=True), f)
    f.close()
    return open(f.filename, 'rb')

if get_server_type == ServerType.CENTRAL:
    __all__ = ()
else:
    __all__ = ('export',)

