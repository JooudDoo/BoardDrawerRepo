
import cv2
from imutils.video import VideoStream

class CameraHandler():

    def __init__(self, videoStreamSource=0):
        self._videoStream = VideoStream(src=videoStreamSource).start()

    def getFrame(self, size: tuple[int, int] = (0, 0)):
        frame = self._videoStream.read()
        # if not checkCode:
        #    raise Exception("Frame not received")
        if size != (0, 0):
            frame = cv2.resize(frame, size)
        return frame

    def __del__(self):
        self._videoStream.stop()
