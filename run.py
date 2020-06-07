import argparse

from app import run_central, run_data


def main(server: str, port: int):
    if server == 'central':
        run_central(port)
    elif server == 'data':
        run_data(port)
    elif server == 'base':
        run_base(port)
    else:
        raise ValueError('Server type is not supported.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server', type=str, required=True,
                        help='Server type. Can be \'central\' or \'data\'.')
    parser.add_argument('-p', '--port', type=int, default=1337,
                        help='Port to use. Default is 1337')
    args = parser.parse_args()
    main(args.server, args.port)

