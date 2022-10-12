import _thread
import threading
import time
import datetime
import asyncio 
import websockets
import socket

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")


async def get_connect():
    async with websockets.connect("ws://localhost:30001") as websocket:
        # for i in range(1,100,1):
        #     await websocket.send("Hi server. I'm client" );
        #     data_rcv = await websocket.recv(); 
        #     print("data received from server : " + data_rcv); 
        await websocket.send("Hi server. I'm client" );
        
        while True:
            now = datetime.datetime.now()
            msg_rcv = await websocket.recv(); 
            print('[%s] %s' % (now, msg_rcv)) 
        
        # print("data received from server : " + data_rcv); 

def get_connect_by_socket():
    global client
    client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect(('192.168.219.106',30001))

    thr=threading.Thread(target=consoles,args=())
    thr.Daemon=True
    thr.start()

def consoles():
     while True:
        msg = client.recv(1024)
        message = msg.decode()
        if(message != None):
            print(message)
        elif(msg.decode()=='down'):
            eney+=30
        elif(msg.decode()=='right'):
            enex+=30
        elif(msg.decode()=='left'):
            enex-=30

if __name__ == '__main__':
    # connect to server 
    #asyncio.get_event_loop().run_until_complete(get_connect());
    #asyncio.get_event_loop().run_forever(get_connect());
    get_connect_by_socket()