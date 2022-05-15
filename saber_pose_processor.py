import math
import sys
import cv2
import imutils
import mediapipe as mp
import time

import numpy as np
from cv2 import flip, blur

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
mp_holistic = mp.solutions.holistic

# For webcam input:
cap = cv2.VideoCapture(0)

prevTime = 0
ksize = (10, 10)

# ornj
lower = np.array([20, 90, 90])
upper = np.array([60, 255, 255])

center = (0, 0)

with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # Convert the BGR image to RGB.
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = flip(image, 1)

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = pose.process(image)

        # Draw the pose annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
        currTime = time.time()
        fps = 1 / (currTime - prevTime)
        prevTime = currTime
        cv2.putText(image, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        frame = blur(image, ksize)

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)
        # mask = flip(mask, 1)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        width = image.shape[0]
        height = image.shape[1]

        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            if M["m00"] != 0:
                center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # Prints coordinates
            # print('xy coords: {0}'.format(center), 'radius {0}'.format(radius))
            # nightmare nightmare nightmare nightmare
            # mouse.position = center
            cv2.putText(image, 'Saber position: ' + str(center), (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 255, 255), 2)
            cv2.putText(image, '+', center, cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255, 255, 255), 2)

        if results.pose_landmarks is not None:

            wrist_bone = results.pose_landmarks.landmark[15]

            print("x: {0}".format(image.shape[1]))
            print("y: {0}".format(image.shape[0]))

            x1 = int(wrist_bone.x * image.shape[1])
            y1 = int(wrist_bone.y * image.shape[0])

            x2 = int(center[0])
            y2 = int(center[1])

            # misnomer because x3 is for the Z-axis, normalized against the depth of the image
            # y3 is just y1 because the height of the landmark doesn't change
            x3 = int(wrist_bone.z*depth)
            y3 = y1

            sys.stdout.write("Wrist x {0} y {0} \n".format(wrist_bone.x * width,
                                                           wrist_bone.y * height))
            sys.stdout.write("Saber center x {0} y {0}\n".format(center[0], center[1]))
            cv2.line(image, (x1, y1), (x2, y2), (255, 140, 0), 2)

            # the next loc isn't strictly necessary, it just displays a line on screen that
            # helps intuitively show the angle
            cv2.line(image, (x1, y1), (image.shape[0], y1), (100, 100, 100, 100), 2)

            if x2-x1 != 0:
                theta_xy = -1*int(math.atan((y1 - y2) / (x2 - x1)) * 180 / math.pi)
                theta_xz = -1*int(math.atan((y1 - y2) / (x2 - x1)) * 180 / math.pi)
            sys.stdout.write(" (LR) XY Angle: " + str(theta_xy) + "\n")
            sys.stdout.write(" (FB) XZ Angle: " + str(z1) + "\n")
        cv2.imshow('Player pose & saber transforms', image)

        # The ESC key
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()
