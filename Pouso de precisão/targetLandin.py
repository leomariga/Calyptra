# -*- coding: utf-8 -*-
from dronekit import VehicleMode, connect, LocationGlobal, LocationGlobalRelative
import argparse
import os
import time
import subprocess
import math

import sys
from pymavlink import mavutil

for i in range(10):
   print i
   sys.stdout.flush()
   time.sleep(0.5)

os.environ['MAVLINK20'] = '1'

proc = subprocess.Popen(['python3', '-u','/home/pi/Desktop/adquirePos.py'],bufsize=-1, stdout=subprocess.PIPE)



parser = argparse.ArgumentParser(description='Play tune on vehicle buzzer.')
vehicle = connect('/dev/ttyAMA0,57600',wait_ready=True)

print "Starting mission"
# Set mode to AUTO to start mission
antes = time.time()
f = open('/home/pi/Desktop/logvoo.txt', 'a')
f.write("Tempo")
f.write(" ")
f.write("X_camera_angulo")
f.write(" ")
f.write("Y_camera_angulo")
f.write(" ")
f.write("X_camera")
f.write(" ")
f.write("Y_camera")
f.write(" ")
f.write("Z_camera")
f.write(" ")
f.write("Pitch_camera")
f.write(" ")
f.write("Roll_camera")
f.write(" ")
f.write("Yaw_camera")
f.write(" ")
f.write("Latitude")
f.write(" ")
f.write("Longitude")
f.write(" ")
f.write("Alt_global")
f.write(" ")
f.write("Alt_relativo")
f.write(" ")
f.write("North")
f.write(" ")
f.write("East")
f.write(" ")
f.write("Down")
f.write(" ")
f.write("Pitch")
f.write(" ")
f.write("ROll")
f.write(" ")
f.write("Yaw")
f.write("\n")
f.close()


def send_land_message(x,y,z):
   msg = vehicle.message_factory.landing_target_encode(
        0,          # time since system boot, not used
        0,          # target num, not used
        mavutil.mavlink.MAV_FRAME_BODY_OFFSET_NED, # frame, not used
        x,
        y,
        z,          # distance, in meters
        0,          # Target x-axis size, in radians
        0           # Target y-axis size, in radians
	)



   vehicle.send_mavlink(msg)
   vehicle.flush()



def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """

    print "Basic pre-arm checks"
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print " Waiting for vehicle to initialise..."
        time.sleep(1)

        
    print "Arming motors"
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True    

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:      
        print " Waiting for arming..."
        time.sleep(1)

    print "Taking off!"
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print " Altitude: ", vehicle.location.global_relative_frame.alt 
        #Break and return from function just below target altitude.        
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: 
            print "Reached target altitude"
            break
        time.sleep(1)


try:
   while True:
           #print vehicle.channels['6']
           if(vehicle.channels['6'] > 1500):
                   arm_and_takeoff(12)
                   print("takeoff")
                   #time.sleep(5)
                   sys.stdout.flush()
                   while(True):
                      line = proc.stdout.readline()
                      if line != '':
                            if(vehicle.mode.name!='LAND'):
                               vehicle.mode = VehicleMode("LAND")
                               print "mudou pra pouso"
                            else:
                               recebeu = line.rstrip().split()
                               if(len(recebeu) == 6):
                                  f = open('/home/pi/Desktop/logvoo.txt', 'a')
                                  anguloX = math.atan2(float(recebeu[0]),float(recebeu[2]))
                                  anguloY = math.atan2(float(recebeu[1]),float(recebeu[2]))
                                  f.write(str(time.time()-antes))
                                  f.write(" ")
                                  f.write(str(anguloX))
                                  f.write(" ")
                                  f.write(str(anguloY))
                                  f.write(" ")
                                  f.write(line.rstrip())
                                  f.write(" ")
                                  f.write(str(vehicle.location.global_frame.lat))
                                  f.write(" ")
                                  f.write(str(vehicle.location.global_frame.lon))
                                  f.write(" ")
                                  f.write(str(vehicle.location.global_frame.alt))
                                  f.write(" ")
                                  f.write(str(vehicle.location.global_relative_frame.alt))
                                  f.write(" ")
                                  f.write(str(vehicle.location.local_frame.north))
                                  f.write(" ")
                                  f.write(str(vehicle.location.local_frame.east))
                                  f.write(" ")
                                  f.write(str(vehicle.location.local_frame.down))
                                  f.write(" ")
                                  f.write(str(vehicle.attitude.pitch))
                                  f.write(" ")
                                  f.write(str(vehicle.attitude.roll))
                                  f.write(" ")
                                  f.write(str(vehicle.attitude.yaw))
                                  f.write("\n")
                                  f.close()
                                  #print float(recebeu[0]), " ", float(recebeu[1])," ", float(recebeu[2])," ", float(recebeu[3])," ", float(recebeu[4])," ", float(recebeu[5]) 
                                  print anguloX, " ", anguloY, " ", float(recebeu[2])
                                  send_land_message(anguloX,anguloY,float(recebeu[2]))
                               sys.stdout.flush()
                      #print(vehicle.mode.name)
                      #time.sleep(1)
                   
           else:
                   if(vehicle.mode.name=='ALT_HOLD'):
                       print "Encerra loop"
                       time.sleep(0.5)
                       break

   print("Completed")
except Exception as e:
   print e
