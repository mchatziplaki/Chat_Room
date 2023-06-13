"""Assignment 4"""

import socket
import threading
import tkinter
from tkinter import ttk
from tkinter import messagebox
import json

# Create a global format variable for multiple uses
FORMAT = 'utf-8'
target_host = socket.gethostname()
HOST_ADDR = "127.0.0.1"
HOST_PORT = 1234
clients_names = []


def connect():
    global username, client
    if len(name_box.get()) < 1:
        tkinter.messagebox.showerror(title="ERROR!!!", message="You MUST enter your first name <e.g. John>")
    else:
        username = name_box.get()
        join(username)

def join(name):
    global client, HOST_PORT, HOST_ADDR
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST_ADDR, HOST_PORT))
        client.send(name.encode()) # Send name to server after connecting

        name_box.config(state=tkinter.DISABLED)
        join_btn.config(state=tkinter.DISABLED)     
        text_box.config(state=tkinter.NORMAL)
        send_to_all_btn.config(state=tkinter.NORMAL)
        send_to_one_btn.config(state=tkinter.NORMAL)
        leave_btn.config(state=tkinter.NORMAL)

        # start a thread to keep receiving message from server
        # do not block the main thread :)
        threading._start_new_thread(receive_message_from_server, (client, "m"))
        
    except Exception as e:
        tkinter.messagebox.showerror(title="ERROR!!!", message="Cannot connect to host: " + HOST_ADDR + " on port: " + str(HOST_PORT) + " Server may be Unavailable. Try again later")


        

    
def receive_message_from_server(sck, m):
    while True:
        from_server = sck.recv(1024).decode()

        if not from_server: break

        # display message from server on the chat window

        # enable the display area and insert the text and then disable.
        # why? Apparently, tkinter does not allow us insert into a disabled Text widget :(
        texts = chat_terminal.get("1.0", tkinter.END).strip()
        chat_terminal.config(state=tkinter.NORMAL)
        if len(texts) < 1:
            chat_terminal.insert(tkinter.END, from_server)
        else:
            chat_terminal.insert(tkinter.END, "\n\n"+ from_server)

        chat_terminal.config(state=tkinter.DISABLED)
        chat_terminal.see(tkinter.END)   
        
        # client.send("".encode())
        # new_name = client.recv(1024).decode()
        # clients_names.append(new_name)
        # print(f"New entry is: {new_name}")
        private_entry['value'] = "Lola"

    sck.close()
    root.destroy()
    
def getChatMessage(msg):
    
    msg = msg.replace('\n', '')
    texts = chat_terminal.get("1.0", tkinter.END).strip()

    # enable the display area and insert the text and then disable.
    # why? Apparently, tkinter does not allow use insert into a disabled Text widget :(
    chat_terminal.config(state=tkinter.NORMAL)
    if len(texts) < 1:
        chat_terminal.insert(tkinter.END, "You->" + msg, "tag_your_message") # no line
    else:
        chat_terminal.insert(tkinter.END, "\n\n" + "You->" + msg, "tag_your_message")

    chat_terminal.config(state=tkinter.DISABLED)

    send_mssage_to_server(msg)

    chat_terminal.see(tkinter.END)
    text_box.delete('1.0', tkinter.END)
    
    
    

def send_mssage_to_server(msg):
    client_msg = str(msg)
    client.send(client_msg.encode())
    if msg == "exit":
        client.close()
        root.destroy()
    print("Sending message")

def leave():
    root.destroy()

# Create the main window
root = tkinter.Tk()
root.title('Chat Service')
root.geometry('400x650')


name_box = tkinter.Entry(root, bd=0, bg='white', width=15,
font =('Courier New',10), foreground='red', justify='left')
name_box.place(x=70, y=6,height= 22, width= 250)

# Create and add the 'Join' button and place it above chat terminal
join_btn= tkinter.Button(root, text = 'Join',  width=7, height=4,
bd=0, bg='lightslategrey', activebackground='lightsteelblue',foreground='white',
font=("Arial", 12), command=lambda : connect())
join_btn.place(x=157, y=35, height=22)

# Create and add the chat terminal
chat_terminal = tkinter.Text(root, bd =0, bg ='white', width=30, height=4,
font=('Courier New',10), foreground='black')
chat_terminal.place(x=6,y=65, height=385, width=370)

# Create and add the scrollbar
scrollbar = tkinter.Scrollbar(root, command=chat_terminal.yview,
cursor='arrow')
scrollbar.place(x=375,y=65, height=385)

# Create and add the message text box
text_box = tkinter.Text(root, bd=0, bg='white', width=15,
font =('Courier New',10), foreground='red')
text_box.place(x=20, y=480,height= 22, width= 250)
text_box.config(state="disabled")

# Create and the 'Send to all' button and place it next to text entry
send_to_all_btn = tkinter.Button(root, text = 'Send to all', width=10, height=4,
bd=0, bg='lightslategrey', activebackground='lightsteelblue',foreground='white',
font=("Arial", 12), command=(lambda: getChatMessage(text_box.get("1.0", tkinter.END))))
send_to_all_btn.place(x=287, y = 480, height=22)
send_to_all_btn.config(state="disabled")

private_entry = ttk.Combobox(root)
private_entry.place(x=20, y = 510, height=22)

send_to_one_btn = tkinter.Button(root, text = 'Send to...', width=10, height=4,
bd=0, bg='lightslategrey', activebackground='lightsteelblue',foreground='white',
font=("Arial", 12), command=lambda : getChatMessage(text_box.get("1.0", tkinter.END)))
send_to_one_btn.place(x=287, y = 510, height=22)
send_to_one_btn.config(state="disabled")


leave_btn = tkinter.Button(root, text = 'Leave', width=10, height=4,
bd=0, bg='lightslategrey', activebackground='lightsteelblue',foreground='white', background = 'red',
font=("Arial", 12), command=leave)
leave_btn.place(x=287, y = 550, height=22)
leave_btn.config(state="disabled")



#private_entry.insert("end", client.recv(1024).decode())


root.mainloop()
