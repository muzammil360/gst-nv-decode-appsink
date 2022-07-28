import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
Gst.init(None)

import time
import numpy as np
import matplotlib.pyplot as plt

from DataReader import DataReader 



# config
RTSP_STREAM_H264 = 'rtsp://admin:2Mini001.@192.168.88.52'
RTSP_STREAM_H265 = 'rtsp://admin:2Mini001.@192.168.88.58'
PIPELINE_H264 = '''
	rtspsrc location={location} ! rtph264depay ! h264parse ! nvv4l2decoder 
    ! nvvideoconvert ! video/x-raw, format=BGR
	! appsink
	'''.format(location = RTSP_STREAM_H264)
PIPELINE_H265 = '''
	rtspsrc location={location} ! rtph265depay ! h265parse ! nvv4l2decoder 
    ! nvvideoconvert ! video/x-raw, format=BGR
	! appsink
	'''.format(location = RTSP_STREAM_H265)

PIPELINE = PIPELINE_H264
MAINLOOP_PAUSE_SEC = 0.1


def printBufferShape(buf):
    if buf is not None: 
        print("bufer.shape: ", buf.shape)


def main():
    pipeline = PIPELINE
    mainloop_pause_sec = MAINLOOP_PAUSE_SEC

    # make reader 
    reader0 = DataReader(pipeline,0)
    reader0.start()
    
    reader1 = DataReader(pipeline,1)
    reader1.start()


    while(True):
        buffer0 = reader0.readBuffer()
        buffer1 = reader1.readBuffer()

        printBufferShape(buffer0)
        printBufferShape(buffer1)
    
        time.sleep(MAINLOOP_PAUSE_SEC)

if __name__ == '__main__':
    
    try:
        main()
    except KeyboardInterrupt as exp:
        plt.close('all')
