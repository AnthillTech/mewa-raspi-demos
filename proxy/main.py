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
LOCAL_SERVER_URL = "192.168.1.1"
# LOCAL_SERVER_URL = "icplayer.com"



def run():
    tunnelServerUrl = "ws://" + TUNNELING_SERVER + "/_ws/" + DEVICE_NAME
    socket = create_connection(tunnelServerUrl)
    while True:
        msg = socket.recv().decode("utf-8")
        parsedMsg = parseMessage(msg)
        response = callWebserver(parsedMsg["method"], parsedMsg["path"], parsedMsg["headers"], parsedMsg["body"])
        headers = buildHeaders(parsedMsg["msgId"], response)
        body = response.read()
        resp = bytes(headers) + body
        socket.send_binary(resp)
        
        
def parseMessage(msg):
    ''' (msgId, method, path, body) '''
    sections = msg.split("\n\n")
    lines = sections[0].split("\n")
    body = sections[1]
    headers = {}
    for i in range (3, len(lines)):
        index = lines[i].index(":")
        if index > 0 and index < len(lines[i])-1:
            k = lines[i][:index]
            v = lines[i][index+1:]
            headers[k] = v
    return {"msgId": lines[0], 
            "method": lines[1], 
            "path": lines[2], 
            "headers": headers,
            "body": body }


def buildHeaders(msgId, response):
    headers = msgId + "\n" + str(response.status) + "\n"
    for (k,v) in response.getheaders():
        headers += k + ":" + v + "\n"
    return headers + "\n"
        

def callWebserver(method, path, headers, body):
    conn = httplib.HTTPConnection(LOCAL_SERVER_URL)
    conn.request(method, path, body, headers)
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
    
