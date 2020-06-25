"""Log processes.

The logger can be initialized using function `init_logger`. When the program
closes, the logger is stopped and by default the log is compressed using lzma.

For logging a variety of levels are available:
 - debug
 - info
 - warning
 - error
 - critical
 - exception

The following example shows how and when these can and should be used.
    >>> import logging
    >>> logging.debug('Debug message, too detailed for user.')
    >>> logging.info('Info the user should now.')
    >>> logging.warning('Warning, the user should now this, but not critical.')
    >>> logging.error('An unexpected problem happened.')
    >>> logging.criticial('Critical problem which might cause serious issues.')
    >>> logging.exception('Impossible to run the program due to this error.')
"""

import atexit
import logging
import lzma
import mmap
import os
import time

LOG_PATH_BASE = 'logs'
LOG_FILE_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_STREAM_FORMAT = '%(levelname)s - %(message)s'


def init_logger(
        file_handler: bool = True,
        stream_handler: bool = True,
        file_level: int = logging.DEBUG,
        stream_level: int = logging.DEBUG,
        compress_file: bool = True):
    logger = logging.getLogger()
    logger.setLevel(logging.NOTSET)
    atexit.register(stop_logger)
    if file_handler:
        logger.addHandler(init_file_handler(compress_file, file_level))
    if stream_handler:
        logger.addHandler(init_stream_handler(stream_level))
    logger.debug('Started logger.')
    if file_handler:
        logger.debug('Writing log to file.')
    if stream_handler:
        logger.debug('Streaming log to stdout.')


def init_file_handler(compress: bool = True,
                      level: int = logging.DEBUG) -> logging.FileHandler:
    if not os.path.isdir(LOG_PATH_BASE):
        os.makedirs(LOG_PATH_BASE)
    filepath = os.path.join(LOG_PATH_BASE, str(int(time.time())) + '.log')
    handler = logging.FileHandler(filepath)
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(LOG_FILE_FORMAT))
    if compress:
        atexit.register(compress_log, filepath)
    return handler


def init_stream_handler(level: int = logging.INFO) -> logging.StreamHandler:
    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(LOG_STREAM_FORMAT))
    return handler


def stop_logger():
    logging.debug('Stop logger.')
    logging.shutdown()


def compress_log(filepath: str, delete: bool = True):
    with open(filepath, 'rb+') as f, lzma.open(filepath + '.xz', 'wb') as fz:
        fz.write(mmap.mmap(f.fileno(), 0))
    if delete:
        os.remove(filepath)


__all__ = ('init_logger')
