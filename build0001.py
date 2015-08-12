import pygst
import gst
import pygtk
import gtk

def bus_handler(unused_bus,message):
	print "\033[95mMSGRCV: " + str(message.type) + "\033[0m"
	if message.type == gst.MESSAGE_ERROR:
		print "\033[91mERROR: " + str(message)
		print "\033[0m"
	elif message.type == gst.MESSAGE_INFO:
		print "\033[93mINFO : " + str(message)
		print "\033[0m"
	elif message.type == gst.MESSAGE_WARNING:
		print "\033[93mWARN : " + str(message)
		print "\033[0m"
	elif message.type == gst.MESSAGE_ELEMENT:
		print "\033[92mMSG  : " + str(message)
		print "\033[0m"
		if message.structure.get_name() == "prepare-xwindow-id":
			print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
			set_xid()
	
	return gst.BUS_PASS

def rm_pad(obj,pad,udata):
	print "pad removed"

def set_xid():
	gtk.gdk.threads_enter()
	sink.set_xwindow_id(xid)
	sink.expose()
	gtk.gdk.threads_leave()

def on_new_pad(dbin,pad,islast):
	print "DECO PAD ADDED"
	#deco = pad.get_parent()
	#pipe = deco.get_parent()
	pad.link(src.get_static_pad("sink"))

	pipe.set_state(gst.STATE_PLAYING)

def on_new_sink_pad(dbin,pad,islast):
	print "SINK PAD ADDED"
	#sink = pad.get_parent()
	#pipe = sink.get_parent()
	deco.link(scale)
	pipe.set_state(gst.STATE_PLAYING)

gtk.gdk.threads_init()

window = gtk.Window(gtk.WINDOW_TOPLEVEL)
draw = gtk.DrawingArea()
draw.modify_bg(gtk.STATE_NORMAL, draw.style.black)
window.add(draw)

window.set_default_size(640,480)
window.set_title("Camviewer")
window.show_all()

xid = draw.window.xid
print str(xid)
xidx = window.window.xid
print str(xidx)

#pipe = gst.parse_launch("rtspsrc name=source ! decodebin name=deco ! xvimagesink name=xvimagesink")
pipe = gst.Pipeline()
print str(pipe)
sink = gst.element_factory_make("ximagesink","ximagesink")
print str(sink)
deco = gst.element_factory_make("decodebin","decode")
print str(deco)
src = gst.element_factory_make("rtspsrc","source")
print str(src)
scale = gst.element_factory_make("videoscale", "scale")
print str(scale)

bus = pipe.get_bus()
print str(bus)
bus.set_sync_handler(bus_handler)

pipe.add(sink,deco,scale,src)
scale.link(sink)
#src.link(deco)
#deco.link(sink)

src.props.location = "rtsp://stream:stream@10.10.255.223/axis-media/media.amp"

deco.connect("pad-added", on_new_pad)
deco.connect("pad-removed", rm_pad)
print "Decoder pad listener added"

sink.set_property("force-aspect-ratio",True)
sink.set_property("handle-expose",True)
sink.connect("pad-added",on_new_sink_pad)
print "Sink pad listener added"

pipe.set_state(gst.STATE_PLAYING)
sink.set_xwindow_id(draw.window.xid)
gtk.main()