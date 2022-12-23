# -*- coding: utf-8 -*-
"""
Created on Thu Jul 15 20:03:58 2021

@author: User
"""


import socket
import threading


ADDR = ('localhost',9000)
FORMAT = "utf-8"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(ADDR)



def extract(msg):
    lines = msg.split("\n")
    line1 = lines[0]
   
    if lines[len(lines) - 2] == '' :
        header = lines[1 : len(lines) - 2]
        body = lines[len(lines) - 1 : ]
    else:
        header = lines[1 : ]
        body = None
        
    return line1, header, body    

def get(msg):
    
    line1, header, body = extract(msg)
    
    if line1[0 : 3] == "GET":
        return True
    else:
        return False

def responsetoget(msg):
    
    line1, header, body = extract(msg)
   
    body = "<html>\n<head>\n<title> \nOutput Data in an HTML file\n \
           </title>\n</head> <body> <h1>Data Networks Project \
           <font color = #00b300>1</font></h1>\n \
           <h2>Part 5: Implementing a Web Server</h2>\n</body></html>"
           
    response = f"HTTP/1.1 200 OK\nContent-Type: text/html; charset=utf-8\n\n{body}"
    return response


    

def handle_client(conn, addr):
    print(f"New Connection: {addr} connected!")
    
    connected = True
    while connected:
        msg = conn.recv(2048).decode(FORMAT)
        if not msg:
            connected = False
            
        if get(msg):
            response = responsetoget(msg)
            
        print(f"{addr} : {msg}")
        conn.send(response.encode(FORMAT))
        
    conn.close()
    
    
def start():
    server.listen()

    while True:
        conn, addr = server.accept()        # Blocking line
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()
        print(f"/nActive Connections: {threading.activeCount() - 1}")
        
        
##############################################################################


print("Server is starting!")
start()
    