#!/bin/bash
gst-launch-1.0 -v rtspsrc location=rtsp://stream:stream@10.10.255.223/axis-media/media.amp \
latency=200 ! decodebin ! autovideosink framerate=60
