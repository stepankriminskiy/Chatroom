import socket
import threading

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect(('127.0.0.1', 5555)) #Connecting locally just for this showcase. Can use external ip for other to connect outside network


def receive(): #continously runs and prints a message received from the server
    while True:
        msg = socket.recv(1024)
        msg = msg.decode('utf-8')
        print(msg)
def sendOut(): #continously runs checking for inputs and sends it out to the server to handle
    while True:
        message = input('')
        socket.send(message.encode('utf-8'))

thread_receive = threading.Thread(target=receive, args=()) #thread 1 to constantly be running to check for server
thread_receive.start()

thread_send = threading.Thread(target=sendOut, args=()) #constantly runs this thread to check for input to send out
thread_send.start()
