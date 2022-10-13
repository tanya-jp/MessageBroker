# Message-Broker
The message broker is responsible for sending received messages to clients. Servers should be able to do two operations, publishing and subscribing.
<p align="center">
  <img src="https://user-images.githubusercontent.com/72709191/195666447-972a70ce-8c34-4a12-b1d9-cce027d1f53e.png" width=50% height=50%>
</p>

## Protocol
Since all connections between server and clients are implemented based on `TCP`, IP and port of origin and destination are needed and after accepting each connection, server needs to know this information.
## Commands
### Client to Server
1. Publish: Sends a message from client to the server based on a specific topic.
2. Subscribe: Announces server that client wants to receive messages from given topic.
3. Ping: Ensures the connection.
4. Pong: Answers Ping from the server.
### Server to Client
1. Message: Sends the message and its topic to the client who asks for a topic.
2. SubAck: Is sent to accept the client's subscribe message, if subscribing is successful. 
3. PubAck: Is sent to accept the client's publish message, if subscribing is successful. 
4. Ping: Ensures the connection.
5. Pong: Answers Ping from the client.

- If 10 sec after sending ping to client, server does not receive any responses, it prints client's IP address and port.

## Input and Output
![image](https://user-images.githubusercontent.com/72709191/195670330-358ccf07-a4f6-46e2-b620-7db5f7bcd7a5.png)
<p align="center">
  <img src="https://user-images.githubusercontent.com/72709191/195670456-343e8534-5352-4c02-adc7-4217bf7a2c45.png" width=60% height=60%>
</p>
<p align="center">
  <img src="https://user-images.githubusercontent.com/72709191/195670476-331c97ba-af37-4325-9650-e37bb15c00d6.png" width=60% height=60%>
</p>

My report in Farsi is available [Here](https://github.com/tanya-jp/Message-Broker/blob/master/message%20broker.pdf).

