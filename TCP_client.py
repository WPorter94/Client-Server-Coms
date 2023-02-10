import sys
import socket

tries = 0
flag = True
connectionID = sys.argv[4]
messageToSend = sys.argv[1] + ' ' + connectionID
address = (sys.argv[2],int(sys.argv[3]))
clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    clientSocket.connect(address)
    clientSocket.send(messageToSend.encode('utf-8'))
except:
    print("Connection Failure")
    flag = False


while flag :
    if(tries < 3 ) :
        clientSocket.settimeout(60)
        try :
            recievedMessage = clientSocket.recv(1024)
            clientSocket.settimeout(None)
            recievedMessage = recievedMessage.decode().split(" ")
            recievedCode = str(recievedMessage[0])
            recievedAddr = recievedMessage[1]
            if recievedCode == 'RESET' :
                clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                clientSocket.connect(address)
                print("Connection Error " + connectionID)
                connectionID = input("Please enter a valid numerical identifier: ")
                messageToSend = sys.argv[1] + ' ' + str(connectionID)
                clientSocket.send(messageToSend.encode('utf-8'))
                tries += 1

            if recievedCode == 'OK':
                print("Connection established " + str(connectionID) + " " + sys.argv[2] + " " + sys.argv[3])
                flag = False
        except socket.timeout : 
            clientSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            clientSocket.connect(address)
            print("Connection Error " + connectionID)
            connectionID = input("Please enter a valid numerical identifier: ")
            messageToSend = sys.argv[1] + ' ' + str(connectionID)

            clientSocket.send(messageToSend.encode('utf-8'))
            tries += 1
        except socket.error : 
            print("Connection Failure")
            flag = False
    else :
        print("Connection Failure")
        flag = False
        

clientSocket.close()