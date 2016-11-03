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

def drawtext(con):
    con.clear()
    con.set_default_font(ugfx.FONT_NAME)
    con.text(0, 5, "SATTRACKER", ugfx.GREEN)
    
def sattracker():

    print("following a satellite")
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((TCP_IP, TCP_PORT))
        s.listen(1)

        conn, addr = s.accept()
        print 'Connection address:', addr

        data = conn.recv(BUFFER_SIZE)
        if not data:
            break

        print("received data:", data)

        if data == "p\n":
            print("pos query at az:{} el: {}", az, el);

            response = "{}\n{}\n".format(az, el)
            print("responing with: \n {}".format(response))
            conn.send(response)
        elif data.startswith("P "):
            values = data.split("  ")
            print(values)
            az = float(values[1])
            el = float(values[2])

            print("moving to az:{} el: {}".format( az, el));

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
