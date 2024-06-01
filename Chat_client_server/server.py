""" Script Python per server multithread per chat asincrone """

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

""" funzione che gestisce la connessione dei client """
def in_connections_acceptor():
    while True:
        client, client_adress = SERVER.accept()
        print("%s:%s joined the chat" % client_adress)
        # Vengono fornite istruzioni di inizializzazione all'utente
        client.send(bytes("Write your name and confirm with Send", "utf8"))
        indirizzi[client] = client_adress
        Thread(target=client_manager, args=(client,)).start()

""" funzione che gestisce l'esperienza di un singolo client (inizializzazione e invio dei messaggi) """
def client_manager(client):
    name = client.recv(BUFSIZ).decode("utf8")
    # Viene fornito il metodo di uscita dalla chat all'utente
    client.send(bytes("Write {exit} to quit", "utf8"))
    # Utilizzo della funzione broadcast per notificare gli utenti della connessione del nuovo client
    broadcast(bytes(("%s joined" % name), "utf8"))
    clients[client] = name

    # La funzione si mette in ascolto per eventuali messaggi da inviare
    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{exit}", "utf8"):
            broadcast(msg, name + ": ")
        # Chiusura della connessione in caso di ricezione del codice di uscita proposto precedentemente
        else:
            client.close()
            del clients[client]
            broadcast(bytes("%s left the chat" % name, "utf8"))
            break

""" funzione di broadcast per recapitare messaggi a tutti gli utenti """
def broadcast(msg, prefix=""):
    for user in clients:
        user.send(bytes(prefix, "utf8") + msg)

""" Inizializzazione delle variabili necessarie (dizionari e caratteristiche del server vere e proprie)"""
clients = {}
indirizzi = {}

HOST = ""
PORT = 53000
BUFSIZ = 1024
ADDR = (HOST, PORT)

""" Apertura del server """
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

""" Server in ascolto """
if __name__ == "__main__":
    SERVER.listen(10)
    print("Waiting for users...")
    THREAD = Thread(target=in_connections_acceptor)
    THREAD.start()
    THREAD.join()
    SERVER.close()
