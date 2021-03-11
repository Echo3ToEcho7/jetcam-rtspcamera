from jetcam.camera import Camera
import atexit
import cv2
import numpy as np
import threading
import traitlets


class RTSPCamera(Camera):
    
    capture_width = traitlets.Integer(default_value=1280)
    capture_height = traitlets.Integer(default_value=720)   
    capture_latency = traitlets.Integer(default_value=200)   
    capture_url = traitlets.Unicode(default_value="rtsp://192.168.1.99")
    capture_decoder = traitlets.Enum(["h264", "h265"], default_value="h265")
    
    def __init__(self, *args, **kwargs):
        super(RTSPCamera, self).__init__(*args, **kwargs)
        try:
            self.cap = cv2.VideoCapture(self._gst_str(), cv2.CAP_GSTREAMER)

            print(self._gst_str())
            re , image = self.cap.read()
            
            if not re:
                raise RuntimeError('Could not read image from camera.')
            
        except:
            raise RuntimeError(
                'Could not initialize camera.  Please see error trace.')

        atexit.register(self.cap.release)
                
    def _gst_str(self):
        return ('rtspsrc location={0} latency={1} ! '
               'rtp{4}depay ! {4}parse ! omx{4}dec ! '
               'nvvidconv ! '
               'video/x-raw, width=(int){2}, height=(int){3}, format=(string)BGRx ! '
               'videoconvert ! appsink max-buffers=1 drop=true').format(self.capture_url, self.capture_latency, self.capture_width, self.capture_height, self.capture_decoder)
    
    def _read(self):
        re, image = self.cap.read()
        if re:
            image_resized = cv2.resize(image,(int(self.width),int(self.height)))
            return image_resized
        else:
            raise RuntimeError('Could not read image from camera')

    def isOpened(self):
        return self.cap.isOpened()
