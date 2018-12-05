############## Program created using Python 2.7 ################################
############## Program created on localhost ####################################
############### The protocol used for this assignment is TCP ###################
#################### Program built in Windows ##################################

#Important notice about log files: On any incorrect inputs, the program terminates hence log files are re-written
#everytime the client and server is restarted

import time
from socket import * # import socket module
import json
import pickle
import sys
import datetime

#Creating a client side TCP socket
serverIP = 'localhost'
serverPort = 49000
clientSocket = socket(AF_INET, SOCK_STREAM) 
clientSocket.connect((serverIP,serverPort))

#Taking user input and sending to the server for the file to be found
print "Connection established at: ", datetime.datetime.now()
file_to_find = raw_input('Enter file name with extension: ')
clientSocket.send(file_to_find)
temp_str = file_to_find.split('.')

#maintaining log file
addr = clientSocket.recv(1024)
with open('cLog.txt', 'w') as log:
    log.write("Sent file name to server IP: \n")
    log.write(str(serverIP))
    log.write("\n")
    log.write("File name sent at date and time: \n")
    log.write(str(datetime.datetime.now()))
    log.write("\n")
    log.write("File name sent to server through client IP:")
    log.write("\n")
    log.write(str(addr))
    log.write("\n\n")
    log.close()

#Receiving info about the file to be searched on the server
check = clientSocket.recv(1024)
if check == '0':
    print "File(s) not found on the server! Program terminated."
    clientSocket.close()

#If file available on the server, do this:
else:
    #De-serializing the received dictionary from the client through pickle
    serverReturn = pickle.loads(clientSocket.recv(1024))

    #maintaining log file
    with open('cLog.txt', 'a') as log:
        log.write("Received dictionary of file names sent from client to server IP: \n")
        log.write(str(serverIP))
        log.write("\n")
        log.write("Dictionary of file names sent at date and time: \n")
        log.write(str(datetime.datetime.now()))
        log.write("\n")
        log.write("Dictionary of file names sent to server through client IP:")
        log.write("\n")
        log.write(str(addr))
        log.write("\n\n")
        log.close()

    #printing the received dictionary on client side
    sys.stdout.write(serverReturn)
    sys.stdout.flush()

    #Prompting the user for the exact file path of the required file
    #The path has to be entered with single back slashes, not double back slashes as returned by the computer. The program works this way
    file_path = raw_input("\nEnter the file path you wish to receive back from the server from the displayed list but with SINGLE BACKSLASHES: ")

    #Sending it back to the server
    clientSocket.send(file_path)

    #maintaining log file
    with open('cLog.txt', 'a') as log:
        log.write("File path sent from client to server IP: \n")
        log.write(str(serverIP))
        log.write("\n")
        log.write("File path sent at date and time: \n")
        log.write(str(datetime.datetime.now()))
        log.write("\n")
        log.write("File path sent through client IP:")
        log.write("\n")
        log.write(str(addr))
        log.write("\n")
        log.write("File path sent: \n")
        log.write(str(file_path))
        log.write("\n\n")
        log.close()

    #print "File received! Success!"

    # Receiving file from client
    rec_file = open("file_found."+ temp_str[1], 'wb')
    data = clientSocket.recv(1024)
    while (data):
        rec_file.write(data)
        clientSocket.settimeout(2)
        data = clientSocket.recv(1024)

    #maintaining log file
    with open('cLog.txt', 'a') as log:
        log.write("Final file received from server IP: \n")
        log.write(str(serverIP))
        log.write("\n")
        log.write("Final file sent at date and time: \n")
        log.write(str(datetime.datetime.now()))
        log.write("\n")
        log.write("Final file sent through client IP: \n")
        log.write(str(addr))
        log.write("\n\n")
        log.close()

        print "File received, mission complete!"

clientSocket.close()
rec_file.close()