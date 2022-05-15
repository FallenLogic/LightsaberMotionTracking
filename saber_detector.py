import cv2
import imutils
import numpy as np
from pynput.mouse import Button, Controller

# This is so we can send input
mouse = Controller()

from cv2 import flip, blur

cap = cv2.VideoCapture(0)

lower = np.array([20, 90, 90])
upper = np.array([60, 255, 255])

while True:
    # Capture frame-by-frame from video camera (webcam in my case)
    ret, frame = cap.read()

    ksize = (10, 10)

    frame = blur(frame, ksize)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)

    frame = flip(frame, 1)
    mask = flip(mask, 1)

    cv2.imshow('Tracking input', frame)
    cv2.imshow('Tracking mask', mask)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        if M["m00"] != 0:
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # Adjusts mouse coordinates
        print('xy coords: {0}'.format(center), 'radius {0}'.format(radius))
        if center[0] > 500:
            mouse.position = mouse.position[0] + 1, mouse.position[1]
        elif center[0] < 460:
            mouse.position = mouse.position[0] - 1, mouse.position[1]
        else:
            mouse.position = mouse.position

        # This moves the mouse up and down - adjust at your own risk
        # if center[1] > 380:
        #     mouse.position = mouse.position[0], mouse.position[1]+1
        # elif center[1] < 360:
        #     mouse.position = mouse.position[0], mouse.position[1]-1
        # else:
        #     mouse.position = mouse.position

        # only proceed if the radius meets a minimum size
        if radius > 250:
            mouse.press(Button.left)
            mouse.release(Button.left)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
