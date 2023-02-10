import socket
import time
import sys

idList = {}
serverAddress = sys.argv[1]
serverPort = int(sys.argv[2])
flag = True

serverSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
serverSocket.bind((serverAddress,serverPort))

while(flag):

    serverSocket.settimeout(300)
    try:
        bytesAdress = serverSocket.recvfrom(1024)
        serverSocket.settimeout(None)
        msg = bytesAdress[0]
        addr = bytesAdress[1]
        recievedMessage =  format(msg)
        recievedAddress = format(addr)
        recievedAddress = recievedAddress.strip("()'").split(", ")
        recievedID = int(recievedMessage[8]+recievedMessage[9]+recievedMessage[10]+recievedMessage[11])
        recievedIP = recievedAddress[0].rstrip("'")
        recievedPort = recievedAddress[1]
        if recievedID in idList.keys() :
            if (time.time() - idList.get(recievedID)) < 60 :
                serverSocket.sendto(str.encode("RESET " + str(recievedID)),addr)
            else :
                idList[recievedID] = time.time()
                messageToSend = "OK " + str(recievedID) + ' ' + recievedIP + ' ' + recievedPort
                messageBytes = str.encode(messageToSend)
                serverSocket.sendto(messageBytes,addr)
        else :
            idList[recievedID] = time.time()
            messageToSend = "OK " + str(recievedID) + ' ' + recievedIP + ' ' + recievedPort
            messageBytes = str.encode(messageToSend)
            serverSocket.sendto(messageBytes,addr)
    except socket.timeout:
        flag = False
        serverSocket.close()
    
