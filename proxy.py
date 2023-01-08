from socket import *
import sys 

if len(sys.argv) <= 1:
    print ('Usage : "python ProxyServer.py server_ip"\n[server_ip : It is the IP Address Of Proxy Server')
    sys.exit(2)

# Create a server socket, bind it to a port and start listening
tcpServerSock = socket(AF_INET, SOCK_STREAM)

# Fill in start.
serverPort = 12000
tcpServerSock.bind((sys.argv[1], serverPort))
tcpServerSock.listen(10)
# Fill in end.

# Blocked urls
with open('blocked.txt') as f:
    blocked_websites = set(f.read().splitlines())

while 1:
    # Start receiving data from the client
    print ('\n\nReady to serve...')
    tcpClientSock, addr = tcpServerSock.accept()
    print ('Received a connection from:', addr)
    # Fill in start.
    message = tcpClientSock.recv(1024)
     # Fill in end.
    if message:
        print(message)
        filename = message.split()[1].decode("utf-8").rpartition("/")[2]
        filename2 = message.split()[1].decode("utf-8")

        if not ( filename2 in blocked_websites):
            fileExist = "false"
            filetouse = "\\cache\\" + filename
            print("The File is not blocked")


            try:
                # Check wether the file exist in the cache
                f = open(filetouse[1:], "rb")
                outputdata = f.readlines()
                fileExist = "true"
                # ProxyServer finds a cache hit and generates a response message
                tcpClientSock.send(b"HTTP/1.0 200 OK\r\n")
                tcpClientSock.send(b"Content-Type:text/html\r\n")
                # Fill in start.
                for line in outputdata:
                    tcpClientSock.send(line)
                f.close()
                # Fill in end.
                print ('Read from cache')
            # Error handling for file not found in cache
            except IOError:
                try:
                    if fileExist == "false":
                        print("File not found in cache")
                        # Create a socket on the proxyserver
                        c = socket(AF_INET, SOCK_STREAM)
                        # Fill in start. # Fill in end.
                        hostname = message.split()[4].decode("utf-8")
                        print( "hostn is "+hostname)
                        
                        
                        print('Attempting cache')
                        # Connect to the socket to port 80
                        # Fill in start.
                        c.connect((hostname, 80))
                        # Fill in end.
                        # Create a temporary file on this socket and ask port 80 for the file requested by the client
                        fileobj = c.makefile("w", None)
                        fileobj.write("GET " + filename2 + " HTTP/1.0\n\n")
                        fileobj.close()
                        # Read the response into buffer
                        # Fill in start.
                        print('cache complete')
                        fileobj = c.makefile('rb', None)
                        buffer = fileobj.readlines()
                        # Fill in end.
                        # Create a new file in the cache for the requested file.
                        # Also send the response in the buffer to client socket and the corresponding file in the cache
                        
                        tmpFile = open("./cache/" + filename, "wb")
                        
                        # Fill in start.
                        for line in buffer:
                            tmpFile.write(line)
                            tcpClientSock.send(line)
                        # Fill in end.
                        tmpFile.close()
                        c.close()
                except:
                    print ("Illegal request")
        else:
            print("The website is blocked")

            tcpClientSock.close()
            print("Socket Closed")   
    else:
        ...
        # HTTP response message for file not found
        tcpClientSock.send("HTTP/1.0 404 sendError\r\n")
        tcpClientSock.send("Content-Type:text/html\r\n")
        # Close the client and the server sockets
        tcpClientSock.close()
        print("socket closed")

