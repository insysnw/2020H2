from socket import *
import re, uuid
import sys

serverName = 'localhost'
serverPort = 12001
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientMacAddr =  macAddr = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
clientBroadCast = '255.255.255'
currClientIPAddr = '0.0.0.0'

def getMACAddr():
    macAddr = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
    return macAddr

def checkMACAddr(address):
    if address == clientMacAddr:
        return True
    else:
        return False

def sendMessage(outgoingMessage):
    clientSocket.sendto(outgoingMessage.encode(),(serverName, serverPort))

def sendDiscover():
    message = 'DISCOVER,' + clientMacAddr + ',' + currClientIPAddr
    sendMessage(message)
    print('Sending discover from client to server')
    print(message)

def sendRequest(MAC, offeredIP):  
    message = 'REQUEST,' + clientMacAddr + ',' + offeredIP
    sendMessage(message)
    print('Sending request from client to server')

def receiveOffer(MAC, offeredIP):
    print('Received offer from server')
    out = 'offered ip: ' + offeredIP
    print(out)
    if checkMACAddr(MAC) == True:
        sendRequest(MAC, offeredIP)
    else:
        pass

def receiveDecline(declinedMessage):
    print (declinedMessage)
    sys.exit()

def Release():
    print('Sending release msg to server')
    outMsg = 'RELEASE,%s,%s'%(clientMacAddr,currClientIPAddr)
    sendMessage(outMsg)

def Renew():
    print('Sending renew msg to server')
    outMsg = 'RENEW,%s,%s'%(clientMacAddr, currClientIPAddr)
    sendMessage(outMsg)

def printMenu():
    print('Choose From The Following')
    print('RELEASE: 1')
    print('RENEW:   2')
    print('QUIT:    3')
    response = input()
    if response == '1':
        Release()
    elif response == '2':
        Renew() 
    elif response == '3':
        Release()
        print('Exiting program')
        sys.exit()
    else:
        print('incorrect response. try again')
        printMenu()

def receiveMessage():
    serverMessage, serverAddress = clientSocket.recvfrom(2048)
    serverMessage = serverMessage.decode()
    out = 'Received message from server: ' + serverMessage
    print(out)
    serverMessage = serverMessage.split(',')    
    msg_type = serverMessage[0]
    msg_mac_addr = serverMessage[1]
    msg_IP = serverMessage[2]
    if checkMACAddr(msg_mac_addr)==True:
        if msg_type == 'ACK' :
            receiveAck(msg_mac_addr, msg_IP)
        elif msg_type == 'OFFER':
            receiveOffer(msg_mac_addr, msg_IP)
        elif 'DECLINE' in msg_type:
            receiveDecline(msg_type)
        else:
            pass
    else:
        pass

def receiveAck(msg_mac_addr, msg_IP):
    global currClientIPAddr
    print('ACK received from server')
    out = 'Client IP Address: ' + msg_IP
    currClientIPAddr = msg_IP
    print(out)
    if checkMACAddr(msg_mac_addr) == True :
        printMenu()
    else:
        print('Incorrect MAC address! Exiting program')
        sys.exit()

def main():
    print('DHCP Client Started')
    print('-------------------')
    sendDiscover()
    print()
    while 1:
        receiveMessage()
        print()

main()
