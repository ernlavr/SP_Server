from src.project.parser import Parser

class TcpNetwork():
    def __init__(self):
        print("Opening a TCP socket")
        self.sceneFile = "<MyScene />"
        self.initSceneParser()

    def initSceneParser(self):
        parser = Parser(self.sceneFile) 
        # TODO port the TCP code here








# ---------------------------------------------------
## TODO Port the code below into the class TCPNetwork
import socket
import threading
import cv2
import atexit
import argparse

class Server():
    def __init__(self, ipAddress="192.168.1.214", port=8052):
        """ Single threaded server application

        Args:
            ipAddress (str, optional): IP Address to which we want to bind to. Defaults to "192.168.0.172".
            port (int, optional): Port to which we want to bind to. Defaults to 8052.
        """

        # Variable setup
        self.localIP = ipAddress
        self.localPort = port
        self.bufferSize = 1024
        self.serverAddress = (self.localIP, self.localPort)

        # Create a datagram socket
        self.TCPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

        # Bind to address and ip
        self.TCPServerSocket.bind(self.serverAddress)
        print("TCP server up and listening on endpoint {0}:{1}".format(self.localIP, self.localPort))

        # Callback function executed when the program finishes
        atexit.register(self.cleanup)

    def cleanup(self):
        print("Cleaning up resources..")
        cv2.destroyAllWindows()
        self.TCPServerSocket.close()

    def listen(self):
        # Listen for incoming connections
        print("Listening for incoming traffic..")
        self.TCPServerSocket.listen(1)

        while True:
            # Wait for a connection
            connection, client_address = self.TCPServerSocket.accept()
            print(f"Accepted connection from {client_address}")
            # Receive the data in small chunks and retransmit it
            # Look for the response
            amount_received = bytearray()
            while True:
                # Receive the data
                data = connection.recv(self.bufferSize)

                # Process the data
                amount_received = amount_received + data
                self.saveFile(None)

                if data:
                    print(f"Received {data}")
                else:
                    print(f"No more data")
                    self.processImage(amount_received)
                    self.decodeData(amount_received)
                    break

                    # pass the output it to parser

    def decodeData(self, data):
        gray = cv2.cvtColor(data, cv2.COLOR_GRAY2BGR)
        cv2.imshow('frame', gray)


    def saveFile(self, data, path):
        """Decodes the binary data as XML and saves it to the path

        Args:
            data ([type]): [description]
            path ([type]): Path relative from the main entry point to a file in res directory
        

        """
        # For inspiration..
        # 1. Decode the data bytes to a string
        # 2. Create a blank text file at the given path
        # 3. Dump the decoded data bytes to the file
        return True

def main():
  # Prep args
  parser = argparse.ArgumentParser(description='Process some integers.')
  parser.add_argument('-l', action='store_true', help='Initialize the server on localhost and default port (8050)')
  parser.add_argument('-i', type=str, help='IP Address for the server (you cannot bind to an IP address that your PC doesnt have! Use if/ipconfig as help)')
  parser.add_argument('-p', type=int, help='TCP port')
  args = parser.parse_args()

  # Prep vars
  serv: Server = None
  argIp = args.i
  argPort = args.p

  # Handle args
  if(args.l):
    argIp = "127.0.0.1"

  if(argIp and argPort is not None):
      serv = Server(argIp, argPort)
  elif(argIp is not None):
      serv = Server(argIp)
  elif(argPort is not None):
      serv = Server(port=argPort)
  else:
      serv = Server()

  serv.listen()

if __name__ == "__main__":
  main()