import socket
import argparse
import os
from read import Status
from read import get_status

def parse_args():
    parser = argparse.ArgumentParser(description="Get the status of bots running on the server.")
    parser.add_argument('port', help="Port to bind socket to.")
    return parser.parse_args()

def bind(port):
    s = socket.socket()
    host = socket.gethostname()
    s.bind( (host, port))
    return s

def handle_command(command):
    home = os.path.expanduser('~')
    if command.lower() == 'status reviewbot':
        status = get_status('{}/ReviewBot/review.log'.format(home))
        if status == Status.up:
            return 'up'
        else:
            return 'down'

    elif command.lower() == 'status swapbot':
        status = get_status('{}/SwapBot/swap.log'.format(home))
        if status == Status.up:
            return 'up'
        else:
            return 'down'
    return ''

def main(args):
    connection.listen(5)
    while True:
        print('Waiting for connection...')
        client, addr = connection.accept()
        print('Connected to {}'.format(addr))
        command = client.recv(1024).decode()
        print('Received: {}'.format(command))
        reply = handle_command(command)
        client.send(reply.encode())
        client.close()
        print('Closed connection with {}'.format(addr))

if __name__ == '__main__':
    args = parse_args()
    connection = bind(int(args.port))
    try:
        main(connection)
    except (KeyboardInterrupt, BrokenPipeError):
        print('Closing connection...')
    except:
        raise
    finally:
        connection.close()
