import argparse
import os


def main(server: str=None, port: int=None):
    if 'FLASK_SERVER_TYPE' not in os.environ:
        os.environ['FLASK_SERVER_TYPE'] = server.upper()
    if 'FLASK_PORT' in os.environ:
        port = os.environ['FLASK_PORT']
    from app import app as application
    application.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server', type=str,
                        required='FLASK_SERVER_TYPE' not in os.environ,
                        help='Server type. Can be \'central\' or \'data\'.')
    parser.add_argument('-p', '--port', type=int, default=5000,
                        help='Port to use. Default is 5000.')
    args = parser.parse_args()
    main(args.server, args.port)

