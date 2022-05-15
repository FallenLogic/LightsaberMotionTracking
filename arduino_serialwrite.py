# importing the libraries
import time

import cv2
import imutils
import numpy as np
import serial
from cv2 import flip, blur

# Setup
cap = cv2.VideoCapture(0)

lower = np.array([20, 90, 90])
upper = np.array([60, 255, 255])

Arduino_Serial = serial.Serial('com3', 9600)

while True:
    # Capture frame-by-frame
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

        if radius > 100:
            print(Arduino_Serial.write(bytes('1', 'utf-8')))
            time.sleep(1)
            Arduino_Serial.write(0)

    if cv2.waitKey(1) & 0xFF == 27:
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
