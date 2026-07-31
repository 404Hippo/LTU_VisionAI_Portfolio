#!/usr/bin/env python3
"""
PICAR-X Vision Lab - Student Starter Code
=============================================
Two missions today:

  MISSION 1 - FACE TRACKING (camera only)
    Make the camera turn to keep a detected face centered in view.

  MISSION 2 - COLOR FOLLOW (camera + car driving)
    Make the camera AND the car body follow a colored object around.

Everything below is already working for you: the camera, the live
video feed, and the detection system that finds faces/colors. Your
job is to fill in the two functions marked "TODO" - that's where the
car's actual "thinking" happens.

HOW TO WATCH THE LIVE CAMERA FEED WHILE TESTING:
  Open a web browser and go to:  http://<the-pi's-ip-address>:9000/mjpg

SYMBOL KEY:
  ( )   parentheses - go after a function name, hold its "inputs"
  [ ]   brackets    - used to look something up by name
  :     colon       - goes at the end of an if/def/while line
  +=    "add this amount to the variable" (two keyboard keys, + then =)
  -=    "subtract this amount from the variable"
  >     "is greater than"   (Shift + period)
  <     "is less than"      (Shift + comma)
"""

from picarx import Picarx
from vilib import Vilib
from time import sleep

px = Picarx()

# ======================================================================
# EVERYTHING BELOW THIS LINE IS ALREADY SET UP - YOU DON'T NEED TO EDIT IT
# ======================================================================

# ---------- Camera and display setup ----------

Vilib.camera_start(vflip=False, hflip=False)
Vilib.display(local=False, web=True)
Vilib.face_detect_switch(True)
sleep(2)  # give the camera time to fully start


# ---------- Helper functions ----------

def clamp_number(number, low, high):
    """
    Keeps a number from going outside a safe range.
    Example: clamp_number(50, -35, 35) returns 35, because 50 is
    too big and gets "clamped" down to the maximum allowed (35).
    You'll use this to keep servo angles safe.
    """
    if number < low:
        return low
    if number > high:
        return high
    return number

def get_face_position():
    """
    Returns (found, x, y) for the face the camera currently sees.
    found = True or False, depending on whether a face is visible.
    x = left-right position of the face (0 to 320, 160 = center)
    y = up-down position of the face (0 to 240, 120 = center)
    If no face is found, x and y will be None.
    """
    if Vilib.detect_obj_parameter['human_n'] > 0:
        x = Vilib.detect_obj_parameter['human_x']
        y = Vilib.detect_obj_parameter['human_y']
        return (True, x, y)
    return (False, None, None)

def set_color_target(color_name):
    """
    Tell the camera which color to look for.
    color_name must be one of:
      'red', 'orange', 'yellow', 'green', 'blue', 'purple'
    Call this once before using get_color_position().
    """
    Vilib.color_detect(color_name)

def get_color_position():
    """
    Returns (found, x, y) for the color you set with set_color_target().
    Same coordinate system as get_face_position() above.
    """
    if Vilib.detect_obj_parameter['color_n'] > 0:
        x = Vilib.detect_obj_parameter['color_x']
        y = Vilib.detect_obj_parameter['color_y']
        return (True, x, y)
    return (False, None, None)

def move_camera(pan_angle, tilt_angle):
    """
    Points the camera to a specific pan (left-right) and tilt
    (up-down) angle. Both should be between -35 and 35.
    """
    px.set_cam_pan_angle(pan_angle)
    px.set_cam_tilt_angle(tilt_angle)

def drive_toward(steering_angle, speed):
    """
    Steers the car's wheels to steering_angle (-35 to 35) and drives
    forward at the given speed (0-100).
    """
    px.set_dir_servo_angle(steering_angle)
    px.forward(speed)

def stop_car():
    """Stops the car's wheels (camera can still move)."""
    px.stop()


# ======================================================================
# MISSION 1: FACE TRACKING - fill in track_face() below
# ======================================================================
#
# GOAL: every time this function runs, check where the face is, and
# adjust the camera's pan/tilt angle a LITTLE bit closer to centering
# it - not all at once, just a small nudge each time. Over many loops
# (this runs about 20 times per second), the camera will smoothly
# glide toward centering the face.
#
# HINTS:
#   - The image is 320 pixels wide. Center is x = 160.
#     If the face's x is LESS than 160, it's on the LEFT side.
#     If the face's x is MORE than 160, it's on the RIGHT side.
#   - The image is 240 pixels tall. Center is y = 120.
#   - You have two variables already set up for you below (pan_angle
#     and tilt_angle) that persist between loops - use += or -= to
#     nudge them, then call move_camera(pan_angle, tilt_angle).
#   - Don't forget to use clamp_number() so the angle never goes past
#     -35 or 35.

