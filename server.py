import socket
import threading
import json


server = None
HOST_ADDR = "127.0.0.1"
HOST_PORT = 1234
client_name = " "
clients = []
clients_names = []


# Start server function
def start_server():
    global server, HOST_ADDR, HOST_PORT # code is fine without this

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(socket.AF_INET)
    print(socket.SOCK_STREAM)

    server.bind((HOST_ADDR, HOST_PORT))
    server.listen(5)  # server is listening for client connection

    threading._start_new_thread(accept_clients(server, " "))



def accept_clients(the_server, y):
    while True:
        client, addr = the_server.accept()
        clients.append(client)

        # use a thread so as not to clog the gui thread
        threading._start_new_thread(send_receive_client_message, (client, addr))


# Function to receive message from current client AND
# Send that message to other clients
def send_receive_client_message(client_connection, client_ip_addr):
    global server, client_name, clients, clients_addr
    client_msg = " "

    # send welcome message to client
    client_name  = client_connection.recv(1024).decode()
    welcome_msg = "Welcome " + client_name
    client_connection.send(welcome_msg.encode())

    clients_names.append(client_name)
    # req = client_connection.recv(1024).decode()
    # if req == "":
    #     client_connection.send(client_name)
    # #client_connection.send(client_name.encode())

    # #####
    

    while True:
        data = client_connection.recv(1024).decode()
        if not data: break
        if data == "exit": break

        client_msg = data

        idx = get_client_index(clients, client_connection)
        sending_client_name = clients_names[idx]

        for c in clients:
            if c != client_connection:
                server_msg = str(sending_client_name + "->" + client_msg)
                c.send(server_msg.encode())

    # find the client index then remove from both lists(client name list and connection list)
    idx = get_client_index(clients, client_connection)
    del clients_names[idx]
    del clients[idx]
    server_msg = "BYE!"
    client_connection.send(server_msg.encode())
    client_connection.close()

    #######

# Return the index of the current client in the list of clients
def get_client_index(client_list, curr_client):
    idx = 0
    for conn in client_list:
        if conn == curr_client:
            break
        idx = idx + 1

    return idx


if __name__ == "__main__":
    start_server()