import socket, struct, threading
from SocketMessageIOFile import SocketMessageIO, MessageType
from ClientGUIFile import ClientGUI
import tkinter as tk
from tkinter import ttk




def listen_for_messages(connection: socket):

    while keep_listening:
        try:
            type, message = manager.receive_message_from_socket(connection)
        except:
            continue
        print(f"{type=}\t{message=}")
        if type == MessageType.MESSAGE:
            print(f"MSG: {message}")
            client_gui.add_to_chat(message)
        elif type == MessageType.USER_LIST:
            update_user_list(message)
            print("------------------")
            for i in range(len(user_list)):
                print(f"{i}\t{user_list[i]}")
            print("------------------")
            client_gui.set_user_list(user_list)

    print("listen_for_messages is over.")

def update_user_list(message: str)->None:
    global user_list
    print(f"{message=}")

    parts = message.split("\t")
    print(f"{parts=}")
    user_list.clear()
    num_users = int(parts[0])
    for i in range(1,num_users+1):
        user_list.append(parts[i])
    client_gui.set_user_list(parts[1:0])

def send_message(message:str):
    manager.send_message_to_socket(message, mySocket)

def close_socket():
    global keep_listening
    keep_listening = False
    mySocket.close()


if __name__ == '__main__':


    global manager, user_list, client_gui, mySocket, listener_thread, keep_listening
    client_gui = ClientGUI()
    user_list = []
    mySocket = socket.socket()
    manager = SocketMessageIO()
    name = input("What is your name? ")

    port = 3000
    mySocket.connect(('127.0.0.1', port))
    # print (mySocket.recv(1024).decode())
    # print (f"Sending {len(name)=}")
    manager.send_message_to_socket(name, mySocket)
    # acknowledgement = manager.receive_message_from_socket(mySocket)
    # print(acknowledgement)
    keep_listening = True
    listener_thread = threading.Thread(target=listen_for_messages, args=(mySocket,))
    listener_thread.start()

    #telling the GUI about two methods in this class that it can call.
    client_gui.message_sender = send_message
    client_gui.shut_down_socket = close_socket


    client_gui.run_loop()

