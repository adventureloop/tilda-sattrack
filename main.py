### Author: tj <tj@enoti.me>
### Description: Scottish Consulate Techno Orbital Tracker
### Category: Other
### License: BSD 3

import sys
import os
import time
import socket
import ugfx
import buttons
import wifi

PORT = 4533
ANY_ADDR = "0.0.0.0"

container = None
textcontainer = None

target_az = 0.0
target_el = 0.0

current_az = 0.0
current_el = 0.0

az = None
el = None

def processbuttons(data):
    #buttons.is_pressed("JOY_RIGHT"):
    #buttons.is_pressed("JOY_LEFT"):
    #buttons.is_pressed("JOY_DOWN"):
    #buttons.is_pressed("JOY_UP"):
    #buttons.is_pressed("JOY_CENTER"):
    #buttons.is_pressed("BTN_A"):
    #buttons.is_pressed("BTN_B"):
    #buttons.is_pressed("BTN_MENU"):

    print("readings buttons")

def drawtext(status="Searching for long range comms..."):
    global current_az
    global current_el

    ugfx.clear(ugfx.BLACK)
    ugfx.set_default_font(ugfx.FONT_NAME)
    ugfx.text(0, 5, "SATTRACKER", ugfx.GREEN)

    ugfx.set_default_font(ugfx.FONT_SMALL)
    ugfx.text(0, 50, status, ugfx.RED)


    posstring = "AZ: {} EL: {}".format(current_az, current_el)
    ugfx.set_default_font(ugfx.FONT_SMALL)
    ugfx.text(0, 70, posstring, ugfx.YELLOW)

#
#  ___ ___ _ ___ _____ ___
# (_-</ -_) '_\ V / _ (_-<
# /__/\___|_|  \_/\___/__/
#
#
def calibrateservos():

    global az
    global el

    az = pyb.Servo(1)
    el = pyb.Servo(2)

    az.angle(0)
    el.angle(0)

#           _               _           
#  ___ __ _| |_ _ _ __ _ __| |_____ _ _ 
# (_-</ _` |  _| '_/ _` / _| / / -_) '_|
# /__/\__,_|\__|_| \__,_\__|_\_\___|_|  
#
#
def sattracker():

    global current_az
    global current_el

    global target_az
    global target_el 

    calibrateservos()
    
    print("following a satellite")

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((ANY_ADDR, PORT))
    s.listen(1)
    s.settimeout(0.5)   #socket will block for most 0.5 seconds

    connected = False

    while True:
        #time.sleep(0.1)           #screen will update at most 10Hz

        status = "waiting for connection"
        conn, addr = s.accept()
        if conn:
            status = 'Connection from {}:{}'.format(addr[0], addr[1])
            drawtext(status)
            connected = True
        else:
            continue

        while connected:
            data = conn.recv(100).decode("utf-8") #timeouts here aren't handled

            if not data:
                break

            if data == "p\n":
                response = "{}\n{}\n".format(current_az, current_el)
                conn.send(response)
            elif data.startswith("P "):
                values = data.split("  ")
                if len(values) != 3:
                    continue

                target_az = float(values[1])
                target_el = float(values[2])
                conn.send(" ")

                az.angle(target_az)
                el.angle(target_el)

                current_az = target_az
                current_el = target_el

                drawtext(status)
            elif data == "q\n":
                print("close command, shutting down")
                conn.close()
                connected = False
                break
            else:
                print("unknown command, closing socket")
                conn.close()
                connected = False
                break

#if __name__ == "__main__":
print("starting")

buttons.init()
ugfx.init()
ugfx.clear(ugfx.BLACK)

textcontainer = ugfx.Container(0, 0, 320, 80)
container = ugfx.Container(0, 80,320,160)

drawtext()
wifi.connect()

sattracker()
