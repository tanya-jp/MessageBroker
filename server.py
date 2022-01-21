import socket
import threading

# HOST = '127.0.0.1'
PORT = 5002
MESSAGE_LENGTH_SIZE = 1024
ENCODING = 'ascii'

topics_members = {}
clients = {}


def main():
    address = socket.gethostbyname(socket.gethostname())
    HOST_INFORMATION = (address, PORT)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(HOST_INFORMATION)
    print("[SERVER START] Server is listening ...")
    start(s)


def start(server):
    server.listen()
    while True:
        conn, address = server.accept()
        clients[conn] = 0
        t = threading.Thread(target=handle_client, args=(conn, address))
        t.start()


def send_msg(server, msg):
    message = msg.encode(ENCODING)
    msg_length = len(message)
    msg_length = str(msg_length).encode(ENCODING)
    msg_length += b' ' * (MESSAGE_LENGTH_SIZE - len(msg_length))

    server.send(msg_length)
    server.send(message)


def handle_client(conn, address):
    print("[NEW CONNECTION] connected from {}".format(address))
    Connected = True
    while Connected:
        try:
            message_length = int(conn.recv(MESSAGE_LENGTH_SIZE).decode(ENCODING))
            msg = conn.recv(message_length)
            if not msg:
                continue
            msg = msg.decode(ENCODING)
            print("[MESSAGE RECEIVED] {}".format(msg))
            if msg == "DISCONNECT":
                Connected = False
            else:
                execute_message(msg, conn)
        except:
            remove_client(conn)
            print('Disconnected suddenly by', address)
            break
    conn.close()


def execute_message(msg, conn):
    split_msg = msg.split()
    if split_msg[0] == "subscribe":
        subscribe_handler(conn, split_msg[1:])


def subscribe_handler(conn: socket.socket, message):
    for msg in message:
        if msg in topics_members.keys():
            if conn not in topics_members[msg]:
                topics_members[msg].append(conn)
        else:
            topics_members[msg] = [conn]
    # print(topics_members)
    msg = "subAck:"
    for topic in topics_members.keys():
        if conn in topics_members[topic]:
            msg += " " + topic
    send_msg(conn, msg)


def remove_client(client):
    for tm in topics_members:
        if client in topics_members[tm]:
            topics_members[tm].remove(client)
    client.close()
    print(topics_members)


if __name__ == "__main__":
    main()