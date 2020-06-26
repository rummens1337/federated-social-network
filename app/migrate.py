import contextlib
import datetime
import io
import json
import os
import re
import tempfile
import typing
import zipfile

from app.database import cursor
from app.type import get_server_type, ServerType
from app.upload import get_file

EXPORT_FORMAT = typing.Dict[str, typing.Union[str, int]]
EXPORT_FORMAT_MULTI = typing.Tuple[EXPORT_FORMAT]

if get_server_type() == ServerType.DATA:
    from app.database import users, posts, comments, friends, uploads, \
        hobbies, skills, languages


def _store_in_zip(
        tablename: str,
        data: EXPORT_FORMAT_MULTI,
        f: typing.BinaryIO,
        primary: str = 'id',
        file_data: typing.BinaryIO = None
    ):
    if not isinstance(f, zipfile.ZipFile):
        if f.tell() > 0:
            raise ValueError('Bad file format.')
        f = zipfile.ZipFile(f)
    result = []
    for d in data:
        print(tablename, d[primary], d, flush=True)
        filename = os.path.join('export', tablename, str(d[primary]))
        if 'uploads_id' in d and d['uploads_id'] is not None:
            upload_data = uploads.export(id=d['uploads_id'], as_dict=True)
            _store_in_zip('uploads', upload_data, f,
                          file_data=get_file(d['uploads_id'], output='fp')[1])
        if file_data is not None:
            f.writestr(filename, file_data.read())
        filename += '.json'
        if filename in f.namelist():
            raise KeyError('Filename already in zip.')
        for key in d.keys():
            if isinstance(d[key], datetime.datetime):
                d[key] = d[key].isoformat()
        f.writestr(filename, bytes(json.dumps(d), 'utf8'))


def _import_data(tablename: str, data: EXPORT_FORMAT):
    if tablename not in globals():
        raise KeyError('Table does not exist.')
    table = globals()[tablename]
    for key in data.keys():
        if not isinstance(data[key], str):
            continue
        r = re.search(r'^date\(([^\)]+)\)$', data[key])
        if not r:
            continue
        try:
            data[key] = datetime.datetime.fromisoformat(data[key])
        except BaseException:
            continue
    return table.insert(**data)


def import_zip(f: typing.Union[bytes, typing.BinaryIO],
               username: typing.Optional[str] = None):
    if isinstance(f, bytes):
        f = io.BytesIO(f)
    if not isinstance(f, zipfile.ZipFile):
        f = zipfile.ZipFile(f)
    checked = False
    filenames = sorted(
        f.namelist(),
        key=lambda x: {
            'uploads': 0,
            'users': 1,
            'posts': 2,
            'hobbies': 2,
            'skills': 2,
            'languages': 2,
            'friends': 2,
            'comments': 3
        }[x.split('/', 2)[-2]]
    )
    upload_ids = {}
    post_ids = {}
    for filename in filenames:
        data = json.loads(str(f.read(filename), 'utf8'))
        if username is None:
            username = data['username']
        else:
            data['username'] = username
        if username is not None and not checked:
            if users.exists(username=username):
                raise ValueError('User already exists.')
            checked = True
        tablename = filename.rsplit('/', 2)[-2]
        if tablename == 'comments' \
                and not posts.exists(id=data['post_id'], username=username):
            continue
        if tablename in ('users', 'posts') and data['uploads_id'] is not None:
            data['uploads_id'] = upload_ids[data['uploads_id']]
        elif tablename == 'comments':
            data['post_id'] = post_ids[data['post_id']]
        old_id = data.get('id')
        if 'id' in data:
            del data['id']
        new_id = _import_data(tablename, data)
        if tablename == 'uploads':
            upload_ids[old_id] = new_id
        elif tablename == 'posts':
            post_ids[old_id] = new_id


def export_zip(username: str) -> str:
    f = zipfile.ZipFile(
        tempfile.NamedTemporaryFile(suffix='.zip', delete=False),
        'w'
    )
    data = users.export(username=username, as_dict=True)
    _store_in_zip('users', data, f, primary='username')
    _store_in_zip('friends', friends.export(username=username, as_dict=True),
                  f)
    _store_in_zip('posts', posts.export(username=username, as_dict=True), f)
    _store_in_zip('comments', comments.export(username=username, as_dict=True),
                  f)
    _store_in_zip(
        'hobbies',
        hobbies.export(
            username=username,
            as_dict=True),
        f)
    _store_in_zip('skills', skills.export(username=username, as_dict=True), f)
    _store_in_zip('languages',
                  languages.export(username=username, as_dict=True), f)
    f.close()
    return open(f.filename, 'rb')


if get_server_type == ServerType.CENTRAL:
    __all__ = ()
else:
    __all__ = ('export_zip', 'import_zip')
