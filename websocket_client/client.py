import _thread
import time
import datetime
import asyncio 
import websockets

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


if __name__ == '__main__':
    # connect to server 
    asyncio.get_event_loop().run_until_complete(get_connect());
    #asyncio.get_event_loop().run_forever(get_connect());