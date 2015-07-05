###############################################################################
##
##  Copyright (C) 2014, Tavendo GmbH and/or collaborators. All rights reserved.
##
##  Redistribution and use in source and binary forms, with or without
##  modification, are permitted provided that the following conditions are met:
##
##  1. Redistributions of source code must retain the above copyright notice,
##     this list of conditions and the following disclaimer.
##
##  2. Redistributions in binary form must reproduce the above copyright notice,
##     this list of conditions and the following disclaimer in the documentation
##     and/or other materials provided with the distribution.
##
##  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
##  AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
##  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
##  ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
##  LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
##  CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
##  SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
##  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
##  CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
##  ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
##  POSSIBILITY OF SUCH DAMAGE.
##
###############################################################################

from twisted.internet.defer import inlineCallbacks

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError
from openni import *


class AppSession(ApplicationSession):

    @inlineCallbacks
    def onJoin(self, details):
        print "Entering onJoin"
        ## SUBSCRIBE to a topic and receive events
        ##
        def onhello(msg):
            print("event for 'onhello' received: {}".format(msg))

        sub = yield self.subscribe(onhello, 'com.example.onhello')
        print("subscribed to topic 'onhello'")


        ## REGISTER a procedure for remote calling
        ##
        def add2(x, y):
            print("add2() called with {} and {}".format(x, y))
            return x + y

        reg = yield self.register(add2, 'com.example.add2')
        print("procedure add2() registered")



# Pose to use to calibrate the user
        pose_to_use = 'Psi'

#initialise openni
        ctx = Context()
        ctx.init()

#create gesture to try and stop create user crashing
# (https://github.com/jmendeth/PyOpenNI/issues/15)
        gest = GestureGenerator()
        gest.create(ctx)

# Create the user generator
        user = UserGenerator()
        user.create(ctx)

# Obtain the skeleton & pose detection capabilities
        skel_cap = user.skeleton_cap
        pose_cap = user.pose_detection_cap

# Declare the callbacks
        def new_user(src, id):
            print "1/4 User {} detected. Looking for pose..." .format(id)
            pose_cap.start_detection(pose_to_use, id)

        def pose_detected(src, pose, id):
            print "2/4 Detected pose {} on user {}. Requesting calibration..." .format(pose,id)
            pose_cap.stop_detection(id)
            skel_cap.request_calibration(id, True)

        def calibration_start(src, id):
            print "3/4 Calibration started for user {}." .format(id)

        def calibration_complete(src, id, status):
            if status == CALIBRATION_STATUS_OK:
                print "4/4 User {} calibrated successfully! Starting to track." .format(id)
                skel_cap.start_tracking(id)
            else:
                print "ERR User {} failed to calibrate. Restarting process." .format(id)
                new_user(user, id)

        def lost_user(src, id):
            print "--- User {} lost." .format(id)

# Register them
        user.register_user_cb(new_user, lost_user)
        pose_cap.register_pose_detected_cb(pose_detected)
        skel_cap.register_c_start_cb(calibration_start)
        skel_cap.register_c_complete_cb(calibration_complete)

# Set the profile
        skel_cap.set_profile(SKEL_PROFILE_ALL)

# Start generating
        ctx.start_generating_all()
        print "0/4 Starting to detect users. Press Ctrl-C to exit."



        ## PUBLISH and CALL every second .. forever
        ##
        counter = 0
        self.publish('com.example.counter', "Starting to look for stuff")
        while True:
            #self.publish('com.example.counter', "Starting to look for stuff")


            # Update to next frame
            ctx.wait_and_update_all()
    
            # Extract head position of each tracked user
            for id in user.users:
                if skel_cap.is_tracking(id):
                    head = skel_cap.get_joint_position(id, SKEL_HEAD)
                    #print "  {}: head at ({loc[0]}, {loc[1]}, {loc[2]}) [{conf}]" .format(id, loc=head.point, conf=head.confidence)
            
                    if head.point[2] < 900:
                        msg =  "0.25"
                        print msg
                        self.publish('com.example.counter', msg)
                    elif 900 < head.point[2] < 1500:
                        msg =  "0.25"
                        print msg
                        self.publish('com.example.counter', msg)
                    elif 1500 < head.point[2] < 2100:
                        msg =  "0.5"
                        print msg
                        self.publish('com.example.counter', msg)
                    elif 2100 < head.point[2] < 2700:
                        msg =  "1"
                        print msg
                        self.publish('com.example.counter', msg)
                    elif 2700 < head.point[2] < 3300:
                        msg =  "2"
                        print msg
                        self.publish('com.example.counter', msg)
                    else:
                        msg =  "4"
                        print msg
                        self.publish('com.example.counter', msg)
                





            yield sleep(0.1)
