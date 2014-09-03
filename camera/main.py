'''
Created on 2014-09-01

@author: Krzysztof Langner
'''

from mewa.client import Connection
import base64    

URI_IMAGE_SERVICE = "org.fi24.image"
URI_IMAGE_GETIMAGE = "org.fi24.image.GetImage"
URI_IMAGE_IMAGE = "org.fi24.image.Image"


#connection = Connection("ws://mewa.cc/ws")
connection = Connection("ws://localhost:9000/ws")

def onMessage(timestamp, fromDevice, msgId, params):
    if msgId == URI_IMAGE_GETIMAGE:
        with open("owl.jpg", "rb") as image_file:
            image = "data:image/png;base64," + base64.b64encode(image_file.read())
            connection.sendMessage(fromDevice, URI_IMAGE_IMAGE, {"data":image})
    elif msgId == "org.fi24.discovery.GetServices":
        connection.sendMessage(fromDevice, "org.fi24.discovery.ServiceList", ["org.fi24.discovery", URI_IMAGE_SERVICE])
    
    
def onError(reason):
    print("Error: " + reason)
    

if __name__ == "__main__":
    connection.onMessage = onMessage
    connection.onError = onError
    connection.connect("test", "camera", "test")


