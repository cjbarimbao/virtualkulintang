import cv2
import numpy as np
import time
import sys
import logging
# import pygame     # for mixing sound

"""
reference code

Title: AirDrums source code
Author: Tolentino, Uy, Naval
Date: 2019
"""

class vkulintang(object):
    def __init__(self):
        # Frame details
        self.frame_width_default = 854
        self.frame_height_default = 480
        self.frame_width = 854
        self.frame_height = 480
        self.pixel_width = 854
        self.pixel_height = 480
        self.grid_x1 = 0
        self.grid_x2 = 0
        self.grid_y1 = 0
        self.grid_y2 = 0
        self.grid_color = (0, 255, 0)

        """
        comments on the frame size:
        adjusted to fit the 8 kulintang gongs

        """

        # Kalman Filter
        self.kalman = cv2.KalmanFilter(4,2)
        self.kalman.measurementMatrix = np.array([[1,0,0,0], 
                                                  [0,1,0,0]],np.float32)
        self.kalman.transitionMatrix = np.array([[1,0,1,0],
                                                 [0,1,0,1],
                                                 [0,0,1,0],
                                                 [0,0,0,1]],np.float32)
        self.kalman.processNoiseCov = np.array([[1,0,0,0],
                                                [0,1,0,0],
                                                [0,0,1,0],
                                                [0,0,0,1]],np.float32) * 0.03
        self.measurement = [[0,0], [0,0], [0,0]]
        self.prediction = [[0,0], [0,0], [0,0]]

        # Patch sizes - Get 10x10 patch from center
        self.patch_size = 10
        self.patch_total_size = self.patch_size*self.patch_size

        # RGB Calibration
        self.CALIBRATED = False

        # Left, right
        self.CALIBRATIONS = [0, 0, 0]
        self.NUM_ITEMS = 2 # number of things to calibrate, 2 or 3

        self.blob_colors = [0, 0, 0]
        self.min_rgb = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        self.max_rgb = np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]])

        # Points detected
        self.prev_pt_2 = np.array([[0, 0], [0, 0], [0, 0]])
        self.prev_pt = np.array([[0, 0], [0, 0], [0, 0]])
        self.new_pt = np.array([[0, 0], [0, 0], [0, 0]])
        self.INIT_ITEM = [0,0, 0]

        # Velocities and accelerations
        self.velocities = [0, 0, 0]
        self.prev_velocities = [0, 0, 0]
        self.accelerations = [0, 0, 0]
        self.dir_vertical = [0, 0, 0]
        self.dir_horizontal = [0, 0, 0]

        # Flag for detection
        self.flags = [0, 0, 0]

        # Init of camera
        self.cam = None

        # FPS
        self.FPS = 0

        # DELTA_T = 1/FPS
        self.DELTA_T = 0

        # Markers
        self.MARKER_ITEMS = ["Left", "Right"]

        # Bounding area coordinates - upper left, lower right coordinates in [x,y]
        self.gong_1 = np.array([[0, 0], [0, 0], [0, 0]])
        self.gong_2 = np.array([[0, 0], [0, 0], [0, 0]])
        self.gong_3 = np.array([[0, 0], [0, 0], [0, 0]])
        self.gong_4 = np.array([[0, 0], [0, 0], [0, 0]])
        self.gong_5 = np.array([[0, 0], [0, 0], [0, 0]])
        self.gong_6 = np.array([[0, 0], [0, 0], [0, 0]])
        self.gong_7 = np.array([[0, 0], [0, 0], [0, 0]])
        self.gong_8 = np.array([[0, 0], [0, 0], [0, 0]])

        self.gong_color_draw = (0, 255, 0)
        self.text_color = (255, 255, 255)
        self.gong_color_strike = (0, 0, 255)

        """ self.coord_crash = np.array([[0, 0], [0, 0], [0, 0]])
        self.coord_hihat = np.array([[0, 0], [0, 0], [0, 0]])
        self.coord_snare = np.array([[0, 0], [0, 0], [0, 0]])

        self.coord_tom1 = np.array([[0, 0], [0, 0], [0, 0]])
        self.coord_bass = np.array([[0, 0], [0, 0], [0, 0]])

        self.coord_ride = np.array([[0, 0], [0, 0], [0, 0]])
        self.coord_tom2 = np.array([[0, 0], [0, 0], [0, 0]])
        self.coord_floor = np.array([[0, 0], [0, 0], [0, 0]])

        self.drum_color_1 =  (0, 255, 0)
        self.drum_color_2 = (255, 0, 0) """


    def cb_calibrate(self, event, x, y, flags, params):
        """ Mouse callback for initial calibration of points """
        img = params[0]
        item_num = params[1]
        descriptor = []

        if event == cv2.EVENT_LBUTTONDOWN:
            point = (x, y)
            line = "[x,y]: {},{} (rgb): ({})".format(point[0], point[1], img[y, x])

            step_size = int(self.patch_size/2)
            height, width = img.shape[:2]

            # Turn into rows, cols format
            top_left = (point[1] - step_size, point[0] - step_size) 
            bottom_right = (point[1] + step_size, point[0] + step_size)

            # Check for top_left for out of bounds
            if (top_left[0] >= height) or (top_left[0] < 0) or (top_left[1] >= width) or (top_left[1] < 0):
                return
            if (bottom_right[0] >= height) or (bottom_right[0] < 0) or (bottom_right[1] >= width) or (bottom_right[1] < 0):
                return

            # Get descriptor, going through rows
            for m in range(top_left[0], bottom_right[0] + 1):
                # Going through columns
                for n in range(top_left[1], bottom_right[1] + 1):
                    descriptor.append(img[m, n])
            descriptor = np.array(descriptor)

            self.min_rgb[item_num, 0] = np.min(descriptor[:,0][self.patch_size:self.patch_total_size-self.patch_size])
            self.max_rgb[item_num, 0] = np.max(descriptor[:,0][self.patch_size:self.patch_total_size-self.patch_size])
            self.min_rgb[item_num, 1] = np.min(descriptor[:,1][self.patch_size:self.patch_total_size-self.patch_size])
            self.max_rgb[item_num, 1] = np.max(descriptor[:,1][self.patch_size:self.patch_total_size-self.patch_size])
            self.min_rgb[item_num, 2] = np.min(descriptor[:,2][self.patch_size:self.patch_total_size-self.patch_size])
            self.max_rgb[item_num, 2] = np.max(descriptor[:,2][self.patch_size:self.patch_total_size-self.patch_size])

            self.CALIBRATED = True


    def init_calibrate(self, num_items):
        """ Intialize calibrations """
        self.NUM_ITEMS = num_items

        self.frame_calibration()
        self.color_calibration()


    def frame_calibration(self):
        """ Calculate initial FPS """
        self.cam = cv2.VideoCapture(0)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH,self.frame_width_default)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT,self.frame_height_default)

        # Calculate FPS
        num_frames = 30
        start = time.time()
        for i in range(num_frames):
            ret, frame = self.cam.read()
        end = time.time()
        seconds = end - start
        self.FPS = 30
        #self.FPS = num_frames / seconds
        self.DELTA_T = 1/self.FPS

        """ Initialize drum area bounding box coordinates """
        self.frame_width = int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))

        self.grid_y1 = int(0.71875*self.frame_height)    # upper y of bound
        self.grid_y2 = int(self.frame_height)           # lower y of bound
        # self.bound_width = 135
        self.bound_width = 0.125                        # x is 12.5% of width

        self.gong_1[0,:] = [0, self.grid_y1]                                                            # (0, upper y)
        self.gong_1[1,:] = [int(self.bound_width*self.pixel_width), self.grid_y2]    #                   (135, lower y)
        self.gong_1[2,:] = [((self.gong_1[0,0] + self.gong_1[1,0])/2) - 25, self.gong_1[0,1] + 25]      # label coordinates

        self.gong_2[0,:] = [int(self.bound_width*self.pixel_width), self.grid_y1]                       # (135, upper y)
        self.gong_2[1,:] = [int(2*self.bound_width*self.pixel_width), self.grid_y2]                     # (270, lower y)
        self.gong_2[2,:] = [((self.gong_2[0,0] + self.gong_2[1,0])/2) - 25, self.gong_2[0,1] + 25]

        self.gong_3[0,:] = [int(2*self.bound_width*self.pixel_width), self.grid_y1]                     # (270, upper y)
        self.gong_3[1,:] = [int(3*self.bound_width*self.pixel_width), self.grid_y2]                     # (405, lower y)
        self.gong_3[2,:] = [((self.gong_3[0,0] + self.gong_3[1,0])/2) - 25, self.gong_3[0,1] + 25]

        self.gong_4[0,:] = [int(3*self.bound_width*self.pixel_width), self.grid_y1]                     # (405, upper y)
        self.gong_4[1,:] = [int(4*self.bound_width*self.pixel_width), self.grid_y2]                     # (540, lower y)
        self.gong_4[2,:] = [((self.gong_4[0,0] + self.gong_4[1,0])/2) - 25, self.gong_4[0,1] + 25]

        self.gong_5[0,:] = [int(4*self.bound_width*self.pixel_width), self.grid_y1]                     # (540, upper y)
        self.gong_5[1,:] = [int(5*self.bound_width*self.pixel_width), self.grid_y2]                     # (675, lower y)
        self.gong_5[2,:] = [((self.gong_5[0,0] + self.gong_5[1,0])/2) - 25, self.gong_5[0,1] + 25]

        self.gong_6[0,:] = [int(5*self.bound_width*self.pixel_width), self.grid_y1]                     # (675, upper y)
        self.gong_6[1,:] = [int(6*self.bound_width*self.pixel_width), self.grid_y2]                     # (810, lower y)
        self.gong_6[2,:] = [((self.gong_6[0,0] + self.gong_6[1,0])/2) - 25, self.gong_6[0,1] + 25]

        self.gong_7[0,:] = [int(6*self.bound_width*self.pixel_width), self.grid_y1]                     # (810, upper y)
        self.gong_7[1,:] = [int(7*self.bound_width*self.pixel_width), self.grid_y2]                     # (945, lower y)
        self.gong_7[2,:] = [((self.gong_7[0,0] + self.gong_7[1,0])/2) - 25, self.gong_7[0,1] + 25]

        self.gong_8[0,:] = [int(7*self.bound_width*self.pixel_width), self.grid_y1]                     # (945, upper y)
        self.gong_8[1,:] = [int(8*self.bound_width*self.pixel_width), self.grid_y2]                     # (1080, lower y)
        self.gong_8[2,:] = [((self.gong_8[0,0] + self.gong_8[1,0])/2) - 25, self.gong_8[0,1] + 25]

    def color_calibration(self):
        """ Computes color calibrations for the left and right markers """
        for i in range(self.NUM_ITEMS):
            item = self.MARKER_ITEMS[i]

            while True:
                ret_val, img = self.cam.read()
                img = cv2.flip(img, 1)

                # For calibration
                title = "Calibrate Picture: {}".format(item)
                cv2.namedWindow(title, cv2.WINDOW_NORMAL)
                cv2.resizeWindow(title, self.frame_width,self.frame_height)

                #set mouse callback function for window
                cv2.setMouseCallback(title, self.cb_calibrate, [img, i])
                cv2.imshow(title, img)


                if self.CALIBRATED == True:
                    break
                if cv2.waitKey(1) == 27: 
                    sys.exit()
                    #break  # esc to quit
            cv2.destroyAllWindows()
            self.CALIBRATED = False
            self.CALIBRATIONS[i] = 1

            self.blob_colors[0] = (int(self.min_rgb[0, 0]), int(self.min_rgb[0, 1]), int(self.min_rgb[0, 2]))
            self.blob_colors[1] = (int(self.min_rgb[1, 0]), int(self.min_rgb[1, 1]), int(self.min_rgb[1, 2]))


    def play_vkulintang(self):
        """ Main code """
        # Start the blob detection
        otherFrame = 0
        img_counter = 0
        t = []
        TIME_ELAPSED = 0
        PLAY_START = time.time()
        while True:
            start = time.time()
            ret_val, img = self.cam.read()

            if TIME_ELAPSED >= 15:
                PLAY_START = time.time()

            if otherFrame <= 0:
                img = cv2.flip(img, 1)

                

                # Draw green grid
                self.draw_grid(img)

                # Find centroids for all blobs to be detected
                for i in range(self.NUM_ITEMS):
                    self.centroid_detection(img, i, img_counter)

                end = time.time()
            
                time_elapsed = end - start
                title = "Blob Detection"
                cv2.namedWindow(title, cv2.WINDOW_NORMAL)
                cv2.resizeWindow(title, int(self.pixel_width), int(self.pixel_height))
                cv2.imshow(title, img)

                otherFrame = 0

                PLAY_END = time.time()
                TOTAL_ELAPSED = PLAY_END - PLAY_START
                t.append(time_elapsed)
            
            else:
                otherFrame = otherFrame - 1
            
            if cv2.waitKey(1) == 27: 
                # Press esc to quit
                print("Average time elapsed: {}".format(np.mean(t)*1000))
                print("Average fps: {}".format(1/np.mean(t)))
                sys.exit()
        

    def draw_grid(self, img):
        """ Draw grid on every frame """
        cv2.rectangle(img, (self.gong_1[0,0], self.gong_1[0,1]), (self.gong_1[1,0], self.gong_1[1,1]), self.gong_color_draw, 2)
        cv2.rectangle(img, (self.gong_2[0,0], self.gong_2[0,1]), (self.gong_2[1,0], self.gong_2[1,1]), self.gong_color_draw, 2)
        cv2.rectangle(img, (self.gong_3[0,0], self.gong_3[0,1]), (self.gong_3[1,0], self.gong_3[1,1]), self.gong_color_draw, 2)
        cv2.rectangle(img, (self.gong_4[0,0], self.gong_4[0,1]), (self.gong_4[1,0], self.gong_4[1,1]), self.gong_color_draw, 2)
        cv2.rectangle(img, (self.gong_5[0,0], self.gong_5[0,1]), (self.gong_5[1,0], self.gong_5[1,1]), self.gong_color_draw, 2)
        cv2.rectangle(img, (self.gong_6[0,0], self.gong_6[0,1]), (self.gong_6[1,0], self.gong_6[1,1]), self.gong_color_draw, 2)
        cv2.rectangle(img, (self.gong_7[0,0], self.gong_7[0,1]), (self.gong_7[1,0], self.gong_7[1,1]), self.gong_color_draw, 2)
        cv2.rectangle(img, (self.gong_8[0,0], self.gong_8[0,1]), (self.gong_8[1,0], self.gong_8[1,1]), self.gong_color_draw, 2)

        cv2.putText(img, "Gong 1", (self.gong_1[2,0], self.gong_1[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.text_color, 2)
        cv2.putText(img, "Gong 2", (self.gong_2[2,0], self.gong_2[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.text_color, 2)
        cv2.putText(img, "Gong 3", (self.gong_3[2,0], self.gong_3[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.text_color, 2)
        cv2.putText(img, "Gong 4", (self.gong_4[2,0], self.gong_4[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.text_color, 2)
        cv2.putText(img, "Gong 5", (self.gong_5[2,0], self.gong_5[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.text_color, 2)
        cv2.putText(img, "Gong 6", (self.gong_6[2,0], self.gong_6[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.text_color, 2)
        cv2.putText(img, "Gong 7", (self.gong_7[2,0], self.gong_7[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.text_color, 2)
        cv2.putText(img, "Gong 8", (self.gong_8[2,0], self.gong_8[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.text_color, 2)


    def centroid_detection(self, img, item_num, img_counter):
        """ Detects centroid of a given item """
        item = self.MARKER_ITEMS[item_num]

        start = time.time()

        # Detect for blob
        maskLAB = cv2.inRange(img, self.min_rgb[item_num], self.max_rgb[item_num])
        kernel = np.ones((10,10),np.uint8)
        dilation = cv2.dilate(maskLAB,kernel,iterations = 1)
        image, contours, hierarchy = cv2.findContours(dilation,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        height,width = dilation.shape[:2]
        c_areas = []

        for c in contours:
            c_area = cv2.contourArea(c)
            c_areas.append(c_area)

        # Find max contour
        self.prev_pt_2[item_num, 0] = self.prev_pt[item_num, 0]
        self.prev_pt_2[item_num, 1] = self.prev_pt[item_num, 1]
        self.prev_pt[item_num, 0] = self.new_pt[item_num, 0]
        self.prev_pt[item_num, 1] = self.new_pt[item_num, 1]

        if (len(c_areas) != 0):
            # Contours detected
            max_c_area_index = c_areas.index(max(c_areas))

            # Calculate moment and center of contour
            M = cv2.moments(contours[max_c_area_index])
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])

            self.new_pt[item_num, 0] = cX   # x-coordinate of the centroid
            self.new_pt[item_num, 1] = cY   # y-coordinate of the centroid

            """ 
            in detection using area in the original source code,
            the x,y coordinates of the centroid is used
            """

            end = time.time()

            # Update through Kalman filter
            if item_num == 2:
                self.measurement[item_num] = np.array(self.new_pt[item_num],np.float32)
                self.kalman.correct(self.measurement[item_num])
                self.prediction[item_num] = self.kalman.predict().reshape(-1,2)[0]
                self.new_pt[item_num] = self.prediction[item_num]

            cv2.circle(img, (cX, cY), 5, self.blob_colors[item_num], -1)
            cv2.putText(img, item, (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        else:
            # No contours detected so set new pt to 0
            self.INIT_ITEM[item_num] = 0
            self.new_pt[item_num, 0] = 0
            self.new_pt[item_num, 1] = 0


    """ def calculate_acceleration(self, img, item_num):
        start = time.time()

        # Calculate dynamics given prev pt and new pt
        dist = np.linalg.norm(self.new_pt[item_num]-self.prev_pt[item_num])
        self.velocities[item_num] = dist/self.DELTA_T
        self.accelerations[item_num]= (self.velocities[item_num] - self.prev_velocities[item_num])/self.DELTA_T
        self.dir_vertical[item_num] = self.new_pt[item_num,1] - self.prev_pt[item_num,1]
        self.dir_horizontal[item_num] = self.new_pt[item_num,0] - self.prev_pt[item_num,0]
        self.prev_velocities[item_num] = self.velocities[item_num]
        self.flags[item_num] -= 1

        end = time.time() """


if __name__ == '__main__':
    kulintang = vkulintang()
    kulintang.init_calibrate(2)
    kulintang.play_vkulintang()
