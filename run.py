import argparse
import os


def main(server: str = None, port: int = None):
    """
    Sets the servertype based on environmental variables provided in the run command.
    These variables define the flow of the entire application.
    Starts the application.

    parameters:
    server (str): data | central -> defines which flask server to use.
    port (int): ~5000-54000 -> defines what port to run on.
    """
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
