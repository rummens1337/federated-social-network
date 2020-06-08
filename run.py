import argparse
import os


# def main(server: str, port: int):
#     os.environ['SERVER_TYPE'] = server.upper()
#     from app import app as application
#     application.run(host='0.0.0.0', port=port)

if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-s', '--server', type=str, required=True,
    #                     help='Server type. Can be \'central\' or \'data\'.')
    # parser.add_argument('-p', '--port', type=int, default=1337,
    #                     help='Port to use. Default is 1337')
    # args = parser.parse_args()
    # main(args.server, args.port)
    from app import app as application
    application.run(host='0.0.0.0')

