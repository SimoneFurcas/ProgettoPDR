""" Script Python per client multithread per chat asincrone """

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tkt


def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkt.END, msg)
        except OSError:
            break


def send(event=None):
    msg = my_msg.get()
    my_msg.set("")
    if msg == "{exit}":
        client_socket.close()
        window.quit()
    else:
        client_socket.send(bytes(msg, "utf8"))


def on_closing(event=None):
    my_msg.set("{quit}")
    send()


window = tkt.Tk()
window.title("Chat")

msg_frame = tkt.Frame(window)
my_msg = tkt.StringVar()
my_msg.set("...")
scrollbar = tkt.Scrollbar(msg_frame)

msg_list = tkt.Listbox(msg_frame, height=20, width=40, yscrollcommand=scrollbar.set)
msg_list.pack(side=tkt.LEFT, fill=tkt.BOTH)
scrollbar.pack(side=tkt.RIGHT, fill=tkt.Y)
msg_list.pack()
msg_frame.pack()

entry_field = tkt.Entry(window, textvariable=my_msg)
entry_field.bind("<Return>", send)

entry_field.pack()
send_button = tkt.Button(window, text="Send", command=send)
send_button.pack()

window.protocol("WM_DELETE_WINDOW", on_closing)


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

receive_thread = Thread(target=receive)
receive_thread.start()
# Avvia l'esecuzione della Finestra Chat.
tkt.mainloop()
