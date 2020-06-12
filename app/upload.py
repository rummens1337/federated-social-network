import os
import typing

from app.utils import server_type, random_string

BASE_UPLOADS_DIR = os.path.join('data', 'uploads')


def save_file_data(filedata: typing.Union[typing.BinaryIO, bytes],
                   filename: typing.Optional[str]=None,
                   extension: typing.Optional[str]=None) -> str:
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
        The following two example show the differences in saving a file using a
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
    with open(results, 'wb') as f:
        if type(filedata) is bytes:
            f.write(filedata)
            return result
        while True:
            buffer = filedata.read(100*1024)
            if buffer is None:
                break
            f.write(buffer)
    return result

if server_type() == 'DATA':
    from app.database import uploads


    def save_file(*args, **kwargs) -> str:
        """Save a file and register in database `uploads` table.

        Example:
            

        Args:
            args: see the arguments from function `save_file_data`.
            kwargs: the keys (str) for user_id and type for the `uploads` table.

        Returns:
            str: The location of the saved file.
        """
        filepath = save_file_data(*args)
        if filename is None:
            filename = os.path.basename(filepath)
        elif extension is not None:
            filename += '.' + extension
        if 'filename' in kwargs or 'location' in kwargs or 'filesize' in kwargs:
            raise KeyError('filename, location and filesize keys are set'
                           ' automatically and should not be set manually.')
        uploads.insert(**kwargs, filename=filename, location=filepath,
                       filesize=os.path.getsize(filepath))
        return filepath


    def get_file(output: str='bytes',
                 **kwargs) -> typing.Tuple[str, typing.Union[typing.BytesIO, bytes]]:
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
        find = uploads.export('filename', 'location', **kwargs)
        if len(find) == 0:
            raise ValueError('Uploaded data not found.' )
        if len(find) > 1:
            raise ValueError('Multiple candidates for uploaded data found.')
        find = find[0]
        with open(find[1], 'rb') as f:
            if output == 'bytes':
                return (find[0], f.read())
            if output == 'filepointer':
                return (find[0], f)
            raise ValueError('Invalid value for argument \'output\'.')

