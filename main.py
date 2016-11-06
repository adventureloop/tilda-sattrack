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

def render(data):
    print("drawing")

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

def drawtext(con, status="searching for long range comms..."):
    con.clear()
    con.set_default_font(ugfx.FONT_NAME)
    con.text(0, 5, "SATTRACKER", ugfx.GREEN)

    con.set_default_font(ugfx.FONT_SMALL)
    con.text(0, 50, status, ugfx.GREEN)

#
#  ___ ___ _ ___ _____ ___
# (_-</ -_) '_\ V / _ (_-<
# /__/\___|_|  \_/\___/__/
#
#
# json:
servoconfig = """
{
    "el_servo":
    [
        {
            "pin":"1",
            "limits":
            [
                "0",
                "180"
            ]
        }
    ]
    "az_servo":
    [
        {
            "pin":"2",
            "limits":
            [
                "0",
                "180"
            ]
        }
        {
            "pin":"4",
            "limits":
            [
                "0",
                "180"
            ]
        }
    ]
}
"""


def calibrateservos():
    print("I am a servo")

#           _               _           
#  ___ __ _| |_ _ _ __ _ __| |_____ _ _ 
# (_-</ _` |  _| '_/ _` / _| / / -_) '_|
# /__/\__,_|\__|_| \__,_\__|_\_\___|_|  
#
#
def sattracker():
    print("following a satellite")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.settimeout(0.5)   #socket will block for most 0.5 seconds
    s.bind((ANY_ADDR, PORT))
    s.listen(1)
    while True:
        sleep(0.1)           #screen will update at most 10Hz

        conn, addr = s.accept()
        print 'Connection from:', addr

        while connected:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break

            print("received data:", data)

            if data == "p\n":
                print("pos query when at az:{} el: {}", current_az, current_el);

                response = "{}\n{}\n".format(az, el)
                print("responing with: \n {}".format(response))
                conn.send(response)
            elif data.startswith("P "):
                values = data.split("  ")
                print(values)
                target_az = float(values[1])
                target_el = float(values[2])

                print("moving to az:{} el: {}".format(target_az, target_el));

                conn.send(" ")
            elif data == "q\n":
                print("close command, shutting down")
                conn.close()
                break
            else:
                print("unknown command, closing socket")
                conn.close()
                break

#if __name__ == "__main__":
print("starting")

buttons.init()
ugfx.init()
ugfx.clear(ugfx.BLACK)

textcontainer = ugfx.Container(0, 0, 320, 80)
container = ugfx.Container(0, 80,320,160)

drawtext(textcontainer)
wifi.connect()

sattracker()
