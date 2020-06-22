import hashlib
import os
import typing

from app.type import get_server_type, ServerType
from app.utils import random_string

BASE_UPLOADS_DIR = os.path.join('data', 'uploads')


def save_file_data(filedata: typing.Union[typing.BinaryIO, bytes],
                   filename: typing.Optional[str]=None,
                   extension: typing.Optional[str]=None,
                   sha256: bool=False) -> str:
    """Save a file.

    Saves a file using a file pointer or a bytes string. The filename is
    optional. If the filename is not is not set, a random filename will be
    chosen, with the set extension if this is given.

    To each filename, a random string of hex digits is appended, so the filename
    is ensured to be unique.

    Note:
        In case a filename and extension are given, the extension will be
        appended to the filename.

    Example:
        The following two examples show the differences in saving a file using a
        filenames with the extension appended and using a filename without
        extension, but with extension given as argument.

        >>> save_file_data(filedata: b'test', filename='test.txt')
        '/data/uploads/text.txt_faB2bED7'
        >>> save_file_data(filedata: b'test', filename='test', extension='txt')
        '/data/uploads/text_9ebBEBDF.txt'

    Args:
        filename (str): The filename to save the file under.
        extension (str): The extension to append to the filename. This is not
            required when a filename including extension is already given.

    Returns:
        (str, str): The location and sha256 hash of the saved file.
        str: The location of the saved file.
    """
    if not os.path.isdir(BASE_UPLOADS_DIR):
        os.makedirs(BASE_UPLOADS_DIR)
    if filename is None:
        filename = random_string(8)
    result = None
    while result is None or os.path.isfile(result):
        result = BASE_UPLOADS_DIR + filename + '_' + random_string(8)
        if extension is not None:
            results += '.' + extension
    if sha256:
        digest = hashlib.sha256()
    with open(result, 'wb') as f:
        if type(filedata) is bytes:
            f.write(filedata)
            if sha256:
                digest.update(filedata)
        else:
            while True:
                buf = filedata.read(100*1024)
                if sha256:
                    digest.update(buf)
                if buf is None:
                    break
                f.write(buf)
    if sha256:
        return (result, digest.hexdigest())
    return result


def verify_file(filepath: str, sha256: str):
    digest = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while True:
            buf = f.read(100*1024)
            if buf is None:
                break
            digest.update(buf)
    return digest.hexdigest() == sha256

if get_server_type() == ServerType.DATA:
    from app.database import uploads


    def save_file(filedata: typing.Union[typing.BinaryIO, bytes],
                  filename: typing.Optional[str]=None,
                  extension: typing.Optional[str]=None,
                  type: str='REPLACE_ME') -> int:
        """Save a file and register in database `uploads` table.

        Example:


        Args:
            args: see the arguments from function `save_file_data`.
            kwargs: the keys (str) for user_id and type for the `uploads` table.

        Returns:
            str: The location of the saved file.
        """
        filepath, digest = save_file_data(filedata, filename=filename,
                                          extension=extension, sha256=True)
        if filename is None:
            filename = os.path.basename(filepath)
        elif extension is not None:
            filename += '.' + extension

        if os.path.getsize(filepath) == 0:
            return False

        return uploads.insert(filename=filename, location=filepath, type=type,
                              filesize=os.path.getsize(filepath), sha256=digest)


    def get_file(id: int, output: str='bytes', verify: bool=False):
        """Get a file from the database and saved location.

        Retrieves a file using a query to the database and opening, and possibly
        reading the file from disk.

        Note:
            Only one row in the database should match the search query, else an
            exception is raised.

        Args:
            output (str): The type of output. This can be 'bytes' to read the
                whole file, or 'filepointer' to get the pointer to the opened
                saved file.
            kwargs: The arguments for requesting data from the database.

        Returns:
            (str, bytes): The original filename and filedata in bytes.
            (str, fp): The original filenamd the pointer to the opened file.
        """
        find = uploads.export('filename', 'location', 'sha256', id=id)
        if len(find) == 0:
            raise ValueError('Uploaded data not found.' )
        if len(find) > 1:
            raise ValueError('Multiple candidates for uploaded data found.')
        filename, location, sha256 = find[0]
        if verify and not verify_file(location, sha256):
            raise ValueError('File has bad sha256 digest.')
        f = open(location, 'rb')
        if output == 'bytes':
            read = f.read()
            f.close()
            return (filename, read)
        if output in ('filepointer', 'fp'):
            return (filename, f)
        raise ValueError('Invalid value for argument \'output\'.')

