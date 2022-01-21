import socket
import threading

# HOST = '127.0.0.1'
PORT = 3033
MESSAGE_LENGTH_SIZE = 1024
ENCODING = 'ascii'

members = {}


def main():
    address = socket.gethostbyname(socket.gethostname())
    HOST_INFORMATION = (address, PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(HOST_INFORMATION)
    print("[SERVER START] Server is listening ...")
    start(s)


def send_msg(server, msg):
    message = msg.encode(ENCODING)
    msg_length = len(message)
    msg_length = str(msg_length).encode(ENCODING)
    msg_length += b' ' * (MESSAGE_LENGTH_SIZE - len(msg_length))

    server.send(msg_length)
    server.send(message)


def start(server):
    server.listen()
    while True:
        conn, address = server.accept()
        t = threading.Thread(target=handle_client, args=(conn, address))
        t.start()


def handle_client(conn, address):
    print("[NEW CONNECTION] connected from {}".format(address))
    Connected = True
    while Connected:
        message_length = int(conn.recv(MESSAGE_LENGTH_SIZE).decode(ENCODING))
        msg = conn.recv(message_length).decode(ENCODING)
        print("[MESSAGE RECEIVED] {}".format(msg))
        split_msg = msg.split()
        if split_msg[0] == "subscribe":
            subscribe_handler(conn, split_msg[1:])
        if msg == "DISCONNECT":
            Connected = False
    conn.close()


def subscribe_handler(conn: socket.socket, message):
    for msg in message:
        if msg in members.keys():
            if conn not in members[msg]:
                members[msg].append(conn)
        else:
            members[msg] = [conn]
    print(members)
    msg = "subscribing on :"
    for topic in members.keys():
        if conn in members[topic]:
            msg += " " + topic
    send_msg(conn, msg)


if __name__ == "__main__":
    main()