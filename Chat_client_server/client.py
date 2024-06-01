""" Script Python per client multithread per chat asincrone """

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tkt

""" funzione per la ricezione di messaggi dal server """
def receive():
    while True:
        try:
            # la funzione è in ascolto sul socket, in attesa di messaggi
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            # Una volta ricevuti, vengono immagazinati nella msg_list, una ListBox 
            # della parte GUI dalla quale verranno proposti all'utente
            msg_list.insert(tkt.END, msg)
        except OSError:
            break

""" funzione per l'invio dei messaggi al server """
def send(event=None):
    # la funzione estrapola l'input utente da my_msg, parte in GUI in cui l'utente può scrivere
    msg = my_msg.get()
    # Il riquadro di scrittura GUI viene pulito
    my_msg.set("")
    # Il messaggio viene inviato sul socket, anche nel caso contenga il codice d'uscita,
    # così da permettere al server di disconnettere l'utente anche dalla sua parte
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{exit}":
        client_socket.close()
        window.quit()

""" funzione che specifica il comportamento del programma alla chiusura della finestra GUI"""
def on_closing(event=None):
    # Invia il codice d'uscita al server
    my_msg.set("{exit}")
    send()


window = tkt.Tk()
window.title("Chat")

msg_frame = tkt.Frame(window)
# Riquadro di scrittura che permette di inserire un Input all'utente
my_msg = tkt.StringVar()
my_msg.set("")
scrollbar = tkt.Scrollbar(msg_frame)

# Listbox in cui verranno visualizzati i messaggi inviati e ricevuti
msg_list = tkt.Listbox(msg_frame, height=20, width=40, yscrollcommand=scrollbar.set)
msg_list.pack(side=tkt.LEFT, fill=tkt.BOTH)
scrollbar.pack(side=tkt.RIGHT, fill=tkt.Y)
msg_list.pack()
msg_frame.pack()
# Creazione della "variabile" my_msg utilizzata nella funzione send
entry_field = tkt.Entry(window, textvariable=my_msg)
# COllegamento della funzione send al tasto Send della GUI
entry_field.bind("<Return>", send)

entry_field.pack()
# Creazione del tasto Send sulla GUI
send_button = tkt.Button(window, text="Send", command=send)
send_button.pack()

# Protocollo da attuare alla chiusura della finestra GUI
window.protocol("WM_DELETE_WINDOW", on_closing)

# Inizializzazione di HOST e PORT chhe identificano il server a cui connettersi
HOST = input("Enter server host: ")
PORT = input("Enter port number: ")

if not PORT:
    PORT = 53000
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

# Creazione e avvio del thread col compito di ricevere i messaggi dal server
receive_thread = Thread(target=receive)
receive_thread.start()
# Avvia l'esecuzione della Finestra di GUI Chat.
tkt.mainloop()
