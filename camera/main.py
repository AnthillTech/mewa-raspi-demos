import picamera
from mewa.client import Connection
import base64

URI_IMAGE_SERVICE = "org.fi24.image"
URI_IMAGE_GETIMAGE = "org.fi24.image.GetImage"
URI_IMAGE_IMAGE = "org.fi24.image.Image"


connection = Connection("ws://channels.followit24.com/ws")
camera = picamera.PiCamera()
camera.resolution = (800, 600)


def onMessage(timestamp, fromDevice, msgId, params):
    if msgId == URI_IMAGE_GETIMAGE:
        camera.capture("image.jpg")
        with open("image.jpg", "rb") as image_file:
            image = "data:image/png;base64," + base64.b64encode(image_file.read())
            connection.sendMessage(fromDevice, URI_IMAGE_IMAGE, {"data":image})
    elif msgId == "org.fi24.discovery.GetServices":
        connection.sendMessage(fromDevice, "org.fi24.discovery.ServiceList", ["org.fi24.discovery", URI_IMAGE_SERVICE])


def onError(reason):
    print("Error: " + reason)


if __name__ == "__main__":
    connection.onMessage = onMessage
    connection.onError = onError
    connection.connect("channel", "camera", "password")

