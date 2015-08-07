#!/usr/bin/python

import pygst
pygst.require("0.10")
import gst
import pygtk
import gtk

class Main:
    def __init__(self):
        self.pipeline = gst.parse_launch("rtspsrc name=source latency=0 ! autovideosink")
	self.source = self.pipeline.get_by_name("source")
	self.source.props.location = "rtsp://stream:stream@10.10.255.223/axis-media/media.amp"
	print "CREATED PIPELINE"
	print str(self.source.props.location)
	print str(self.pipeline)
        
        self.pipeline.set_state(gst.STATE_PLAYING)
	print "PLAYING"

start=Main()
gtk.main()
