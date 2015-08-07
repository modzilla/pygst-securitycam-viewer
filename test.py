import pygst
pygst.require("0.10")
import gst

import time

import pygtk
import gtk


pipeline = gst.parse_launch("rtspsrc name=source latency=0 ! decodebin ! autovideosink")
source = pipeline.get_by_name("source")
source.props.location = "rtsp://stream:stream@10.10.255.223/axis-media/media.amp"
pipeline.set_state(gst.STATE_PLAYING)

gtk.main()


