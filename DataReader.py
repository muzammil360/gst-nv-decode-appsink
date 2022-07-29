import gi

gi.require_version('GstApp', '1.0')
from gi.repository import GObject, Gst, GstApp

import multiprocessing
import numpy


class DataReader():

    def __init__(self, pipeline_str, idx=0):
        self.pipeline_str = pipeline_str
        self.idx = str(idx)

        # make pipeline object from string
        self.pipeline = Gst.parse_launch(self.pipeline_str)

        # configure app sink
        self.appsink = self.pipeline.get_by_name('appsink'+self.idx)
        self.appsink.set_property("emit-signals", True)     # needed if we want 'new-sample' callback to work
        self.appsink.connect("new-sample", newSampleCb, self)


        # get and configure bus
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect("message", self.onMessage)

        self.output_array = None

        # create main event loop object
        self.mainloop = GObject.MainLoop()

        # thread to make pipeline non-blocking
        threadFunc = self.mainloop.run
        self.thread = multiprocessing.Process(target=threadFunc, daemon=True)


    def start(self):
        print('starting pipeline')
        self.pipeline.set_state(Gst.State.PLAYING)
        self.thread.start()
        

    def stop(self):
        print('stoping pipeline')
        self.pipeline.set_state(Gst.State.NULL)
        self.thread.join()

    def readBuffer(self):

        output = self.output_array
        self.output_array = None
        return output


    def onMessage(self, bus, message):
        '''
        handles the messages posted on bus
        '''

        structure = message.get_structure()
        if structure is None:
            return


        if message.type == Gst.MessageType.EOS:
            self.pipeline.set_state(Gst.State.NULL)
            print('End of stream: {}'.format(message))

        elif message.type == Gst.MessageType.ERROR:
            self.pipeline.set_state(Gst.State.NULL)
            err, debug = message.parse_error()
            print("Error message: {}".format(err))
            print("Debug message: {}".format(debug))
        else:
            print("unhandled message received on bus")


def gst_to_opencv(sample):
    buf = sample.get_buffer()
    caps = sample.get_caps()
    # print("caps.get_structure(0): ", caps.get_structure(0))
    # print(caps.get_structure(0).get_value('format'))
    # print(caps.get_structure(0).get_value('height'))
    # print(caps.get_structure(0).get_value('width'))

    # print(buf.get_size())
    height = caps.get_structure(0).get_value('height')
    width = caps.get_structure(0).get_value('width')

    arr = numpy.ndarray((height, width,3),
                        buffer=buf.extract_dup(0, buf.get_size()),
                        dtype=numpy.uint8)


    return arr

def newSampleCb(appsink, userdata):
    # global output_buffer
    sample = appsink.emit("pull-sample")
    userdata.output_array = gst_to_opencv(sample)
    # print('new buffer received')

    return Gst.FlowReturn.OK
