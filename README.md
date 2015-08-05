# Current  Team Triple R's Govhack project

THINGS WE DID FOR SETUP:

Dependencies:
(used homebrew for as many of these as possible which seemed to be important in keeping paths working properly)
-openni
-sensor
-nite
-CMake
-boost

Some of these links made apparances:
https://github.com/jmendeth/PyOpenNI/wiki/Installing-PyOpenNI
http://andrewdeniszczyc.com/blog/funicular

Then got PyOpenNI from here:
https://github.com/jmendeth/PyOpenNI/wiki/building-on-linux






THINGS TO DO TO MAKE IT WORK ONCE SETUP IS DONE:

[1]
($ pwd /Users/ruthpearson/Desktop/crossbarexamples/hello/python/hello/web)
$ python -m SimpleHTTPServer
Serving HTTP on 0.0.0.0 port 8000 ...

This makes the visualisation appear in a browser at: http://localhost:8000/

[2]
($ pwd /Users/ruthpearson/Desktop/crossbarexamples/hello/python/hello/web)
$ coffee -c -w script3.coffee 
11:58:05 - compiled /Users/ruthpearson/Desktop/crossbarexamples/hello/python/hello/web/script3.coffee

This changes the coffee script (which the visualisation is written in) to javascript which is what D3 uses for the visulisation uses.  Run this at the beginning and it will keep compiling the javascript as the coffee script changes. 

[3]
($ pwd /Users/ruthpearson/Desktop/crossbarexamples/hello/python/hello)
$ crossbar start
2015-07-05 11:53:32+1000 [Controller  25427] Log opened.
2015-07-05 11:53:32+1000 [Controller  25427] ==================== Crossbar.io ====================
	
2015-07-05 11:53:32+1000 [Controller  25427] Crossbar.io 0.10.4 starting
2015-07-05 11:53:32+1000 [Controller  25427] Running on CPython using KQueueReactor reactor
2015-07-05 11:53:32+1000 [Controller  25427] Starting from node directory /Users/ruthpearson/Desktop/crossbarexamples/hello/python/hello/.crossbar
2015-07-05 11:53:33+1000 [Controller  25427] Starting from local configuration '/Users/ruthpearson/Desktop/crossbarexamples/hello/python/hello/.crossbar/config.json'
etc

This is what runs the whole thing!  Crossbar is what we are using to make the python code (which gets the kinect input) talk to the visualisation.
