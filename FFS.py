############## Program created using Python 2.7 ############################
############## Program created on localhost ################################
############### The protocol used for this assignment is TCP ###############
#################### Program built in Windows 10.1 ##############################

#Important notice about log files: On any incorrect inputs, the program terminates hence log files are re-written
#everytime the client and server is restarted

from socket import*
import os
import os.path
import re
import json
import pickle
import datetime
import sys

#Creating a server side TCP socket and other variables
serverIP = 'localhost'
serverPort = 49000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((serverIP, serverPort))
serverSocket.listen(1)
dict = {}
dict2 = {}
found = 1
check = 1
file_requested = ''
counter = 0
check2 = 1
seq = 0
run = 1

#Server ready state
print "Connection established at: ", datetime.datetime.now()
print("The FFS server is ready to receive a client request!")
	
while(run):
	#Server prompted to receive input from client
	connectionSocket, addr = serverSocket.accept()

	file = connectionSocket.recv(1024)
	connectionSocket.send(str(addr))

	#maintaining log file
	with open('sLog.txt', 'w') as log:
		log.write("Received file name from client IP: \n")
		log.write(str(addr))
		log.write("\n")
		log.write("File requested name:")
		log.write("\n")
		log.write(str(file))
		log.write("\n")
		log.write("Received at date and time: \n")
		log.write(str(datetime.datetime.now()))
		log.write("\n")
		log.write("Received at server IP: \n")
		log.write(str(serverIP))
		log.write("\n\n")
		log.close()

	#Loop to crawl directories for the searched file, instructor must enter his directory here
	for dirpath, dirs, files in os.walk("E:\\"):
		for root in os.walk('.'):
			if file in files or file in dirs:
				counter += 1
				print "File found!"
				found = 1
				print os.path.join(dirpath, file)
				file_requested = os.path.join(dirpath, file)

				#getting size in bytes of the file found
				size = os.path.getsize(os.path.join(dirpath, file))
				print "File Size", size, "bytes"

				#Inserting the filepath and filesize into a python dictionary
				dict[size] = dirpath
				dict2[size] = file_requested
				break

	#Checking to see if the dictionary has any entries
	if dict:
		print "File(s) found on the server."

		#Send the dictionary to the client
		temp = json.dumps(dict).encode('utf-8')
		connectionSocket.send(str(found))
		connectionSocket.send(pickle.dumps(temp))

		#maintaining log file
		with open('sLog.txt', 'a') as log:
			log.write("Sent dictionary of all found files back to client at client IP: \n")
			log.write(str(addr))
			log.write("\n")
			log.write("Dictionary sent to client at date and time: \n")
			log.write(str(datetime.datetime.now()))
			log.write("\n")
			log.write("Dictionary sent by server IP: \n")
			log.write(str(serverIP))
			log.write("\n\n")
			log.close()
		#tcp_send(pickle.dumps(dict))

	#if the dictionary is empty means the requested file was not found on the server
	else:
		print "File(s) not found on the server"
		found = 0
		connectionSocket.send(str(found))
		connectionSocket.send("File(s) not found on the server! Server terminated.")
		serverSocket.close()

	#Receiving the exact file path of the desired file back from the client
	file_path = connectionSocket.recv(1024)

	with open("sLog.txt", 'a') as log:
		# maintaining log file
		log.write("Received file path back from the client IP: \n")
		log.write(str(addr))
		log.write("\n")
		log.write("File path sent from the client: \n")
		log.write(str(file_path))
		log.write("\n")
		log.write("File path received at date and time: \n")
		log.write(str(datetime.datetime.now()))
		log.write("File path received at server IP: \n")
		log.write(str(serverIP))
		log.write("\n\n")
		log.close()

    #Looking for the file based on value matching in dictionary
	for item, location in dict.iteritems():
		if file_path == location:
			#print file_path
			#print item
			print "File found, sending back to the client."
			#connectionSocket.send("Receiving file from server...")
			check = 1
			filename = os.path.join(file_path, file)

			#Searching the requested file from the directory
			for items, location in dict2.iteritems():
				#print items
				#print  location
				#if file found, send to client
				if filename == location:
					check2 = 1
					print "Sending ", filename, "..."
					#connectionSocket.send(filename)

					#Sending file to client
					toClient = open(filename, 'rb')

					data = toClient.read(1024)

					while (data):
						connectionSocket.send(data)
						data = toClient.read(1024)

					run = 0

					#connectionSocket.send(data)
					print "Voila! File sent to the client!"

					# maintaining log file
					with open('sLog.txt', 'a') as log:
						log.write("Sent final file to client through server IP: \n")
						log.write(str(serverIP))
						log.write("\n")
						log.write("Full path of Final file: \n")
						log.write(str(filename))
						log.write("\n")
						log.write("Final file sent at date and time: \n")
						log.write(str(datetime.datetime.now()))
						log.write("\n")
						log.write("Final file sent to client at client IP:")
						log.write("\n")
						log.write(str(addr))
						log.write("\n\n")
						log.close()

					#serverSocket.close()

				else:
					check2 = 0
			break

		else:
			check = 0

		if check2 == 0:
			print "File missing from server."

    #If incorrect path, do this
	if check == 0:
		print "Incorrect path sent by the client!"
		connectionSocket.send("The path you sent is incorrect! Program terminated.")
		serverSocket.close()

connectionSocket.close()
toClient.close()