pan_angle = 0
tilt_angle = 0

def track_face():
    global pan_angle, tilt_angle

    found, x, y = get_face_position()

    if found:
        print("Face at x =", x, " y =", y)

        # TODO: adjust pan_angle based on x
        # (hint: if x is less than 160, the face is left, so you
        #  probably want pan_angle to decrease a little)
        
        pan_angle += (x * 10 / 320) - 5

        # TODO: adjust tilt_angle based on y

        tilt_angle -= (y * 10 / 240) - 5

        # TODO: clamp both angles to a safe range using clamp_number()

        pan_angle = clamp_number(pan_angle, -35, 35)
        tilt_angle = clamp_number(tilt_angle, -35, 35)

        # TODO: call move_camera() with your new angles

        move_camera(pan_angle, tilt_angle)

    else:
        print("No face seen")


# ======================================================================
# MISSION 2: COLOR FOLLOW - fill in follow_color() below
# ======================================================================
#
# GOAL: pick a color (already set below), then make the CAR (not just
# the camera) drive toward it, steering to keep it roughly centered.
#
# HINTS:
#   - Same 320-wide, 240-tall coordinate system as Mission 1.
#   - You'll need to decide: if the color is on the left, which way
#     should the wheels turn? What steering_angle number represents
#     "turn left" vs "turn right"? (Look at drive_toward() above -
#     it takes a steering_angle from -35 to 35.)
#   - Keep your driving speed slow and safe - try somewhere around
#     15-25.
#   - If no color is found, make sure the car stops! (use stop_car())

set_color_target('red')  # change this to whatever color you want to chase
steering_angle = 0

def follow_color():
    found, x, y = get_color_position()

    if found:
        print("Color at x =", x, " y =", y)

        # TODO: figure out a steering_angle based on x
        # (hint: how far is x from 160, the center? that difference
        #  tells you both which way to turn AND roughly how much)

        if x < 160:
            steering_angle = -((160 - x) / 160) * 35  # turn left
        elif x > 160:
            steering_angle = ((x - 160) / 160) * 35  # turn right
        else:
            steering_angle = 0  # centered
        

        # TODO: call drive_toward() with your steering_angle and a
        # safe speed

        steering_angle = clamp_number(steering_angle, -35, 35)  # ensure steering angle is safe

        drive_toward(steering_angle, 20)  # safe speed of 20

        pass  # delete this line once you've written your code
    else:
        print("No color seen")
        stop_car()


pan_angle = 0
tilt_angle = 0
steering_angle = 0

def track_and_follow_face():
    global pan_angle, tilt_angle, steering_angle

    found, x, y = get_face_position()

    if found:
        print("Face at x =", x, " y =", y)

        pan_angle += (x * 10 / 320) - 5
        pan_angle = clamp_number(pan_angle, -35, 35)

        tilt_angle -= (y * 10 / 240) - 5
        tilt_angle = clamp_number(tilt_angle, -35, 35)

        move_camera(pan_angle, tilt_angle)

        steering_angle += (x * 10 / 320) - 5
        steering_angle = clamp_number(steering_angle, -35, 35)

        drive_toward(steering_angle, 20)
    else:
        print("No face seen")
        stop_car()

# ======================================================================
# CHOOSE WHICH MISSION TO RUN
# ======================================================================
# Change this to "face" or "color" depending on which one you're
# testing right now.

MISSION = "facefollow"


# ---------- Main loop (do not edit) ----------

if __name__ == "__main__":
    try:
        while True:
            if MISSION == "face":
                track_face()
            elif MISSION == "color":
                follow_color()
            elif MISSION == "facefollow":
                track_and_follow_face()
            sleep(0.05)
    except KeyboardInterrupt:
        pass
    finally:
        stop_car()
        px.set_dir_servo_angle(0)
        px.set_cam_pan_angle(0)
        px.set_cam_tilt_angle(0)
        print("Stopped safely.")
