# coding: utf-8

# HerbaChat Client made by HerbeMalveillante
# http://projetcharbon.tk

# importation of necessary modules :
import socketio
import socket
from tkinter import *
from tkinter.messagebox import *
import time

########## Global Variables ##########

sio = socketio.Client()

version = "0.1.0"
color1 = "Dark Gray"  # background color
color2 = "Dim Gray"  # frames color
color3 = "Light Gray"  # fields color
color4 = "black"  # color 4

print("we need to ask you some information. These information will be automatically inputted when you click on 'login' in the menu.")
client_username = input("Enter a username : ")
print("to login to the official HerbaChat servers, enter this address : 'http://malvherbe.ddns.net:5000'")
server_address = input("Enter a server address : ")

isReady = False


########## Misc Functions ##########


def get_ip_address():  # returns the client's ip address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def alert():  # print some dumb and useless shit when something happens
    print("SOMETHING HAPPENED WAHOU")


def get_message():  # gets the value of the message_entry content
    message_content = entry_value.get()
    message_author = client_username
    print("got message : " + message_content)
    return [message_content, message_author]


def send_message(self):  # sends a message to the server. Does not print anything
    if isReady:
        message = get_message()
        message_entry.delete(0, END)
        print("sending the message : " + message[0])
        sio.emit('messageClient-->Server', message)
    else:
        print("Unable to send message : not connected.")


def connect(ip_address, username):  # connects to the given server with the given username. Please disconnect from all the servers before trying to reconnect to a new one.
    global isReady
    print("Connecting to the socket server at : " + ip_address + " as " + username + ".")
    while True:
        try:
            sio.connect(ip_address)
            print("Connected successfully")
            break
        except:
            print(ip_address)
            print(
                "error : please check that the server is online and the address is correct. Address format : http://[address]:[port]")
            time.sleep(1)

    isReady = True
    disable_text_box(message_box, message_entry, entry_value, "enable")
    sio.emit('connectionClient-->Server', username)


def get_hour():  # returns the hour in the following format : '[HH:MM] ' (with a space)
    date = time.ctime(time.time())
    hour = "[" + date[11:16] + "] "
    return hour


########## Useful Variables ##########

# this line is used if you want a local (on only one computer) connection.
# serverIpAddress = "http://" + get_ip_address() + ":5000"
# this line is used if you want a connection on a specific ip (still local)
# serverIpAddress = "http://192.168.1.84:5000"

########## GUI CONFIGURATION ##########


def login():  # called when the login button from the menu is clicked
    def send_login():  # sends the login information to the connect() function
        print("sending the credentials and connecting")
        connect(server_address, client_username)

    print("launching the login window")
    send_login()


def disable_text_box(widget, entry, entryvalue, state):  # disables the message_box and more generally all the chat.
    if state == "disable":
        entry.config(state=DISABLED)
        entryvalue.set("Please login using the 'file' menu before trying to talk in the chat.")
        widget.delete(0, END)
        print("chat disabled")
    elif state == "enable":
        entry.config(state=NORMAL)
        entryvalue.set("")
        print("chat enabled")
    else:
        print("error : 'state' argument must be 'enabled' or 'disabled'.")


def print_in_chat(message):  # displays a message in the chat
    message_box.config(state=NORMAL)
    message_box.insert(END, message)
    message_box.config(state=DISABLED)
    message_box.see("end")


def root():  # The main window : the one with the chat in it.

    # needed because we can't use functions parameters in tkinter keys commands for some reason.
    global entry_value
    global message_entry
    global message_box

    print("Loading the main window")

    # Configuration
    root_window = Tk()  # creates the window object
    root_window.title("HerbaChat Client " + version)  # gives a name for the window
    try:
        root_window.iconbitmap(r'data/icon.ico')
    except TclError:
        print("something went wrong while applying the icon. Check that it is present in the folder 'data/icon.ico'.")
    root_window.minsize(600, 600)
    root_window.configure(background=color1)

    # Frame 1 (message history)
    frame_1 = LabelFrame(root_window, text="Message History", borderwidth=2, relief=GROOVE)
    frame_1.pack(side=TOP, padx=30, pady=30)
    frame_1.configure(background=color2)
    # Frame 2 (message entry)
    frame_2 = LabelFrame(root_window, text="Type your message and hit RETURN to send.", borderwidth=2, relief=GROOVE)
    frame_2.pack(side=BOTTOM, padx=30, pady=30)
    frame_2.configure(background=color2)

    # Message box (the big text widget that displays the chat)
    message_box = Text(frame_1)
    message_box.config(state=DISABLED, bg=color3)
    message_box.pack(side=LEFT)

    # Scrollbar
    scrollbar = Scrollbar(frame_1)
    scrollbar.pack(side=RIGHT, fill=Y)

    # Message entry (the field in which you type messages)
    entry_value = StringVar()  # creating the variable that contains the message
    entry_value.set("")

    message_entry = Entry(frame_2, textvariable=entry_value, width=100)
    message_entry.config(background=color3)
    message_entry.pack()

    # Adding the scrollbar to the message box
    message_box.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=message_box.yview)

    # Adding the menu
    menu_bar = Menu(root_window)

    menu1 = Menu(menu_bar, tearoff=0)
    menu1.add_command(label="Login", command=login)
    menu1.add_separator()
    menu1.add_command(label="Settings", command=alert)
    menu1.add_separator()
    menu1.add_command(label="Quit", command=alert)
    menu_bar.add_cascade(label="File", menu=menu1)

    menu2 = Menu(menu_bar, tearoff=0)
    menu2.add_command(label="About", command=alert)
    menu_bar.add_cascade(label="Help", menu=menu2)

    root_window.config(menu=menu_bar)

    # Adding the key to register the message
    root_window.bind('<Return>', send_message)

    print("Main Window Loaded")

    if not isReady:
        disable_text_box(message_box, message_entry, entry_value, "disable")
    else:
        disable_text_box(message_box, message_entry, entry_value, "enable")

    root_window.mainloop()


########## Message reception from the server ##########

@sio.on('confirmMessageServer-->Client')
def on_message_reception(message):  # called on the reception of the message reception confirmation from the server
    print("received a message from the server :")
    print(message[1] + ' : ' + message[0])
    message_to_write = get_hour() + message[1] + ' : ' + message[0] + "\n"
    print_in_chat(message_to_write)


@sio.on('confirmConnectionServer-->Client')
def on_connection_confirmation(username):  # called on the reception of the connection confirmation from the server
    print("received a connection confirmation message from the server :")
    print(get_hour() + username + " just connected !")
    print_in_chat(get_hour() + username + " just connected !\n")


########## Main ##########

if __name__ == '__main__':  # runs if the program is launched as himself and not as a module
    print("HerbaChat V" + version)
    print("Created by HerbeMalveillante")
    print("Pre Alpha version")
    print("")
    root()
