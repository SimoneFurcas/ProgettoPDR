""" Script Python per server multithread per chat asincrone """

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

""" funzione che gestisce la connesione dei client """


def in_connections_acceptor():
    while True:
        client, client_adress = SERVER.accept()
        indirizzi[client] = client_adress
        print("%s:%s joined the chat" % client_adress)
        client.send(bytes("Write your name and confirm with Send", "utf8"))
        Thread(target=client_manager, args=(client,)).start()


def client_manager(client):
    name = client.recv(BUFSIZ).decode("utf8")
    client.send(bytes("Write {exit} to quit", "utf8"))
    broadcast(bytes(("%s joined" % name), "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{exit}", "utf8"):
            broadcast(msg, name + ": ")
        else:
            client.close()
            del clients[client]
            broadcast(bytes("%s left the chat" % name, "utf8"))
            break


def broadcast(msg, prefix=""):
    for user in clients:
        user.send(bytes(prefix, "utf8") + msg)


clients = {}
indirizzi = {}

HOST = ""
PORT = 53000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(10)
    print("Waiting for users...")
    THREAD = Thread(target=in_connections_acceptor)
    THREAD.start()
    THREAD.join()
    SERVER.close()
