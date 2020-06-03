import argparse

from web import run


def main(port: int):
    run(port)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, required=True,
                        help='The port to run the dashboard on.')
    args = parser.parse_args()
    main(args.port)

