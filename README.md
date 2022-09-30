# SocketProgram
COSC264 | Assignment 1 | Semester 2 | Grade recieved 87.75%

My task was to write two programs in Python. The first one, called server will allow the other program, called
client, to ask the server for the current date or time of day. The server offers to deliver these in three different
languages.
The programs required two different types of packets to be used: DT-Request and DT-Response packets (where
’DT’ stands for “DateTime”). With a DT-Request a client requests either the date or the current time of day
from the server. With a DT-Response packet the server returns both the date and current time of day in a binary
representation, followed by either the date or the time of day (depending on the client’s choice) in a textual
representation.

TO RUN THE PROGRAM:
  – Open one terminal on your machine and start the server, handing over the port number to which the
  server should bind as a parameter on the command line.
  – Open another terminal on the same computer and start the client. For the second parameter (hostname
  / IP address of the server) you can use the IP address 127.0.0.1, which refers to ’this host’ without
  needing to specify any actual IP address of this host. For the port name parameter please use the port
  number that you have started the server with.
