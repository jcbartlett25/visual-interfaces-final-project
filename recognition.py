################################
# Joshua Bartlett
# jcb2254
# Visual Interfaces to Computers
################################

import cv2                              
import numpy as np
import math
from collections import deque

class GestureRecognizer(object):

    def __init__(self):
        self.camera = None
        self.circular_buffer_x = deque([1,2,3,4,5,6,7,8,9,10])
        self.circular_buffer_y = deque([1,2,3,4,5,6,7,8,9,10])
        self.circular_buffer_gesture = deque([1,2,3,4,5,6])

    def set_up(self):
        self.camera = cv2.VideoCapture(0)
        self.camera.set(3,640)
        self.camera.set(4,480)
        self.circular_buffer_x = deque([1,2,3,4,5,6,7,8,9,10])
        self.circular_buffer_y = deque([1,2,3,4,5,6,7,8,9,10])
        self.circular_buffer_gesture = deque([1,2,3,4,5,6])

    def read_motion(self, x_variance, y_variance, cnt):

        # If x variance is high and y is relatively low, then we know we are moving left and right
        if x_variance > 400 and y_variance < 200:
            return 'left and right'

        # If y variance is high and x is low, then we are moving up and down
        elif y_variance > 800 and x_variance < 200:
            return 'up and down'

        # If both are low, then we are relatively still and will analyze if it is a fist
        elif x_variance < 100 and y_variance < 100:
            return self.check_for_fist(cnt)

        # Notable motion in both directions, not relevant
        else:
            return 'unknown'


    def check_for_fist(self, cnt):

        # Get the area of the contour
        cnt_area = cv2.contourArea(cnt)

        # Get the radius of the minimum circle
        _, radius = cv2.minEnclosingCircle(cnt)

        # Calculate area of circle using radius
        circle_area = (radius**2)*3.14
        
        # If the area of the circle is similar to that of the contour
        # then we can assume that the gesture is not that of a splayed hand
        # and more circular aka like a fist
        if(circle_area * .55 < cnt_area):
            return "fist"

        return "notfist"


    def wait_for_fist(self):

        self.set_up()
        ready_to_return = False

        while not ready_to_return:

            # Capture frame from camera
            ret, frame = self.camera.read()
            
            frame=cv2.bilateralFilter(frame,5,50,100)

            # Flip frame to feel more natural to user
            frame=cv2.flip(frame,1)

            # Convert RGB image into grayscale
            frame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Gaussian blur removes noise from the image
            frame = cv2.GaussianBlur(frame, (5,5), 0)

            # Apply a threshold to filter out all pixels below a certain value
            _, thresh = cv2.threshold(frame, 90, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

            # Crop the image so we only look at a certain region where we exprect the hand to be
            crop_img = thresh[10:240, 320:630]

            # Draw frame around where the image will be cropped
            cv2.rectangle(frame,(320,10),(630,240),(0,255,0),2)

            # Find the contours in the cropped image
            contours, hierarchy = cv2.findContours(crop_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            if contours:

                # Get the largest contour and its hull
                cnt = max(contours, key=lambda countour: cv2.contourArea(countour))
                hull = cv2.convexHull(cnt)

                # Draw the hull and contour on the cropped image
                cv2.drawContours(crop_img, [cnt], 0, (125,255,10), 5)
                cv2.drawContours(crop_img, [hull], 0, (125,255,10), 5)

                # Compute the center of the contour
                M = cv2.moments(cnt)

                try:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    contour_center = (cx, cy)

                    # Pop out the oldest contouor location in each queue
                    self.circular_buffer_x.popleft()
                    self.circular_buffer_y.popleft()
                    self.circular_buffer_gesture.popleft()

                    # Add the newest location in each queue
                    self.circular_buffer_x.append(contour_center[0])
                    self.circular_buffer_y.append(contour_center[1])

                    # Calculate the variance in each direction
                    x_variance = np.var(self.circular_buffer_x)
                    y_variance = np.var(self.circular_buffer_y)

                    result = self.read_motion(x_variance, y_variance, cnt)
                    self.circular_buffer_gesture.append(result)
                    #print(result)

                    # If we have seen the same detected gesture enough times in a row, then we are done
                    if self.circular_buffer_gesture.count(self.circular_buffer_gesture[0]) == len(self.circular_buffer_gesture):

                        if self.circular_buffer_gesture[0] == "fist":
                            ready_to_return = True

                # Sometimes one of the points is 0, which causes an error
                except ZeroDivisionError:
                    print('cmon man')

            # Display the images
            crop_img = cv2.resize(crop_img, (480, 360))
            frame = cv2.resize(frame, (480, 360))
            horizontal = np.concatenate((frame, crop_img), axis=1)
            cv2.imshow('gesture', horizontal)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


        # When everything done, release the capture
        self.camera.release()
        cv2.destroyAllWindows()
        return True

    def look_for_gesture(self):
        
        self.set_up()
        ready_to_return = False

        while not ready_to_return:

            # Capture frame from camera
            ret, frame = self.camera.read()
            
            frame=cv2.bilateralFilter(frame,5,50,100)

            # Flip frame to feel more natural to user
            frame=cv2.flip(frame,1)

            # Convert RGB image into grayscale
            frame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Gaussian blur removes noise from the image
            frame = cv2.GaussianBlur(frame, (5,5), 0)

            # Apply a threshold to filter out all pixels below a certain value
            _, thresh = cv2.threshold(frame, 90, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

            # Crop the image so we only look at a certain region where we exprect the hand to be
            crop_img = thresh[10:240, 320:630]

            # Draw frame around where the image will be cropped
            cv2.rectangle(frame,(320,10),(630,240),(0,255,0),2)

            # Find the contours in the cropped image
            contours, hierarchy = cv2.findContours(crop_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            if contours:

                # Get the largest contour and its hull
                cnt = max(contours, key=lambda countour: cv2.contourArea(countour))
                hull = cv2.convexHull(cnt)

                # Draw the hull and contour on the cropped image
                cv2.drawContours(crop_img, [cnt], 0, (125,255,10), 5)
                cv2.drawContours(crop_img, [hull], 0, (125,255,10), 5)

                # Compute the center of the contour
                M = cv2.moments(cnt)

                try:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    contour_center = (cx, cy)

                    # Pop out the oldest contouor location in each queue
                    self.circular_buffer_x.popleft()
                    self.circular_buffer_y.popleft()
                    self.circular_buffer_gesture.popleft()

                    # Add the newest location in each queue
                    self.circular_buffer_x.append(contour_center[0])
                    self.circular_buffer_y.append(contour_center[1])

                    # Calculate the variance in each direction
                    x_variance = np.var(self.circular_buffer_x)
                    y_variance = np.var(self.circular_buffer_y)

                    result = self.read_motion(x_variance, y_variance, cnt)
                    self.circular_buffer_gesture.append(result)
                    print(result)

                    # If we have seen the same detected gesture enough times in a row, then we are done
                    if self.circular_buffer_gesture.count(self.circular_buffer_gesture[0]) == len(self.circular_buffer_gesture):

                        if self.circular_buffer_gesture[0] != 'notfist' and self.circular_buffer_gesture[0] != 'unknown':
                            ready_to_return = True

                # Sometimes one of the points is 0, which causes an error
                except ZeroDivisionError:
                    print('cmon man')

            # Display the images
            crop_img = cv2.resize(crop_img, (480, 360))
            frame = cv2.resize(frame, (480, 360))
            horizontal = np.concatenate((frame, crop_img), axis=1)
            cv2.imshow('gesture', horizontal)

            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


        # When everything done, release the capture
        self.camera.release()
        cv2.destroyAllWindows()
        return self.circular_buffer_gesture[0]

