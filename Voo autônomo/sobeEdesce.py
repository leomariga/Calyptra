# -*- coding: utf-8 -*-
from dronekit import VehicleMode, connect
import argparse
import os
import time

os.environ['MAVLINK20'] = '1'




parser = argparse.ArgumentParser(description='Play tune on vehicle buzzer.')
vehicle = connect('/dev/ttyAMA0,57600',wait_ready=True)

print "Starting mission"
# Set mode to AUTO to start mission


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



while True:
        print(vehicle.channels['6'])
        print(vehicle.mode.name)
        if(vehicle.channels['6'] > 1500):
                arm_and_takeoff(12)
                time.sleep(10)
                vehicle.mode = VehicleMode("LAND")
        else:
                if(vehicle.mode.name=='ALT_HOLD'):
                    print "Encerra loop"
                    time.sleep(0.5)
                    break

print("Completed")
