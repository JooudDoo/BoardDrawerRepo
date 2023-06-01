
import cv2
from imutils.video import VideoStream

class VideoHandler():

    def __init__(self, videoStreamSource=None):
        self._videoStream = VideoStream(src=videoStreamSource).start()
        self.current_source = videoStreamSource

        self.status = 200
        frame = self._videoStream.read()
        if frame is None:
            self.status = 500

    def change_source(self, new_src):
        """
        Меняем источник видео потока
        Если новый источник не выдает кадры сменяем обратно
        """
        status = 0
        del self._videoStream
        try:
            self._videoStream = VideoStream(src=new_src).start()
            frame = self._videoStream.read()
        except:
            frame = None

        
        if frame is None:
            self.change_source(self.current_source)
        else:
            status = 1
            self.current_source = new_src
        return status

    def getFrame(self, size: tuple[int, int] = (0, 0)):
        frame = self._videoStream.read()
        if frame is None:
            self.change_source(self.current_source)
            return self.getFrame(size)
        if size != (0, 0):
            frame = cv2.resize(frame, size)
        return frame

    def __del__(self):
        self._videoStream.stop()