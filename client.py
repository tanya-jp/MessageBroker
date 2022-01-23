import socket
import sys

# HOST = '127.0.0.1'
# HOST = sys.argv[1]
# PORT = sys.argv[2]

MESSAGE_LENGTH_SIZE = 1024
ENCODING = 'ascii'
conn = None


def main():
    if len(sys.argv) <= 3:
        print("INVALID INPUT!")
        sys.exit()
    if sys.argv[1] == "default":
        # HOST = socket.gethostbyname(socket.gethostname())
        HOST = '127.0.0.1'
    else:
        HOST = sys.argv[1]
    if sys.argv[2] == "default":
        PORT = 1373
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


def server_msg(conn: socket.socket):
    conn.settimeout(10.0)
    while True:
        message_length = int(conn.recv(MESSAGE_LENGTH_SIZE).decode(ENCODING))
        msg = conn.recv(message_length)
        # msg = client.recv(1024)
        if not msg:
            continue
        msg = msg.decode(ENCODING)
        print(msg)
        message = msg
        conn.settimeout(None)
        split_msg = message.split()
        if split_msg[0] == "subAck:":
            print("Subscribing on ")
            for m in split_msg[1:]:
                print(m)
        elif msg == "pubAck":
            print("Message published successfully")
            sys.exit()
        elif msg == "INVALID TOPIC!":
            print(msg)
            sys.exit()
        elif split_msg[0] == 'pong':
            # print("PONG!")
            sys.exit()
        elif split_msg[0] == 'ping':
            pong(conn)


def client_msg(conn: socket.socket):
    while True:
        if sys.argv[3] == "subscribe":
            subscribe(conn, sys.argv[4:])
        elif sys.argv[3] == "publish":
            publish(conn, sys.argv[4:])
        elif sys.argv[3] == "ping":
            ping(conn)
        # elif sys.argv[3] == "pong":
        #     pong(conn)
        else:
            print("INVALID INPUT!")
            sys.exit()
        try:
            server_msg(conn)
        except socket.error:
            print("TIMEOUT: No response from server")


def subscribe(conn: socket.socket, message):
    # split_msg = message.split()
    if len(message) < 1:
        print("NO TOPIC DETECTED!")
        print("Please try again.")
        sys.exit()
    msg = "subscribe"
    for m in message:
        msg += " " + m
    send_msg(conn, msg)


def publish(conn: socket.socket, message):
    msg = "publish "
    if len(message) == 0:
        print("NO TOPIC OR MESSAGE DETECTED!")
        sys.exit()
    if len(message) == 1:
        print("NO MESSAGE DETECTED!")
        sys.exit()
    msg += message[0] + " "
    message = message[1:]
    for m in message:
        msg += " " + m
    send_msg(conn, msg)


def ping(client: socket.socket):
    send_msg(client, "ping")


def pong(client: socket.socket):
    send_msg(client, "pong")


if __name__ == '__main__':
    main()
