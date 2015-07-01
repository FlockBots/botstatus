import socket
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Get the status of bots running on the server.")
    parser.add_argument('host', help="Hostname to connect to.")
    parser.add_argument('port', help="Port to connect to.")
    parser.add_argument('--command', help="Command to send to server.")
    return parser.parse_args()

def connect(host, port):
    s = socket.socket()
    s.connect( (host, port))
    return s

def main(connection, host, command=None):
    if not command:
        command = input('{}:: '.format(args.host))
    connection.send(command.encode())
    status = connection.recv(1024)
    print(status.decode())
    connection.close()

if __name__ == '__main__':
    args = parse_args()
    try:
        connection = connect(args.host, int(args.port))
        main(connection, args.host, args.command)
    except (KeyboardInterrupt, BrokenPipeError):
        pass
    except:
        print('down')
        raise
    finally:
        connection.close()