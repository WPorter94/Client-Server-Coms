import sys
import socket
import time

tries = 0
flag = True
connectionID = sys.argv[4]
messageToSend = sys.argv[1] + ' ' + connectionID
address = (sys.argv[2],int(sys.argv[3]))
clientSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

clientSocket.sendto(messageToSend.encode('utf-8'),address)

while flag :
    
    if(tries < 3 ) :
        clientSocket.settimeout(60)
        try :
            recievedMessage = clientSocket.recvfrom(1024)
            clientSocket.settimeout(None)
            recievedMsg = recievedMessage[0].decode()
            recievedAddr = recievedMessage[1]
            recievedCode = str(recievedMsg).strip("()'").split(" ")[0] 
            if recievedCode == 'RESET' :
                print("Connection Error " + connectionID)
                connectionID = input("Please enter a valid numerical identifier: ")
                messageToSend = sys.argv[1] + ' ' + connectionID
                clientSocket.sendto(messageToSend.encode('utf-8'),address)
                tries += 1

            if recievedCode == 'OK':
                print("Connection established " + connectionID + " " + sys.argv[2] + " " + sys.argv[3])
                flag = False
                clientSocket.close()
        except socket.timeout : 
            print("Connection Error " + connectionID)
            connectionID = input("Please enter a valid numerical identifier: ")
            messageToSend = sys.argv[1] + ' ' + connectionID
            clientSocket.sendto(messageToSend.encode('utf-8'),address)
            tries += 1
        except socket.error :
            print("Connection Failure")
            flag = False
            clientSocket.close()
    else :
        print("Connection Failure")
        flag = False
        clientSocket.close()
        
