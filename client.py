import socket
import sys

# HOST = '127.0.0.1'
# HOST = sys.argv[1]
# PORT = sys.argv[2]

MESSAGE_LENGTH_SIZE = 1024
ENCODING = 'ascii'
conn = None


def main():
    if sys.argv[1] == "default":
        HOST = socket.gethostbyname(socket.gethostname())
    else:
        HOST = sys.argv[1]
    if sys.argv[2] == "default":
        PORT = 5005
    else:
        PORT = sys.argv[2]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER_INFORMATION = (HOST, int(PORT))
    s.connect(SERVER_INFORMATION)
    client_msg(s)


def send_msg(client, msg):
    message = msg.encode(ENCODING)
    msg_length = len(message)
    msg_length = str(msg_length).encode(ENCODING)
    msg_length += b' ' * (MESSAGE_LENGTH_SIZE - len(msg_length))

    client.send(msg_length)
    client.send(message)


def server_msg(client: socket.socket):
    client.settimeout(10.0)
    while True:
        message_length = int(client.recv(MESSAGE_LENGTH_SIZE).decode(ENCODING))
        msg = client.recv(message_length)
        # msg = client.recv(1024)
        if not msg:
            continue
        msg = msg.decode(ENCODING)
        print(msg)
        message = msg
        client.settimeout(None)
        split_msg = message.split()
        if split_msg[0] == "subAck:":
            print("Subscribing on ")
            for m in split_msg[1:]:
                print(m)
        elif msg == "pubAck":
            print("Message published successfully")
            sys.exit()
        elif msg == "INVALID TOPIC!":
            sys.exit()

        elif split_msg[0] == 'pong':
            print("PONG!")
            break
        elif split_msg[0] == 'ping':
            pong(client)


def client_msg(client: socket.socket):
    while True:
        # message = input()
        # split_msg = message.split()
        if sys.argv[3] == "subscribe":
            # print(sys.argv[4:])
            subscribe(client, sys.argv[4:])
        elif sys.argv[3] == "publish":
            publish(client, sys.argv[4:])
        try:
            server_msg(client)
        except socket.error:
            print("TIMEOUT: No response from server")


def subscribe(client: socket.socket, message):
    # split_msg = message.split()
    if len(message) < 2:
        print("NO TOPIC DETECTED!")
        print("Please try again.")
        return
    msg = "subscribe"
    for m in message:
        msg += " " + m
    send_msg(client, msg)


def publish(client: socket.socket, message):
    msg = "publish "
    msg += message[0] + " "
    message = message[1:]
    for m in message:
        msg += " " + m
    send_msg(client, msg)


def ping(client: socket.socket):
    send_msg(client, "ping")


def pong(client: socket.socket):
    send_msg(client, "pong")


if __name__ == '__main__':
    main()
