import cv2
import numpy as np
import time
import datetime
import pygame
from matplotlib import pyplot as plt

"""
program: image segmentation using rg chromaticity + blob detection + hit detection
change log:
    04/15/23 @ initialization: increasing frame width to accomodate gongs
    04/15/23 @ main detection: downsampling included to minimize lag during detection while accomodating increase in width
    05/02/23 @ image segmentation: modified segmentation using histogram backprojection
    05/07/23 @ blob detection: working centroid detection using numpy where and average on pixels with maximum histogram values
    05/08/23 @ blob detection: added thresholding to binarize histogram backprojected image
    05/09/23 @ blob detection: moved thresholding to calibration to reduce processing time
    05/11/12 @ hit detection: added hit detection and bounding boxes

"""

class segmentation(object):
    def __init__(self):
        self.frame_width = 854
        self.frame_height = 480
        self.pixel_width = 427
        self.pixel_height = 240
        self.DISPLAY_WIDTH = 854
        self.DISPLAY_HEIGHT = 480
        self.center = (int(self.pixel_width/2), int(self.pixel_height/2))
        self.radius = 125
        self.diameter = int(2*self.radius)

        self.center_color = (255, 0, 0)
        self.bound_color = (0, 255, 0)
        self.detection_point = np.array([[0, 0], [0, 0]])

        self.patch_size = 50
        self.patch_half = int(self.patch_size/2)
        self.patch_retrieved = False

        self.cam = None
        self.total_markers = 2
        
        # Parameters to adjust
        self.BINS = 32 # bin size of histogram
        self.THRESH = 50 # minimum histogram threshold value 
        self.MIN_CENTROID = 5 # minimum number of pixel dimensions to be considered as centroid

        # array for storing cropped patch for each marker [0,1] = [red, green]
        self.patch = [np.zeros((self.patch_size,self.patch_size,3)), np.zeros((self.patch_size,self.patch_size,3))]
        self.patch = np.array(self.patch)
        # array for storing min and max rgb values for each marker [0,1] = [red, green]
        self.min_rgb = [np.zeros((3)), np.zeros((3))]
        self.min_rgb = np.array(self.min_rgb)
        self.max_rgb = [np.zeros((3)), np.zeros((3))]
        self.max_rgb = np.array(self.max_rgb)
        # array for storing normalized chromaticity values for every pixel in the patch for each marker [0,1] = [red, green]
        self.patch_r = [np.zeros((self.patch_size,self.patch_size)), np.zeros((self.patch_size,self.patch_size))]
        self.patch_r = np.array(self.patch_r)
        self.patch_g = [np.zeros((self.patch_size,self.patch_size)), np.zeros((self.patch_size,self.patch_size))]
        self.patch_g = np.array(self.patch_g)
        self.patch_r_int = [np.zeros((self.patch_size,self.patch_size)), np.zeros((self.patch_size,self.patch_size))]
        self.patch_g_int = [np.zeros((self.patch_size,self.patch_size)), np.zeros((self.patch_size,self.patch_size))]

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
        self.gong_color_strike_r = (0, 0, 255)
        self.gong_color_strike_g = (255, 0, 0)
        self.text_color = (255, 255, 255)

        self.centroid = np.array([[0, 0], [0, 0]], dtype=np.uint16)
        self.Cr = np.array([0, 0])
        self.Cg = np.array([0, 0])

        self.hit_state_g = False
        self.hit_state_r = False
        self.directory_sound = "./kulintang_sounds/"

    def init_calibration(self):
        self.marker_calibration()
        self.init_bounding_boxes_coord()

    def init_drum_sounds(self):
            # initialize pygame
            pygame.mixer.pre_init()
            pygame.init()
            self.ifDrumSoundsOn = True

            self.gong_sound_1 = pygame.mixer.Sound(self.directory_sound + "Mgd_Kulintangan_301_P1_N0_S1.wav")
            self.gong_sound_2 = pygame.mixer.Sound(self.directory_sound + "Mgd_Kulintangan_302_P1_N0_S1.wav")
            self.gong_sound_3 = pygame.mixer.Sound(self.directory_sound + "Mgd_Kulintangan_303_P1_N0_S1.wav")
            self.gong_sound_4 = pygame.mixer.Sound(self.directory_sound + "Mgd_Kulintangan_304_P1_N0_S1.wav")
            self.gong_sound_5 = pygame.mixer.Sound(self.directory_sound + "Mgd_Kulintangan_305_P1_N0_S1.wav")
            self.gong_sound_6 = pygame.mixer.Sound(self.directory_sound + "Mgd_Kulintangan_306_P1_N0_S1.wav")
            self.gong_sound_7 = pygame.mixer.Sound(self.directory_sound + "Mgd_Kulintangan_307_P1_N0_S1.wav")
            self.gong_sound_8 = pygame.mixer.Sound(self.directory_sound + "Mgd_Kulintangan_308_P1_N0_S1.wav")

    def marker_calibration(self):
        self.cam = cv2.VideoCapture(0)
        frame_center = (int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH)/2), int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT)/2))
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH,self.frame_width)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT,self.frame_height)
        j = 0
        for i in range(self.total_markers):
            while True:
                _, frame = self.cam.read()
                mirrored = cv2.flip(frame, 1)
                mirrored_ds = self.downsample(mirrored)
                image = cv2.circle(mirrored, frame_center, self.radius + 1, self.center_color, 2)

                if i == 0:
                    title = "Calibration: Left"
                elif i == 1:
                    title = "Calibration: Right"
                cv2.namedWindow(title, cv2.WINDOW_NORMAL)
                cv2.resizeWindow(title, self.frame_width, self.frame_height)
                cv2.setMouseCallback(title, self.retrieve_patch, [mirrored_ds, i])
                cv2.imshow(title, image)

                if self.patch_retrieved == True:
                    break
                if cv2.waitKey(1) == 27:
                    break
            cv2.destroyAllWindows()
            self.patch_retrieved = False

        # Histogram of patch
        hmatrix0, _, _ = np.histogram2d(self.patch_g_int[0].flatten(), self.patch_r_int[0].flatten(), bins = self.BINS, range = [[0,self.BINS-1],[0,self.BINS-1]])
        hmatrix1, _, _ = np.histogram2d(self.patch_g_int[1].flatten(), self.patch_r_int[1].flatten(), bins = self.BINS, range = [[0,self.BINS-1],[0,self.BINS-1]])
        #np.save('hmatrix0.npy', self.hmatrix_l)
        #np.save('hmatrix1.npy', self.hmatrix_r)
        # normalize each hmatrix to max value from 0 to 100
        self.max_index_0 = np.where(hmatrix0.flatten() == np.amax(hmatrix0.flatten()))
        self.max_index_1 = np.where(hmatrix1.flatten() == np.amax(hmatrix1.flatten()))
        print(self.max_index_0)
        print(self.max_index_1)
        self.hmatrix0 = (hmatrix0 / np.amax(hmatrix0))*100
        _, self.hmatrix0 = cv2.threshold(hmatrix0, self.THRESH, 255, cv2.THRESH_BINARY)
        self.hmatrix1 = (hmatrix1 / np.amax(hmatrix1))*100
        _, self.hmatrix1 = cv2.threshold(hmatrix1, self.THRESH, 255, cv2.THRESH_BINARY)

        #plt.imsave('histogram.png',self.hmatrix)
        #plt.imsave('green.png',self.hmatrix_g)
        #plt.imsave('red.png',self.hmatrix_r)
        #self.hmatrix1d = self.hmatrix.flatten()
        self.hmatrix_01d = self.hmatrix0.flatten()
        self.hmatrix_11d = self.hmatrix1.flatten()
        #np.save('hmatrix_g1d.npy', self.hmatrix_01d)
        #np.save('hmatrix_r1d.npy', self.hmatrix_11d)

        #print(self.max_rgb[0], self.max_rgb[1])
        print("Quitting Calibration...")

    def retrieve_patch(self, event, x, y, flags, params):
        image = params[0]
        marker = params[1]

        if event == cv2.EVENT_LBUTTONDOWN:
            # Crop image to N x N patch
            new_width = (int(self.center[0]-self.patch_half), int(self.center[0]+self.patch_half))
            new_height = (int(self.center[1]-self.patch_half), int(self.center[1]+self.patch_half))
            cropped = image[new_height[0]:new_height[1], new_width[0]:new_width[1]]
            self.patch[marker] = np.array(cropped)
            self.min_rgb[marker] = np.amin(cropped, axis=(0,1))
            self.max_rgb[marker] = np.amax(cropped, axis=(0,1))
            #if marker == 0:
            #    cv2.imwrite('red_patch.jpg', cropped)
            #else:
            #    cv2.imwrite('green_patch.jpg', cropped)
            # RG chromaticity (normalized) of patch
            np.seterr(invalid='ignore')
            I = self.patch[marker].sum(axis=2)
            I[I == 0] = 100000

            self.patch_r[marker] = self.patch[marker, :,:,2] / I
            self.patch_g[marker] = self.patch[marker, :,:,1] / I
            self.patch_r_int[marker] = (self.patch_r[marker]*(self.BINS-1)).astype(int)
            self.patch_g_int[marker] = (self.patch_g[marker]*(self.BINS-1)).astype(int)

            self.patch_retrieved = True             

    def downsample(self, frame):
        '''
        reduce resolution
        '''
        res = (self.pixel_width, self.pixel_height)
        return cv2.resize(frame, res, interpolation = cv2.INTER_AREA)

    def image_segmentation(self, frame):
        """
        image_segmentation(frame)

        Returns the backprojection of the frame using the histogram matrix

        Parameters
        ----------
        frame : the downsampled RGB frame

        Returns
        -------
        thresh_r : ndarray
            Thresholded binary image of red pixels
        thresh_g : ndarray
            Thresholded binary image of green pixels
        """

        np.seterr(invalid='ignore')
        I = frame.sum(axis=2)
        I[I == 0] = 100000

        self.frame_r = frame[:,:,2] / I
        self.frame_g = frame[:,:,1] / I
        
        frame_r_int = (self.frame_r*(self.BINS-1)).astype(int)
        frame_g_int = (self.frame_g*(self.BINS-1)).astype(int)

        bp_0 = self.hmatrix_01d[frame_g_int.flatten()*self.BINS + frame_r_int.flatten()].reshape(self.frame_r.shape)
        bp_1 = self.hmatrix_11d[frame_g_int.flatten()*self.BINS + frame_r_int.flatten()].reshape(self.frame_r.shape)

        masked_0 = cv2.bitwise_and(frame, frame, mask = bp_0.astype(np.uint8))
        masked_1 = cv2.bitwise_and(frame, frame, mask = bp_1.astype(np.uint8))
        
        if self.max_index_0 < self.max_index_1:
            thresh_r = cv2.inRange(masked_0, self.min_rgb[0], self.max_rgb[0])  # left marker is red
            thresh_g = cv2.inRange(masked_1, self.min_rgb[1], self.max_rgb[1])  # right marker is green
        else:
            thresh_r = cv2.inRange(masked_0, self.min_rgb[0], self.max_rgb[0])  # left marker is green
            thresh_g = cv2.inRange(masked_1, self.min_rgb[1], self.max_rgb[1])  # right marker is red
            
        return thresh_r, thresh_g

    def blob_detection(self, frame):
        """
        blob_detection(frame)

        Calculates the centroid of the blob in the segmented frame

        Parameters
        ----------
        frame : ndarray
            An array representation of the frame's backprojection
        Returns
        -------
        center : ndarray
            An array representation of the centroid of the blob (x,y) 
            where y is the row and x is the column location in the original frame
        """
        
        center = [0,0] # center[0] = X, center[1] = Y
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
        #kernel = np.ones((2,2),np.uint8)
        frame = cv2.dilate(frame,kernel,iterations = 1)
        #frame = cv2.erode(frame, kernel, iterations = 1)
        #frame = cv2.morphologyEx(frame, cv2.MORPH_OPEN, kernel)
        indices = np.where(frame == 255)

        if indices[0].size > self.MIN_CENTROID:
            center[1] = indices[0].mean()
            center[0] = indices[1].mean()
        elif indices[0].size > 0:
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10))
            frame = cv2.dilate(frame,kernel,iterations = 1)
            indices = np.where(frame == 255)
            center[1] = indices[0].mean()
            center[0] = indices[1].mean()
            #print(indices[0].size)
        else:
            center = [0, self.grid_y1]
                    
        center = np.array(center, dtype=np.uint16)
        return center, frame

    def init_bounding_boxes_coord(self):

        self.grid_y1 = int(0.71875*self.pixel_height)    # upper y of bound
        self.grid_y2 = int(self.pixel_height)           # lower y of bound
        # self.bound_width = 135
        self.bound_width = 0.125                        # x is 12.5% of width

        self.gong_1[0,:] = [0, self.grid_y1]                                                            # (0, upper y)
        self.gong_1[1,:] = [int(self.bound_width*self.pixel_width), self.grid_y2]    #                   (135, lower y)
        self.gong_1[2,:] = [((self.gong_1[0,0] + self.gong_1[1,0])/2) - 12, self.gong_1[0,1] + 25]      # label coordinates

        self.gong_2[0,:] = [int(self.bound_width*self.pixel_width), self.grid_y1]                       # (135, upper y)
        self.gong_2[1,:] = [int(2*self.bound_width*self.pixel_width), self.grid_y2]                     # (270, lower y)
        self.gong_2[2,:] = [((self.gong_2[0,0] + self.gong_2[1,0])/2) - 12, self.gong_2[0,1] + 25]

        self.gong_3[0,:] = [int(2*self.bound_width*self.pixel_width), self.grid_y1]                     # (270, upper y)
        self.gong_3[1,:] = [int(3*self.bound_width*self.pixel_width), self.grid_y2]                     # (405, lower y)
        self.gong_3[2,:] = [((self.gong_3[0,0] + self.gong_3[1,0])/2) - 12, self.gong_3[0,1] + 25]

        self.gong_4[0,:] = [int(3*self.bound_width*self.pixel_width), self.grid_y1]                     # (405, upper y)
        self.gong_4[1,:] = [int(4*self.bound_width*self.pixel_width), self.grid_y2]                     # (540, lower y)
        self.gong_4[2,:] = [((self.gong_4[0,0] + self.gong_4[1,0])/2) - 12, self.gong_4[0,1] + 25]

        self.gong_5[0,:] = [int(4*self.bound_width*self.pixel_width), self.grid_y1]                     # (540, upper y)
        self.gong_5[1,:] = [int(5*self.bound_width*self.pixel_width), self.grid_y2]                     # (675, lower y)
        self.gong_5[2,:] = [((self.gong_5[0,0] + self.gong_5[1,0])/2) - 12, self.gong_5[0,1] + 25]

        self.gong_6[0,:] = [int(5*self.bound_width*self.pixel_width), self.grid_y1]                     # (675, upper y)
        self.gong_6[1,:] = [int(6*self.bound_width*self.pixel_width), self.grid_y2]                     # (810, lower y)
        self.gong_6[2,:] = [((self.gong_6[0,0] + self.gong_6[1,0])/2) - 12, self.gong_6[0,1] + 25]

        self.gong_7[0,:] = [int(6*self.bound_width*self.pixel_width), self.grid_y1]                     # (810, upper y)
        self.gong_7[1,:] = [int(7*self.bound_width*self.pixel_width), self.grid_y2]                     # (945, lower y)
        self.gong_7[2,:] = [((self.gong_7[0,0] + self.gong_7[1,0])/2) - 12, self.gong_7[0,1] + 25]

        self.gong_8[0,:] = [int(7*self.bound_width*self.pixel_width), self.grid_y1]                     # (945, upper y)
        self.gong_8[1,:] = [int(8*self.bound_width*self.pixel_width), self.grid_y2]                     # (1080, lower y)
        self.gong_8[2,:] = [((self.gong_8[0,0] + self.gong_8[1,0])/2) - 12, self.gong_8[0,1] + 25]

    def disp_config(self, frame, Cr, Cg):
        """
        Draw bounding boxes and centroid for every frame
        -----------
        Parameters:
        frame : current frame to be displayed
        Cr : centroid of red blob
        Cg : centroid of green blob
        """

        #----- draw centroid -----
        if Cr[1] != self.grid_y1:
            cv2.circle(frame, (Cr[0], Cr[1]), 5, (255, 0, 0), -1)
        if Cg[1] != self.grid_y1:
            cv2.circle(frame, (Cg[0], Cg[1]), 5, (255, 0, 0), -1)
        
        #----- draw bounding boxes -----
        cv2.rectangle(frame, (self.gong_1[0,0], self.gong_1[0,1]), (self.gong_1[1,0], self.gong_1[1,1]), self.gong_color_draw, 2)
        cv2.rectangle(frame, (self.gong_2[0,0], self.gong_2[0,1]), (self.gong_2[1,0], self.gong_2[1,1]), self.gong_color_draw, 2)
        cv2.rectangle(frame, (self.gong_3[0,0], self.gong_3[0,1]), (self.gong_3[1,0], self.gong_3[1,1]), self.gong_color_draw, 2)
        cv2.rectangle(frame, (self.gong_4[0,0], self.gong_4[0,1]), (self.gong_4[1,0], self.gong_4[1,1]), self.gong_color_draw, 2)
        cv2.rectangle(frame, (self.gong_5[0,0], self.gong_5[0,1]), (self.gong_5[1,0], self.gong_5[1,1]), self.gong_color_draw, 2)
        cv2.rectangle(frame, (self.gong_6[0,0], self.gong_6[0,1]), (self.gong_6[1,0], self.gong_6[1,1]), self.gong_color_draw, 2)
        cv2.rectangle(frame, (self.gong_7[0,0], self.gong_7[0,1]), (self.gong_7[1,0], self.gong_7[1,1]), self.gong_color_draw, 2)
        cv2.rectangle(frame, (self.gong_8[0,0], self.gong_8[0,1]), (self.gong_8[1,0], self.gong_8[1,1]), self.gong_color_draw, 2)

        #----- add labels -----
        # green centroid
        cv2.putText(frame, "RIGHT", (Cg[0] - 25, Cg[1] - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)
        # red centroid
        cv2.putText(frame, "LEFT", (Cr[0] - 25, Cr[1] - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)
        # gong labels
        cv2.putText(frame, "Gong 1", (self.gong_1[2,0], self.gong_1[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.25, self.text_color, 1)
        cv2.putText(frame, "Gong 2", (self.gong_2[2,0], self.gong_2[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.25, self.text_color, 1)
        cv2.putText(frame, "Gong 3", (self.gong_3[2,0], self.gong_3[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.25, self.text_color, 1)
        cv2.putText(frame, "Gong 4", (self.gong_4[2,0], self.gong_4[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.25, self.text_color, 1)
        cv2.putText(frame, "Gong 5", (self.gong_5[2,0], self.gong_5[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.25, self.text_color, 1)
        cv2.putText(frame, "Gong 6", (self.gong_6[2,0], self.gong_6[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.25, self.text_color, 1)
        cv2.putText(frame, "Gong 7", (self.gong_7[2,0], self.gong_7[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.25, self.text_color, 1)
        cv2.putText(frame, "Gong 8", (self.gong_8[2,0], self.gong_8[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.25, self.text_color, 1)
    
    def hit_detection(self, Cr, Cg):
        """
        hit_detection(Cr, Cg)

        Detects if the centroid has hit any of the gong boxes

        Parameters
        ----------
        Cr : ndarray
            An array representation of the centroid of the red blob (x,y) 
            where y is the row and x is the column location in the original frame
        Cg : ndarray
            An array representation of the centroid of the green blob (x,y) 
            where y is the row and x is the column location in the original frame
        Returns
        -------
        gong_no : list
            gong number hit detected for green and red centroid. 0 if false.
        """
        gong_no = [0,0] # each element corresponds to the gong nos. hit by the green centroid and the red centroid

        
        #----- check if blob is in hit state (i.e. centroid is previously hit, not held within bounding box)
        if self.hit_state_g == False:
            #----- check if motion is downwards -----
            if (self.Cg_prev < Cg[1]):
                #----- check if green blob is within detection area -----
                if (Cg[1] > self.grid_y1):
                    self.hit_state_g = True
                    #---- Binary search algorithm for checking x coordinates
                    if Cg[0] <= self.gong_5[0,0]:
                        if Cg[0] <= self.gong_3[0,0]:
                            if Cg[0] <= self.gong_2[0,0]:
                                gong_no[0] = 1
                            else:
                                gong_no[0] = 2
                        else:
                            if Cg[0] <= self.gong_4[0,0]:
                                gong_no[0] = 3
                            else:
                                gong_no[0] = 4
                    else:
                        if Cg[0] <= self.gong_7[0,0]:
                            if Cg[0] <= self.gong_6[0,0]:
                                gong_no[0] = 5
                            else:
                                gong_no[0] = 6
                        else:
                            if Cg[0] <= self.gong_8[0,0]:
                                gong_no[0] = 7
                            else:
                                gong_no[0] = 8

        #----- check if blob is in hit state (i.e. centroid is previously hit, not held within bounding box)
        if self.hit_state_r == False:
            #---- check if motion is downwards ----
            if (self.Cr_prev < Cr[1]):
                #----- check if red blob is within detection area -----
                if (Cr[1] > self.grid_y1):
                    self.hit_state_r = True
                    #---- Binary search algorithm for checking x coordinates
                    if Cr[0] <= self.gong_5[0,0]:
                        if Cr[0] <= self.gong_3[0,0]:
                            if Cr[0] <= self.gong_2[0,0]:
                                gong_no[1] = 1
                            else:
                                gong_no[1] = 2
                        else:
                            if Cr[0] <= self.gong_4[0,0]:
                                gong_no[1] = 3
                            else:
                                gong_no[1] = 4
                    else:
                        if Cr[0] <= self.gong_7[0,0]:
                            if Cr[0] <= self.gong_6[0,0]:
                                gong_no[1] = 5
                            else:
                                gong_no[1] = 6
                        else:
                            if Cr[0] <= self.gong_8[0,0]:
                                gong_no[1] = 7
                            else:
                                gong_no[1] = 8


        return gong_no
    
    def play_kulintang(self, gong_no, frame):
        """
        play_kulintang(gong_no, frame)

        Plays the sound and animation of the gong hit

        Parameters
        ----------
        gong_no : list
            gong number hit detected for green and red centroid. 0 if false.
        """

        #----- display animation and play sound for hits in the green centroid
        if gong_no[0] > 0:
            if gong_no[0] < 5:
                if gong_no[0] < 3:
                    if gong_no[0] < 2:
                        cv2.rectangle(frame, (self.gong_1[0,0], self.gong_1[0,1]), (self.gong_1[1,0], self.gong_1[1,1]), self.gong_color_strike_g, 2)
                        self.gong_sound_1.play()
                    else:
                        cv2.rectangle(frame, (self.gong_2[0,0], self.gong_2[0,1]), (self.gong_2[1,0], self.gong_2[1,1]), self.gong_color_strike_g, 2)
                        self.gong_sound_2.play()
                else:
                    if gong_no[0] < 4:
                        cv2.rectangle(frame, (self.gong_3[0,0], self.gong_3[0,1]), (self.gong_3[1,0], self.gong_3[1,1]), self.gong_color_strike_g, 2)
                        self.gong_sound_3.play()
                    else:
                        cv2.rectangle(frame, (self.gong_4[0,0], self.gong_4[0,1]), (self.gong_4[1,0], self.gong_4[1,1]), self.gong_color_strike_g, 2)
                        self.gong_sound_4.play()
            else:
                if gong_no[0] < 7:
                    if gong_no[0] < 6:
                        cv2.rectangle(frame, (self.gong_5[0,0], self.gong_5[0,1]), (self.gong_5[1,0], self.gong_5[1,1]), self.gong_color_strike_g, 2)
                        self.gong_sound_5.play()
                    else:
                        cv2.rectangle(frame, (self.gong_6[0,0], self.gong_6[0,1]), (self.gong_6[1,0], self.gong_6[1,1]), self.gong_color_strike_g, 2)
                        self.gong_sound_6.play()
                else:
                    if gong_no[0] < 8:
                        cv2.rectangle(frame, (self.gong_7[0,0], self.gong_7[0,1]), (self.gong_7[1,0], self.gong_7[1,1]), self.gong_color_strike_g, 2)
                        self.gong_sound_7.play()
                    else:
                        cv2.rectangle(frame, (self.gong_8[0,0], self.gong_8[0,1]), (self.gong_8[1,0], self.gong_8[1,1]), self.gong_color_strike_g, 2)
                        self.gong_sound_8.play()

        #----- display animation and play sound for hits in the red centroid
        if gong_no[1] > 0:
            if gong_no[1] < 5:
                if gong_no[1] < 3:
                    if gong_no[1] < 2:
                        cv2.rectangle(frame, (self.gong_1[0,0], self.gong_1[0,1]), (self.gong_1[1,0], self.gong_1[1,1]), self.gong_color_strike_r, 2)
                        self.gong_sound_1.play()
                    else:
                        cv2.rectangle(frame, (self.gong_2[0,0], self.gong_2[0,1]), (self.gong_2[1,0], self.gong_2[1,1]), self.gong_color_strike_r, 2)
                        self.gong_sound_2.play()
                else:
                    if gong_no[1] < 4:
                        cv2.rectangle(frame, (self.gong_3[0,0], self.gong_3[0,1]), (self.gong_3[1,0], self.gong_3[1,1]), self.gong_color_strike_r, 2)
                        self.gong_sound_3.play()
                    else:
                        cv2.rectangle(frame, (self.gong_4[0,0], self.gong_4[0,1]), (self.gong_4[1,0], self.gong_4[1,1]), self.gong_color_strike_r, 2)
                        self.gong_sound_4.play()
            else:
                if gong_no[1] < 7:
                    if gong_no[1] < 6:
                        cv2.rectangle(frame, (self.gong_5[0,0], self.gong_5[0,1]), (self.gong_5[1,0], self.gong_5[1,1]), self.gong_color_strike_r, 2)
                        self.gong_sound_5.play()
                    else:
                        cv2.rectangle(frame, (self.gong_6[0,0], self.gong_6[0,1]), (self.gong_6[1,0], self.gong_6[1,1]), self.gong_color_strike_r, 2)
                        self.gong_sound_6.play()
                else:
                    if gong_no[1] < 8:
                        cv2.rectangle(frame, (self.gong_7[0,0], self.gong_7[0,1]), (self.gong_7[1,0], self.gong_7[1,1]), self.gong_color_strike_r, 2)
                        self.gong_sound_7.play()
                    else:
                        cv2.rectangle(frame, (self.gong_8[0,0], self.gong_8[0,1]), (self.gong_8[1,0], self.gong_8[1,1]), self.gong_color_strike_r, 2)
                        self.gong_sound_8.play()
        
        #if gong_no[0] > 0:
        #    cv2.imwrite('strike_g.png', frame)
        #if gong_no[1] > 0:
        #    cv2.imwrite('strike_r.png', frame)


    def update_hit_state(self):
        # ----- update hit state -----
        if self.hit_state_g == True:
            if self.Cg[1] < self.grid_y1:
                self.hit_state_g = False

        if self.hit_state_r == True:
            if self.Cr[1] < self.grid_y1:
                self.hit_state_r = False

    def main_detection(self):
        ''' Main Code '''
        t = []
        i = 0
        while True:
            
            start = time.time()
            _, frame = self.cam.read()
            frame = self.downsample(frame)
            frame = cv2.flip(frame, 1)
            binary_r, binary_g = self.image_segmentation(frame)
            #-------- blob detection -----------
            self.Cr_prev = self.Cr[1]
            self.Cg_prev = self.Cg[1]
            self.Cr, morphed_r = self.blob_detection(binary_r)
            self.Cg, morphed_g = self.blob_detection(binary_g)
            end = time.time()
            t.append(end - start)
            #-------- configure display --------  
            self.disp_config(frame, self.Cr, self.Cg)
            #-------- hit detection ------------
            self.update_hit_state()
            gong_no = self.hit_detection(self.Cr, self.Cg)
            #----- play sound and animation ----
            self.play_kulintang(gong_no, frame)
            #-------- display frame ------------
            i = i + 1
            title = "Virtual Kulintang"
            cv2.namedWindow(title, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(title, int(self.DISPLAY_WIDTH*0.8), int(self.DISPLAY_HEIGHT*0.8))
            cv2.imshow(title, frame)
            
            #display = np.concatenate((binary_r, binary_g), axis = 1)
            #title = "Image Segmentation"
            #cv2.namedWindow(title, cv2.WINDOW_NORMAL)
            #cv2.resizeWindow(title, int(self.DISPLAY_WIDTH), int(self.DISPLAY_HEIGHT/2))
            #cv2.imshow(title, display)

            morphed = np.concatenate((morphed_r, morphed_g), axis = 1)
            title = "Morphological Operation"
            cv2.namedWindow(title, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(title, int(self.DISPLAY_WIDTH), int(self.DISPLAY_HEIGHT/2))
            cv2.imshow(title, morphed)
            
            #if i == 80:
            #    cv2.imwrite('system.png', frame)

            
            if cv2.waitKey(1) == 27:
                break

        #--------------- termination sequence ------------------
        self.cam.release()
        cv2.destroyAllWindows()
        print("Quitting Detection...")
        #------------ print average execution time -------------
        avg_t = sum(t)/len(t)
        now = datetime.datetime.now()
        print(now.strftime("%Y-%m-%d %H:%M:%S"))
        print("Average numpy where + mean execution time: {0:.2f} msec".format(avg_t*1000))
        print("Average frame rate: {} fps".format(int(1/avg_t)))


if __name__ == '__main__':
    start = segmentation()
    start.init_drum_sounds()
    start.init_calibration()
    start.main_detection()
