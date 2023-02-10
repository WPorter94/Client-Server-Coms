import socket
import time
import sys

idList = {}
serverAddress = sys.argv[1]
serverPort = int(sys.argv[2])
flag = True
serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serverSocket.bind((serverAddress,serverPort))
serverSocket.listen()


while(flag):
    serverSocket.settimeout(300)
    clientConnection, recievedAddress = serverSocket.accept()
    
    try:
        
        bytesAddress = clientConnection.recv(1024)
        
        serverSocket.settimeout(None)
        bytesAddress = bytesAddress.decode().split(" ")
       
        
        if bytesAddress[0] == 'HELLO' :
            recievedMessage = bytesAddress[0]
            recievedID = int(bytesAddress[1])        
            recievedIP = recievedAddress[0]
            recievedPort = recievedAddress[1]
            if recievedID in idList.keys() :
                if (time.time() - idList.get(recievedID)) < 60 :
                    messageToSend = str.encode("RESET " + str(recievedID))
                    clientConnection.sendall(messageToSend)
                else :
                    idList[recievedID] = time.time()
                    messageToSend = str.encode("OK " + str(recievedID) + ' ' + str(recievedIP) + ' ' + str(recievedPort))
                    clientConnection.sendall(messageToSend)      
            else :
                idList[recievedID] = time.time()
                messageToSend = str.encode("OK " + str(recievedID) + ' ' + str(recievedIP) + ' ' + str(recievedPort))
                clientConnection.sendall(messageToSend)
    except socket.timeout:
        flag = False
        serverSocket.close()
    
