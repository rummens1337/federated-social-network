import argparse

from web import run


def main(port: int, server_type: str):
    run(port, server_type)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, required=True,
                        help='The port to run the dashboard on.')
    parser.add_argument('-s', '--server', type=str, required=True,
                        help='Type of server to run. Must be \'central\' or '
                        '\'data\'.')
    args = parser.parse_args()
    if args.server not in ('central', 'data'):
        raise ValueError('Server should be \'central\' or \'data\'.')
    main(args.port, args.server)

