# =============================================================================
# Specification
#
# =============================================================================

from websocket import create_connection, WebSocketTimeoutException
import socket
import time
import json
import Protocol


MEWA_SERVER = "localhost:9000"
DEVICE_NAME = "simulator"
CHANNEL_NAME = "test"
PASSWORD = "test"

STATUS_NOCONNECTION = 0    
STATUS_CONNECTING = 1
STATUS_CONNECTED = 2

class Connection:

    def __init__(self, server, services):
        self._services = services
        self._serverUrl = "ws://%s/ws" % server
        self._status = STATUS_NOCONNECTION
         
    def run(self, channel, device, password):
        while True:
            self._ws = None
            try:
                self._ws = create_connection(self._serverUrl, timeout=1)
                self._connectToChannel(channel, device, password)
                self._status = STATUS_CONNECTING
                while self._status != STATUS_NOCONNECTION:
                    packet = self._readPacket()
                    if self._status == STATUS_CONNECTING:
                        self._processConnecting(packet)
                    elif self._status == STATUS_CONNECTED:
                        self._processConnected(packet)
                    # Based on status call processing routine
            except Exception as e:
                print(e)
            if self._ws != None:
                self._ws.close()
            print("connection closed. Reconnect in 5 seconds...")
            time.sleep(5)
            
    def _connectToChannel(self, channel, device, password):
        packet = Protocol.connect(channel, device, password, [""])
        self.send(packet)
            
    def _readPacket(self, ):
        ''' Read packet and return json representation '''
        try:
            packet = self._ws.recv()
            data = json.loads(packet)
        except WebSocketTimeoutException:
            data = {}
        return data
            
    def send(self, packet):
        self._ws.send(packet)
            
    def _processConnecting(self, packet):
        ''' Processing while waiting for connection '''
        if packet['type'] == 'connected':
            self._status = STATUS_CONNECTED
        else:
            self._status = STATUS_NOCONNECTION
            
    def _processConnected(self, packet):
        ''' Processing while connected to the channel '''
        if 'type' in packet:
            if packet['type'] == 'message':
                self._processMessage(packet)
            elif packet['type'] == 'event':
                self._processEvent(packet)
                
    def _processMessage(self, packet):
        if packet['id'] == 'org.fi24.discovery.GetServices':
            packet = Protocol.sendMessage(packet['device'], "org.fi24.discovery.ServiceList", self._services)
            self.send(packet)
                
    def _processEvent(self, packet):
        print("Received event:")
        print(packet)


        
if __name__ == "__main__":
    connection = Connection(MEWA_SERVER, ["org.fi24.temperature"])
    connection.run(CHANNEL_NAME, DEVICE_NAME, PASSWORD)
    
