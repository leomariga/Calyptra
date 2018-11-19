# -*- coding: utf-8 -*-
from dronekit import VehicleMode, connect
from pymavlink import mavutil
import argparse
import os
import time
import math


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


def arm_and_takeoff_nogps(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude without GPS data.
    """

    ##### CONSTANTS #####
    DEFAULT_TAKEOFF_THRUST = 0.7
    SMOOTH_TAKEOFF_THRUST = 0.6

    print("Basic pre-arm checks")
    # Don't let the user try to arm until autopilot is ready
    # If you need to disable the arming check,
    # just comment it with your own responsibility.
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        time.sleep(1)


    print("Arming motors")
    # Copter should arm in GUIDED_NOGPS mode
    vehicle.mode = VehicleMode("GUIDED_NOGPS")
    vehicle.armed = True

    while not vehicle.armed:
        print(" Waiting for arming...")
        vehicle.armed = True
        time.sleep(1)

    print("Taking off!")

    thrust = DEFAULT_TAKEOFF_THRUST
    while True:
        current_altitude = vehicle.location.global_relative_frame.alt
        print(" Altitude: %f  Desired: %f" %
              (current_altitude, aTargetAltitude))
        if current_altitude >= aTargetAltitude*0.95: # Trigger just below target alt.
            print("Reached target altitude")
            break
        elif current_altitude >= aTargetAltitude*0.6:
            thrust = SMOOTH_TAKEOFF_THRUST
        set_attitude(thrust = thrust)
        time.sleep(0.2)


def set_attitude(roll_angle = 0.0, pitch_angle = 0.0, yaw_rate = 0.0, thrust = 0.5, duration = 0):
    """
    Note that from AC3.3 the message should be re-sent every second (after about 3 seconds
    with no message the velocity will drop back to zero). In AC3.2.1 and earlier the specified
    velocity persists until it is canceled. The code below should work on either version
    (sending the message multiple times does not cause problems).
    """
    
    """
    The roll and pitch rate cannot be controllbed with rate in radian in AC3.4.4 or earlier,
    so you must use quaternion to control the pitch and roll for those vehicles.
    """
    
    # Thrust >  0.5: Ascend
    # Thrust == 0.5: Hold the altitude
    # Thrust <  0.5: Descend
    try:
        msg = vehicle.message_factory.set_attitude_target_encode(
            0, # time_boot_ms
            1, # Target system
            1, # Target component
            0b00000000, # Type mask: bit 1 is LSB
            to_quaternion(roll_angle, pitch_angle), # Quaternion
            0, # Body roll rate in radian
            0, # Body pitch rate in radian
            math.radians(yaw_rate), # Body yaw rate in radian
            thrust  # Thrust
        )
        vehicle.send_mavlink(msg)

        start = time.time()
        while time.time() - start < duration:
            vehicle.send_mavlink(msg)
            time.sleep(0.1)
    except Exception as e:
        print e


def to_quaternion(roll = 0.0, pitch = 0.0, yaw = 0.0):
    """
    Convert degrees to quaternions
    """
    t0 = math.cos(math.radians(yaw * 0.5))
    t1 = math.sin(math.radians(yaw * 0.5))
    t2 = math.cos(math.radians(roll * 0.5))
    t3 = math.sin(math.radians(roll * 0.5))
    t4 = math.cos(math.radians(pitch * 0.5))
    t5 = math.sin(math.radians(pitch * 0.5))

    w = t0 * t2 * t4 + t1 * t3 * t5
    x = t0 * t3 * t4 - t1 * t2 * t5
    y = t0 * t2 * t5 + t1 * t3 * t4
    z = t1 * t2 * t4 - t0 * t3 * t5

    return [w, x, y, z]


        

while True:
        if(vehicle.channels['6'] > 1500):
                if(vehicle.mode.name=='STABILIZE'):
                        try:
                            print('arm_and_takeoff')
                            # Take off 5m in GUIDED_NOGPS mode.
                            #arm_and_takeoff_nogps(5)
                            arm_and_takeoff(10)
                            
                            # Hold the position for 3 seconds.
                            print("Segura posição por 3 segundos")
                            time.sleep(3)
                            print("MUDA PARA GUIDED NO GPS")
                            vehicle.mode = VehicleMode("GUIDED_NOGPS")
                            set_attitude(duration = 3)

                            print("Iniciar teste seje o que deus quiser")
                            # Move the drone forward and backward.
                            # Note that it will be in front of original position due to inertia.
                            print("Move forward")
                            set_attitude(pitch_angle = -5, thrust = 0.5, duration = 2)

                            set_attitude(duration = 1)


                            print("Move backward")
                            set_attitude(pitch_angle = 5, thrust = 0.5, duration = 4)

                            set_attitude(duration = 1)

                            print("Move foreward")
                            set_attitude(pitch_angle = -5, thrust = 0.5, duration = 2)


                            set_attitude(duration = 1)

                            #vehicle.mode = VehicleMode("BRAKE")

                            print("Setting LAND mode...")
                            vehicle.mode = VehicleMode("LAND")
                            print "Close vehicle object"
                            vehicle.close()
                        except Exception as e:
                            print e
                        break
                
        else:
                if(vehicle.mode.name=='GUIDED'):
                        vehicle.mode = VehicleMode("ALT_HOLD")

        time.sleep(0.5)

print("Completed")
