# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 23:18:20 2021

@author: M Sabbagh
"""

import socket
from base64 import b64encode
from base64 import b64decode
import os


def extract(msg):
    lines = msg.splitlines()
    line1 = lines[0]
    header = lines[1 : ]
    body = None
    for i in range (len(lines)):
        if lines[i] == "":
            header = lines[1 : i]
            body = lines[i + 1  : ]
            
    return line1, header, body
        
            
def OK200(msg):
    
    line1, header, body = extract(msg)
    
    if line1 == "HTTP/1.0 200 OK":
        return True
    else:
        return False
    
def save(msg, response):
    
    line1, header, body = extract(response)
    line1_1 ,header1_1, body1_1 = extract(msg)
    
        
    x = line1_1[4 : -9]
    y = x.split("/")[-1 : ]
    
    for e in y:
        filename = e
    
        
    path1 = "D:/SUT/Semester 6/Data Networks/project/client files/testfiles/" + filename
    
    
    for i in range(len(header)):
        if header[i][0 : 14] == "Content-Type: ":
            content_type = header[i][14 : ]
    
    if content_type == "text/html" or content_type == "text/txt":
        content = ""
        for i in range(len(body)):
            content = content + body[i] + "\n" 

        file = open(path1,'w')
        file.write(content)
        file.close()
    elif content_type == "image/jpg" or content_type == "image/png":
        u = response.splitlines()[-1 :]
        for e in u:
            content = e
        content = str.encode(content)
        content = b64decode(content)
        file = open( path1, 'wb')
        file.write(content)
        file.close()
        
def post(path):
    
    y = path.split(".")[-1 : ]
    for e in y:
        ctype = e
        
    if ctype == "html":
        content_type = "text/html"
        file = open(path, 'r')
        content = file.read()
        length = len(content)
        
    elif ctype == "txt":
        content_type = "text/txt"
        file = open(path, 'r')
        content = file.read()
        length = len(content)
        
    elif ctype == "jpg":
        content_type = "image/jpg"
        length = os.stat(path).st_size
        file = open(path, 'rb')
        content = file.read()
        content = b64encode(content)
        content = str(content, 'utf-8')
        
    elif ctype == "png":
        content_type = "image/png"
        length = os.stat(path).st_size
        file = open(path, 'rb')
        content = file.read()
        file.close()
        content = b64encode(content)
        content = str(content, 'utf-8')
   
    msg = f"POST /{path} HTTP/1.1\nHost: server\nContent-Length: {length}\nContent-Type: {content_type}\n\n{content}"
    
    return msg

    
def send(msg):
    message = msg.encode(FORMAT)
    client.send(message)
    response = client.recv(20480000).decode(FORMAT)
    print(response)
    
    if OK200(response):
        save(msg, response)
    
##############################################################################

PORT = 8000
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "DISCONNECT!"

SERVER = "192.168.56.1"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
    
    
   
    

test1_1 = "GET /../.. HTT/1.1\nHost: developer.mozilla.org\nAccept-Language: fr"
test1_2 = "GET  HTTP/1.1\nHost: developer.mozilla.org\nAccept-Language: fr"
test1_3 = "GET /../.. HTTP/1.1\nHost developer.mozilla.org\nAccept-Language: fr"

test2 = "???? /../.. HTTP/1.1\nHost: developer.mozilla.org\nAccept-Language: fr"

test3 = "PUT /../.. HTTP/1.1\nHost: developer.mozilla.org\nAccept-Language: fr"

test4 = "GET /testfiles/test.png HTTP/1.1\nHost: server"
test5 = "GET /testfi/test1.jpg HTTP/1.1\nHost: server"

test7 = "POST /../.. HTTP/1.1\nHost: developer.mozilla.org\nAccept-Language: fr\n\n<html><body><h1>THISISFORBIDDEN!</h1></body></html>"
msg = post("D:/SUT/Semester 6/Data Networks/project/client files/testfiles/test.jpg")

#send(test1_1)
#send(test1_2)
#send(test1_3)
#send(test2)
#send(test3)
#send(test4)
#send(test5)
#send(test7)
#send(msg)
#send("number of connected clients")
#send("file type stats")
#send("request stats")
#send("response stats")
#send("disconnect")
