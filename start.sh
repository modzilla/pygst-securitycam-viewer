#!/bin/bash
./gstreamer -v rtspsrc location="rtsp://stream:stream@10.10.255.223/axis-media/media.amp" ! rtpmp4depay ! mpeg4videoparse ! ffdec_mpeg4 ! ffmpegcolorspace ! autovideosink
