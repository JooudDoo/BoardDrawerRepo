
import warnings

import cv2
from imutils.video import VideoStream

from .VideoHandler import VideoHandler

# DEPRECATED
class CameraHandler(VideoHandler):

    def __init__(self, videoStreamSource=0):
        warnings.warn("Module deprecated and should be removed", DeprecationWarning)
        super().__init__(videoStreamSource)