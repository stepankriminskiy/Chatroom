import socket
import threading


def handleClient(client, address):
    client.send(welcomeMessage.encode('utf-8'))  # send a welcome message for the newly connected client to receive
    client.send("Please enter a nickname".encode('utf-8')) #asks for connected client to enter name
    nickname = client.recv(1024) #next sent in input is saved as that clients nickname
    client.send("Your nickname is:".encode('utf-8') + nickname) #sends that client its nickname
    print(nickname.decode('utf-8') + " HAS CONNECTED TO THE CHATROOM") #server prints who connected
    SendMessageToClients((nickname + " HAS CONNECTED TO THE CHATROOM".encode('utf-8')), client) #Sends all users who connected
    while True:
        try:
            message = client.recv(1024)  # sit here and wait until receiving a message from client socket
            print(nickname.decode('utf-8') + ":" + message.decode(
                'utf-8'))  # print that message with the clients nickname
            message = nickname + ": ".encode('utf-8') + message
            SendMessageToClients(message, client)  # send that message to every client
        except: #exception if client discconects from server
            clients.remove(client) #removes client from list of clients
            client.close() #closes the socket
            print(nickname.decode('utf-8') + " HAS DISCCONNECTED FROM THE CHATROOM") #prints that user has dc'd
            SendMessageToClients((nickname + " HAS DISCONNECTED FROM THE CHATROOM".encode('utf-8')), client)#sends to all users
            break


def SendMessageToClients(msg, currentClient):
    for client in clients:
        if (
                client != currentClient):  # sends the message back to every other client but the client that sent
            # the message
            client.send(msg)


clients = []  # stores a list of the clients
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # setup server to be a socket
welcomeMessage = "Welcome to the server!"
server.bind(('127.0.0.1', 5555))  # usually leave it as '' so it generate and uses external ip so people outside network can connect

server.listen()  # wait and listen until server receives something from another socket
while True:
    client, address = server.accept()  # whenever a socket connects, get its socket object and address
    clients.append(client)  # add the client socket to the clients list
    thread = threading.Thread(target=handleClient,
                              args=(client, address))  # start a thread for that client under handle client
    thread.start()
