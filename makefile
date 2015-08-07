test = gstreamer
ext = c
CC = gcc
CPP = g++
gstreamer:
	$(CC) -g $(test).$(ext) -o $(test) `pkg-config gstreamer-0.10 --libs --cflags` `pkg-config gtk+-2.0 --libs --cflags`
clean:
	rm -rf $(test)
