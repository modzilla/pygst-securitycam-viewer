#!/usr/bin/env python

import gobject
gobject.threads_init()
import gst

import pygtk
pygtk.require("2.0")
import gtk
gtk.gdk.threads_init()
import sys
import os

class DemoException(Exception):
    
    def __init__(self, reason):
        self.reason = reason

class Demo:

    __name__ = "Camviewer"
    __usage__ = "python rcam.py --- starts the camera monitor"
    __def_win_size__ = (960, 540)        
 
    def createPipeline(self, w):
     
        def set_xid(window):
            gtk.gdk.threads_enter()
            sink.set_xwindow_id(window.window.xid)
            sink.expose()
            gtk.gdk.threads_leave()


        def bus_handler(unused_bus, message):
            if message.type == gst.MESSAGE_ELEMENT:
                if message.structure.get_name() == 'prepare-xwindow-id':
                    set_xid(w)
            return gst.BUS_PASS

        self.pipeline = gst.parse_launch("rtspsrc name=source latency=100 ! decodebin")
	print str(self.pipeline)
        self.src = self.pipeline.get_by_name("source")
	self.src.props.location = "rtsp://stream:stream@10.10.255.223/axis-media/media.amp"
	print str(self.src.props)
	bus = self.pipeline.get_bus()
        bus.set_sync_handler(bus_handler)

        sink = gst.element_factory_make("ximagesink", "sink")
        sink.set_property("force-aspect-ratio", True)
        sink.set_property("handle-expose", True)
        scale = gst.element_factory_make("videoscale", "scale")
        cspace = gst.element_factory_make("ffmpegcolorspace", "cspace")

        self.pipeline.add(cspace, scale, sink)
        scale.link(sink)
        cspace.link(scale)
        self.pipeline.set_state(gst.STATE_PLAYING)
	return (self.pipeline, cspace)

    def customWidgets(self):
        return gtk.HBox()

    def createWindow(self):

        w = gtk.Window()
        w.set_size_request(*self.__def_win_size__)
        w.set_title(self.__name__)
        w.connect("destroy", gtk.main_quit)

        controls = (
            ("play_button", gtk.ToolButton(gtk.STOCK_MEDIA_PLAY), self.onPlay),
            ("stop_button", gtk.ToolButton(gtk.STOCK_MEDIA_STOP), self.onStop),
            ("quit_button", gtk.ToolButton(gtk.STOCK_QUIT), gtk.main_quit)
        )

        box = gtk.HButtonBox()

        for name, widget, handler in controls:
            widget.connect("clicked", handler)
            box.pack_start(widget, True)
            setattr(self, name, widget)
        
        viewer = gtk.DrawingArea()
        viewer.modify_bg(gtk.STATE_NORMAL, viewer.style.black)
        
        self.xid = None
        
        layout = gtk.VBox(False)
        layout.pack_start(viewer)

        layout.pack_start(self.customWidgets(), False, False)
        layout.pack_end(box, False, False)
        w.add(layout)
        w.show_all()

        return viewer

    def onPlay(self, unused_button):
        self.pipeline.set_state(gst.STATE_PLAYING)

    def onStop(self, unused_button):
        self.pipeline.set_state(gst.STATE_READY)

    def run(self):
        w = self.createWindow()
        p, s = self.createPipeline(w)
        try:
            gtk.main()
        except DemoException, e:
            print e.reason
            print self.__usage__
            sys.exit(-1)

if __name__ == '__main__':
    Demo().run()
