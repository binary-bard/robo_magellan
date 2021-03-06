#!/usr/bin/env python
#
# Copyright 2017 Robot Garden, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Revision $Id$

## Simple talker demo that listens to std_msgs/Strings published 
## to the 'chatter' topic

import rospy
import rospkg
from std_msgs.msg import String
import os
import commands
import soundmap
import subprocess as subp

basepath = None

def exec_cmd(command):
    # Sound sometimes doesn't play. Add padding
    shh_cmd = 'paplay ' + basepath + '/scripts/sounds/' + 'silence-1sec.wav'
    process = subp.Popen(shh_cmd, shell=True)
    # Play file
    process = subp.Popen(command, shell=True)
    process.wait()
    #os.system(command)
    # Sound sometimes doesn't play. Add padding
    shh_cmd = 'paplay ' + basepath + '/scripts/sounds/' + 'silence-1sec.wav'
    process = subp.Popen(shh_cmd, shell=True)

def callback_file(data):
    rospy.loginfo(rospy.get_caller_id() + ' Play file: %s', data.data)
    cmd = 'paplay '+data.data
    exec_cmd(cmd)

def callback_token(data):
    rospy.loginfo(rospy.get_caller_id() + ' Play token: %s', data.data)
    # Convert token to file name
    try:
        # Find the enum by token, create path, play
        fn = soundmap.SoundMapEnum.__getattr__(data.data).file_name
        path = basepath + '/scripts/sounds/' + fn
        rospy.loginfo('Path: '+path)
        cline = 'paplay '+path
        exec_cmd(cline)
    except:
        rospy.loginfo('No enum named: '+data.data)


def chatty():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('chatty', anonymous=True)

    # Get an instance of RosPack with the default search paths
    rospack = rospkg.RosPack()
    # Get file path of this package
    global basepath 
    basepath = rospack.get_path('robo_magellan')

    rospy.Subscriber('playfile', String, callback_file)
    rospy.Subscriber('play', String, callback_token)

    rospy.spin()

if __name__ == '__main__':
    chatty()
