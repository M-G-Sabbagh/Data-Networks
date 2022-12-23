# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 22:48:13 2021

@author: M Sabbagh
"""

import socket
import threading
import datetime
import os
from base64 import b64encode
from base64 import b64decode
import json


datetime = datetime.datetime.now()


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
 
            
            
def Error400(msg): 
    
    line1, header, body = extract(msg)
    
    wrongline1 = True
    for i in range (len(line1) - 2):
        if line1[i : i + 2] == " /":
            wrongline1 = False
    
    wrongheaderformat = True
    if isinstance(header, str):
        for i in range (len(header)):
            if header[i] == ":" :
                wrongheaderformat = False
    else:
        a = [0]*len(header)
        for i in range (len(header)):
            for j in range(len(header[i])):
                if header[i][j] == ":":
                    a[i] = 1
        if a == [1]*len(header):
            wrongheaderformat = False
              
    version = line1[-8 : ]
    if version != "HTTP/1.0" and version != "HTTP/1.1":
        return True
    elif wrongline1:
        return True
    elif wrongheaderformat:
        return True
    else:
        return False
     
def Error400Response():
    response = f"HTTP/1.0 400 Bad Request\nConnection: close\nContent-Length: 46\nContent-Type: text/html\nDate: [utc-{datetime}]\n\n<html><body><h1>BADREQUEST!</h1></body></html>"
    return response   
 
    
def Error501(msg):
    
    line1, header, body = extract(msg)
    
    if line1[0:3] != "PUT" and line1[0:3] != "GET" and line1[0:4] != "POST" and line1[0:4] != "HEAD" and line1[0:6] != "DELETE" :
        return True
    else:
        return False
    
    
def Error501Response():
    response = f"HTTP/1.0 501 Not Implemented\nConnection: close\nContent-Length: 50\nContent-Type: text/html\nDate: [utc-{datetime}]\n\n<html><body><h1>NOTIMPLEMENTED!</h1></body></html>"
    return response   
      
def Error405(msg):
    
    line1, header, body = extract(msg)
    
    if line1[0:3] != "GET" and line1[0:4] != "POST" :
        return True
    else:
        return False
  
def Error405Response():
    response = f"HTTP/1.0 405 Method Not Allowed\nConnection: close\nContent-Length: 46\nContent-Type: text/html\nAllow: GET\nDate: [utc-{datetime}]\n\n<html><body><h1>NOTALLOWED!</h1></body></html>"
    return response   

def OK200(msg):
    
    line1, header, body = extract(msg)
    
    path = line1[4:-9]
    
    if line1[0:3] != "GET":
        return False
    elif not os.path.isfile("." + path):
        return False
    else:
        return True
    

def OK200Response(msg):
    
    line1, header, body = extract(msg)
    
    path = line1[4:-9]
    y = path.split(".")[-1 : ]
    for e in y:
        ctype = e
        
    if ctype == "html":
        content_type = "text/html"
        file = open("." + path, 'r')
        content = file.read()
        length = len(content)
        
    elif ctype == "txt":
        content_type = "text/txt"
        file = open("." + path, 'r')
        content = file.read()
        length = len(content)
        
    elif ctype == "jpg":
        content_type = "image/jpg"
        length = os.stat("." + path).st_size
        
        with open("." + path, "rb") as file: 
            content = file.read()
            content = b64encode(content)
            content = str(content, 'utf-8')
        
    elif ctype == "png":
        content_type = "image/png"
        length = os.stat("." + path).st_size
        file = open("." + path, 'rb')
        content = file.read()
        file.close()
        content = b64encode(content)
        content = str(content, 'utf-8')
   
    response =  f"HTTP/1.0 200 OK\nConnection: close\nContent-Length: {length}\nContent-Type: {content_type}\nDate: [utc-{datetime}]\n\n{content}"
    
    
    file = open("filetype.json", "r")
    dic = json.loads(file.read())
    file.close()
    
    key = len(dic) + 1
    
    dic[key] = content_type
    
    file = open("filetype.json", "w")
    json.dump(dic, file)
    file.close()
    
    return response
       
        
    
def Error301(msg):
    
    line1, header, body = extract(msg)
    
    path = line1[4:-9]
    
    if line1[0:3] != "GET":
        return False
    elif os.path.isfile("." + path):
        return False
    else:
        return True
    
    
def Error301Response():
    response = f"HTTP/1.0 301 Moved Permanently\nConnection: close\nContent-Length: 52\nContent-Type: text/html\nDate: [utc-{datetime}]\n\n<html><body><h1>MOVEDPERMANENTLY!</h1></body></html>"
    return response

def Error403(msg):
    
    line1, header, b = extract(msg)

    if b != None:
        for e in b:
            body = e
    if line1[0 : 4] == "POST" and body == "<html><body><h1>THISISFORBIDDEN!</h1></body></html>" :
        return True
    else:
        return False
        
    
def Error403Response():
    response = f"HTTP/1.0 403 Forbidden\nConnection: close\nContent-Length: 45\nContent-Type: text/html\nDate: [utc-{datetime}]\n\n<html><body><h1>FORBIDDEN!</h1></body></html>"
    return response
    
def ispost(msg):
    
    line1, header, b = extract(msg)

    if b != None:
        for e in b:
            body = e
    if line1[0 : 4] == "POST" and body != "<html><body><h1>THISISFORBIDDEN!</h1></body></html>" :
        return True
    else:
        return False
    
def saveandresponse(msg):
    
    line1, header, body = extract(msg)
    
        
    x = line1[4 : -9]
    y = x.split("/")[-1 : ]
    
    for e in y:
        filename = e
    
        
    path1 = "D:/SUT/Semester 6/Data Networks/project/server files/testfiles/" + filename
    
    
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
        u = msg.splitlines()[-1 :]
        for e in u:
            content = e
        content = str.encode(content)
        content = b64decode(content)
        file = open( path1, 'wb')
        file.write(content)
        file.close()
      
    response =  f"HTTP/1.0 200 OK\nConnection: close\nContent-Length: 40\nContent-Type: text/html\nDate: [utc-{datetime}]\n\n<html><body><h1>POST!</h1></body></html>"
    return response
    
    
def log(addr, msg, response, starttime):
    
    req_line1, req_header, req_body = extract(msg)
    res_line1, res_header, res_body = extract(response)
    res_type = res_line1[9 : ]
    
    req_type = ""
    for i in range (len(req_line1)):
        if req_line1[i] != " ":
            req_type = req_type + req_line1[i]
        else:
            break
        
    
    file = open("log.json", "r")
    dic = json.loads(file.read())
    file.close()
    
    key = len(dic) + 1
    
    dic[key] = [addr, req_type, res_type, str(starttime)]
    
    file = open("log.json", "w")
    json.dump(dic, file)
    file.close()
    
    
def numofclients():
    response = f"Number of connected clients: {threading.activeCount() - 1}"
    return response

def filetypestats():
    
    file = open("filetype.json", "r")
    dic = json.loads(file.read())
    file.close()
    
    html = 0
    txt = 0
    jpg = 0
    png = 0
    
    for key in dic:
        if dic[key] == "text/html":
            html = html + 1
        elif dic[key] == "text/txt":
            txt = txt + 1
        elif dic[key] == "image/jpg":
            jpg = jpg + 1
        elif dic[key] == "image/png":
            png = png + 1
        
            
    response = f"text/html : <{html}>\ntext/txt : <{txt}>\nimage/jpg : <{jpg}>\nimage/png : <{png}>"
    return response   


def requeststats():  
    
    file = open("log.json", "r")
    dic = json.loads(file.read())
    file.close()
    
    GET = 0
    PUT = 0
    POST = 0
    DELETE = 0
    HEAD = 0
    Improper = 0
    
    for key in dic:
        if dic[key][1] == 'GET':
            GET = GET + 1
        elif dic[key][1] == 'PUT':
            PUT = PUT + 1
        elif dic[key][1] == 'POST':
            POST = POST + 1
        elif dic[key][1] == 'DELETE':
            DELETE = DELETE + 1
        elif dic[key][1] == 'HEAD':
            HEAD = HEAD + 1
        elif dic[key][1] == 'Improper':
            Improper = Improper + 1
            
    response = f"GET : <{GET}>\nPUT : <{PUT}>\nPOST : <{POST}>\nDELETE : <{DELETE}>\nHEAD : <{HEAD}>\nImproper : <{Improper}>"
    return response   

def responsestats():
    
    file = open("log.json", "r")
    dic = json.loads(file.read())
    file.close()
    
    E400 = 0
    E501 = 0
    E405 = 0
    E200 = 0
    E301 = 0
    E403 = 0
    
    for key in dic:
        if dic[key][2][0 : 3] == '400':
            E400 = E400 + 1
        elif dic[key][2][0 : 3] == '501':
            E501 = E501 + 1
        elif dic[key][2][0 : 3] == '405':
            E405 = E405 + 1
        elif dic[key][2][0 : 3] == '200':
            E200 = E200 + 1
        elif dic[key][2][0 : 3] == '301':
            E301 = E301 + 1
        elif dic[key][2][0 : 3] == '403':
            E403 = E403 + 1
            
    response = f"400 : <{E400}>\n501 : <{E501}>\n405 : <{E405}>\n200 : <{E200}>\n301 : <{E301}>\n403 : <{E403}>"
    return response   
    

    
def handle_request(msg, conn):
    
    telnet = False
         
    if msg == "number of connected clients":
        response = numofclients()
        telnet = True
    elif msg == "file type stats":
        response = filetypestats()
        telnet = True
    elif msg == "request stats":
        response = requeststats()
        telnet = True
    elif msg == "response stats":
        response = responsestats()
        telnet = True
    elif msg == "disconnect":
        telnet = True
        conn.close()
    
    elif Error400(msg):
        response = Error400Response()
    elif Error501(msg):
        response = Error501Response()
    elif Error405(msg):
        response = Error405Response()
    elif Error301(msg):
        response = Error301Response()
    elif OK200(msg):
        response = OK200Response(msg)
    elif Error403(msg):
        response = Error403Response()
    elif ispost(msg):
        response = saveandresponse(msg)
        
    return response, telnet
    
       
       
def handle_client(conn, addr):
    print(f"New Connection: {addr} connected!")

    connected = True
    while connected:
        msg = conn.recv(20480000).decode(FORMAT)
        if not msg:
            connected = False
            
        print(f"\n{addr}:\n{msg}")
        
            
        response, telnet = handle_request(msg, conn)
        
        if not telnet:

            log(addr, msg, response, datetime)    
            
        conn.send(response.encode(FORMAT))       
        
        
    conn.close()
    
    
def start():
    server.listen()
    print(f"Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()        # Blocking line
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()
        print("\n")
        print(f"Active Connections: {threading.activeCount() - 1}")
        
        
##############################################################################


PORT = 8000
SERVER = socket.gethostbyname(socket.gethostname())
print(SERVER)
ADDR = (SERVER, PORT)
FORMAT = "utf-8"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(ADDR)


print("Server is starting!")
start()
        

