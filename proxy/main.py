import time
import httplib
import datetime
from websocket import create_connection

# Where to connect with websockets
TUNNELING_SERVER = "localhost:9000"
# TUNNELING_SERVER = "followit24.com:8080"
# Unique for tunnel server device name (no spaces allowed)
DEVICE_NAME = "test"
# Provide content from this server
LOCAL_SERVER_URL = "bluenotepad.com"



def run():
    tunnelServerUrl = "ws://" + TUNNELING_SERVER + "/_ws/" + DEVICE_NAME
    socket = create_connection(tunnelServerUrl)
    while True:
        msg = socket.recv().decode("utf-8")
        (msgId, method, path, body) = parseMessage(msg)
        response = callWebserver(method, path, body)
        headers = buildHeaders(msgId, response)
        body = response.read()
        resp = bytes(headers) + body
        socket.send_binary(resp)
        
        
def parseMessage(msg):
    ''' (msgId, method, path, body) '''
    lines = msg.split("\n")
    return (lines[0], lines[1], lines[2], lines[3])


def buildHeaders(msgId, response):
        headers = msgId + "\n" + str(response.status) + "\n"
        for (k,v) in response.getheaders():
            headers += k + ":" + v + "\n"
        return headers + "\n"
        

def callWebserver(method, path, body):
        conn = httplib.HTTPConnection(LOCAL_SERVER_URL)
        conn.request(method, path, body)
        return conn.getresponse()

if __name__ == "__main__":
    while True:
        try:
            print(str(datetime.datetime.now()) + ": Starting connection")
            run()
        except Exception as e:
            print(type(e))
            print(e)
        print(str(datetime.datetime.now()) + ": Connection lost. Reconnecting in 5 seconds...")
        time.sleep( 5 )
    
