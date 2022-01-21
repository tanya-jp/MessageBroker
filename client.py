import socket

# HOST = '127.0.0.1'
PORT = 3033
MESSAGE_LENGTH_SIZE = 1024
ENCODING = 'ascii'


def main():
    address = socket.gethostbyname(socket.gethostname())
    SERVER_INFORMATION = (address, PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(SERVER_INFORMATION)
    client_msg(s)
    # send_msg(s, "HELLO WORLD!")
    # send_msg(s, "DISCONNECT")


def send_msg(client, msg):
    message = msg.encode(ENCODING)
    msg_length = len(message)
    msg_length = str(msg_length).encode(ENCODING)
    msg_length += b' ' * (MESSAGE_LENGTH_SIZE - len(msg_length))

    client.send(msg_length)
    client.send(message)


def client_msg(client: socket.socket):
    while True:
        message = input()
        split_msg = message.split()
        if split_msg[0] == "subscribe":
            subscribe(client, message)


def subscribe(client: socket.socket, message):
    split_msg = message.split()
    if split_msg[0] == "subscribe":
        if len(split_msg) < 2:
            print("NO TOPIC DETECTED!")
            print("Please try again.")
            return
        send_msg(client, message)


if __name__ == '__main__':
    main()
