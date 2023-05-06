import cv2
import numpy as np
import time
import sys
import logging
import pygame

# Configure logger
#logging.basicConfig(filename="test.log", format='%(filename)s: %(message)s', filemode='w')
logPath = "."
fileName = "test"
logging.basicConfig(
    level=logging.ERROR,
    #format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
    format="%(asctime)s %(message)s",
    handlers=[
        logging.FileHandler("{0}/{1}.log".format(logPath, fileName)),
        logging.StreamHandler()
    ])
# Create a logger object
logger = logging.getLogger()



class AirDrums(object):
    def __init__(self):
        # Frame details
        self.frame_width_default = 640
        self.frame_height_default = 480
        self.frame_width = 640
        self.frame_height = 480
        self.grid_x1 = 0
        self.grid_x2 = 0
        self.grid_y1 = 0
        self.grid_y2 = 0
        self.grid_color = (0, 255, 0)

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


        # Patch sizes
        # Get 10x10 patch from center
        self.patch_size = 10
        self.patch_total_size = self.patch_size*self.patch_size

        # RGB Calibration
        self.CALIBRATED = False
        # Left, right, bass
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
        # flag for detection
        self.flags = [0, 0, 0]

        # Init of camera
        self.cam = None

        # FPS
        self.FPS = 0
        # DELTA_T = 1/FPS
        self.DELTA_T = 0

        # Drum sounds
        self.ifDrumSoundsOn = False
        self.directory_sound = "./sounds/"

        self.DRUM_ITEMS = ["Left", "Right", "Bass"]

        self.drum_snare = None
        self.drum_hihat = None
        self.drum_crash = None

        self.drum_tom1 = None
        self.drum_tom2 = None
        self.drum_ride = None

        self.drum_floor = None
        self.drum_bass = None

        # Drum coordinates, upper left, lowerr right coordinates in [x, y]
        # 3rd coordinate is placement of drum name
        # 4th coordinate is y coordinate for 50% area coverage
        self.coord_crash = np.array([[0, 0], [0, 0], [0, 0]])
        self.coord_hihat = np.array([[0, 0], [0, 0], [0, 0]])
        self.coord_snare = np.array([[0, 0], [0, 0], [0, 0]])

        self.coord_tom1 = np.array([[0, 0], [0, 0], [0, 0]])
        self.coord_bass = np.array([[0, 0], [0, 0], [0, 0]])

        self.coord_ride = np.array([[0, 0], [0, 0], [0, 0]])
        self.coord_tom2 = np.array([[0, 0], [0, 0], [0, 0]])
        self.coord_floor = np.array([[0, 0], [0, 0], [0, 0]])

        self.drum_color_1 =  (0, 255, 0)
        self.drum_color_2 = (255, 0, 0)


        self.num_hits = 0


    def cb_calibrate(self, event, x, y, flags, params):
        '''
            Mouse callback for initial calibration of points
        '''
        img = params[0]
        item_num = params[1]
        descriptor = []

        if event == cv2.EVENT_LBUTTONDOWN:
            point = (x, y)
            line = "[x,y]: {},{} (rgb): ({})".format(point[0], point[1], img[y, x])
            #logger.debug(line)

            step_size = int(self.patch_size/2)
            height, width = img.shape[:2]

            # Turn into rows, cols format
            top_left = (point[1] - step_size, point[0] - step_size) 
            bottom_right = (point[1] + step_size, point[0] + step_size)

            # Check for top_left for out of bounds
            if (top_left[0] >= height) or (top_left[0] < 0) or (top_left[1] >= width) or (top_left[1] < 0):
                #logger.debug("out of bounds")
                return
            if (bottom_right[0] >= height) or (bottom_right[0] < 0) or (bottom_right[1] >= width) or (bottom_right[1] < 0):
                #logger.debug("out of bounds")
                return

            # Get descriptor, going through rows
            for m in range(top_left[0], bottom_right[0] + 1):
                # Going through columns
                for n in range(top_left[1], bottom_right[1] + 1):
                    descriptor.append(img[m, n])
            descriptor = np.array(descriptor)
            #logger.debug(descriptor)

            self.min_rgb[item_num, 0] = np.min(descriptor[:,0][self.patch_size:self.patch_total_size-self.patch_size])
            self.max_rgb[item_num, 0] = np.max(descriptor[:,0][self.patch_size:self.patch_total_size-self.patch_size])
            self.min_rgb[item_num, 1] = np.min(descriptor[:,1][self.patch_size:self.patch_total_size-self.patch_size])
            self.max_rgb[item_num, 1] = np.max(descriptor[:,1][self.patch_size:self.patch_total_size-self.patch_size])
            self.min_rgb[item_num, 2] = np.min(descriptor[:,2][self.patch_size:self.patch_total_size-self.patch_size])
            self.max_rgb[item_num, 2] = np.max(descriptor[:,2][self.patch_size:self.patch_total_size-self.patch_size])

            #logger.debug("Calibration Done!")
            self.CALIBRATED = True

    def init_drum_sounds(self):
        # initialize pygame
        pygame.mixer.pre_init()
        pygame.init()
        self.ifDrumSoundsOn = True

        self.drum_crash = pygame.mixer.Sound(self.directory_sound + "crash.wav")
        self.drum_hihat = pygame.mixer.Sound(self.directory_sound + "hihat.wav")
        self.drum_snare = pygame.mixer.Sound(self.directory_sound + "snare.wav")

        self.drum_tom1 = pygame.mixer.Sound(self.directory_sound + "tom1.wav")
        self.drum_bass = pygame.mixer.Sound(self.directory_sound + "kick.wav")

        self.drum_ride = pygame.mixer.Sound(self.directory_sound + "ride.wav")
        self.drum_tom2 = pygame.mixer.Sound(self.directory_sound + "tom2.wav")
        self.drum_floor = pygame.mixer.Sound(self.directory_sound + "floor.wav")


    def init_calibrate(self, num_items):
        # Initialize calibrations

        self.NUM_ITEMS = num_items

        self.frameCalibration()
        self.colorCalibrations()

    def frameCalibration(self):
        '''
            Calculate initial FPS
            Also initialize frames and drum coordinates
        '''
        self.cam = cv2.VideoCapture(0)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH,self.frame_width_default)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT,self.frame_height_default)

        self.frame_width = int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        #logger.debug("width: {}, height: {}".format(self.frame_width, self.frame_height))

        self.grid_x1 = int(0.33*self.frame_width)
        self.grid_x2 = int(0.66*self.frame_width)
        self.grid_y1 = int(0.33*self.frame_height)
        self.grid_y2 = int(0.66*self.frame_height)

        self.grid_y1_5 = int(0.16*self.frame_height)
        self.grid_y2_5 = int(0.48*self.frame_height)
        self.grid_y3_5 = int(0.8*self.frame_height)

        # Initialize drum area bounding box coordinates

        # Left column of boxes
        self.coord_crash[0,:] = [0, self.grid_y1_5]
        self.coord_crash[1,:] = [self.grid_x1, self.grid_y1]
        self.coord_crash[2,:] = [((self.coord_crash[0,0] + self.coord_crash[1,0])/2) - 25, self.coord_crash[0,1] + 25]

        self.coord_hihat[0,:] = [0, self.grid_y2_5]
        self.coord_hihat[1,:] = [self.grid_x1, self.grid_y2]
        self.coord_hihat[2,:] = [((self.coord_hihat[0,0] + self.coord_hihat[1,0])/2) - 25, self.coord_hihat[0,1] + 25]


        self.coord_snare[0,:] = [0, self.grid_y3_5]
        self.coord_snare[1,:] = [self.grid_x1, self.frame_height]
        self.coord_snare[2,:] = [((self.coord_snare[0,0] + self.coord_snare[1,0])/2) - 25, self.coord_snare[0,1] + 25]


        # Center column of boxes
        self.coord_tom1[0,:] = [self.grid_x1, self.grid_y2_5]
        self.coord_tom1[1,:] = [self.grid_x2, self.grid_y2]
        self.coord_tom1[2,:] = [((self.coord_tom1[0,0] + self.coord_tom1[1,0])/2) - 25, self.coord_tom1[0,1] + 25]


        self.coord_bass[0,:] = [self.grid_x1, self.grid_y3_5]
        self.coord_bass[1,:] = [self.grid_x2, self.frame_height]
        self.coord_bass[2,:] = [((self.coord_bass[0,0] + self.coord_bass[1,0])/2) - 25, self.coord_bass[0,1] + 25]


        # Right column of boxes
        self.coord_ride[0,:] = [self.grid_x2, self.grid_y1_5]
        self.coord_ride[1,:] = [self.frame_width, self.grid_y1]
        self.coord_ride[2,:] = [((self.coord_ride[0,0] + self.coord_ride[1,0])/2) - 25, self.coord_ride[0,1] + 25]


        self.coord_tom2[0,:] = [self.grid_x2, self.grid_y2_5]
        self.coord_tom2[1,:] = [self.frame_width, self.grid_y2]
        self.coord_tom2[2,:] = [((self.coord_tom2[0,0] + self.coord_tom2[1,0])/2) - 25, self.coord_tom2[0,1] + 25]


        self.coord_floor[0,:] = [self.grid_x2, self.grid_y3_5]
        self.coord_floor[1,:] = [self.frame_width, self.frame_height]
        self.coord_floor[2,:] = [((self.coord_floor[0,0] + self.coord_floor[1,0])/2) - 25, self.coord_floor[0,1] + 25]




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
        #logger.debug('FPS: %.2f'%self.FPS)
        #logger.debug('DELTA_T: %.2f'%self.DELTA_T)


    def colorCalibrations(self):
        '''
            Computes the color calibrations for the left and right sticks
        '''
        for i in range(self.NUM_ITEMS):
            item = self.DRUM_ITEMS[i]

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
            #logger.debug(self.min_rgb)
            #logger.debug(self.max_rgb)

        self.blob_colors[0] = (int(self.min_rgb[0, 0]), int(self.min_rgb[0, 1]), int(self.min_rgb[0, 2]))
        self.blob_colors[1] = (int(self.min_rgb[1, 0]), int(self.min_rgb[1, 1]), int(self.min_rgb[1, 2]))
        #logger.debug('BLOB_COLORS')
        #logger.debug(self.blob_colors[0])
        #logger.debug(self.blob_colors[1])


    def playDrums(self):
        '''
            The main mode of AirDrums
        '''
        # Start the blob detection
        otherFrame = 0
        img_counter = 0
        TIME_ELAPSED = 0
        PLAY_START = time.time()
        while True:
            ret_val, img = self.cam.read()

            if TIME_ELAPSED >= 15:
                PLAY_START = time.time()

            if otherFrame <= 0:

                img = cv2.flip(img, 1)

                start = time.time()

                # Draw green grid
                self.drawGrid(img)
                # Draw drum names
                self.drawDrumNames(img)


                # Find centroids for all blobs to be detected
                for i in range(self.NUM_ITEMS):
                    self.centroidDetection(img, i, img_counter)

                # Calculate dynamics for all blobs
                #for i, val in enumerate(self.CALIBRATIONS):
                #    self.calculateDynamics(img, i)

                # Check what drum pad was triggered
                # for i, val in enumerate(self.CALIBRATIONS):
                #     self.detectTriggerThruDynamics(img, i)

                for i in range(2):
                    self.detectTriggerThruArea(img, i)

                # include bass drum
                if (self.NUM_ITEMS == 2):
                    for i in range(2):
                        self.detectBassTrigger(img, self.NUM_ITEMS, i)
                else:
                    self.detectBassTrigger(img, self.NUM_ITEMS, 2)



                end = time.time()
                time_elapsed = end - start
                #logger.debug("Seconds elapsed: {}".format(time_elapsed))
                cv2.imshow("AirDrums", img)
                #img_name = "frame_{}.jpg".format(img_counter)
                #cv2.imwrite("./AirDrums_v7_data/" + img_name, img)
                #img_counter = img_counter + 1

                otherFrame = 0

                PLAY_END = time.time()
                TOTAL_ELAPSED = PLAY_END - PLAY_START
                line = "time: {}, hits: {}".format(TOTAL_ELAPSED, self.num_hits)
                logger.info(line)
            else:
                otherFrame = otherFrame - 1


            if cv2.waitKey(1) == 27: 
                # Press esc to quit
                sys.exit()

    def drawDrumNames(self, img):
        '''
            Draw drum names on every frame
        '''
        cv2.putText(img, "CRASH", (self.coord_crash[2,0], self.coord_crash[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.drum_color_1, 2)
        cv2.putText(img, "HIHAT", (self.coord_hihat[2,0], self.coord_hihat[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.drum_color_1, 2)
        cv2.putText(img, "SNARE", (self.coord_snare[2,0], self.coord_snare[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.drum_color_1, 2)

        cv2.putText(img, "TOM1", (self.coord_tom1[2,0], self.coord_tom1[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.drum_color_1, 2)
        cv2.putText(img, "BASS", (self.coord_bass[2,0], self.coord_bass[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.drum_color_1, 2)

        cv2.putText(img, "RIDE", (self.coord_ride[2,0], self.coord_ride[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.drum_color_1, 2)
        cv2.putText(img, "TOM2", (self.coord_tom2[2,0], self.coord_tom2[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.drum_color_1, 2)
        cv2.putText(img, "FLOOR", (self.coord_floor[2,0], self.coord_floor[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.drum_color_1, 2)



    def drawGrid(self, img):
        '''
            Draw grid on every frame
        '''
        # cv2.line(img, (self.grid_x1, 0), (self.grid_x1, self.frame_height), self.grid_color, 1, 1)
        # cv2.line(img, (self.grid_x2, 0), (self.grid_x2, self.frame_height), self.grid_color, 1, 1)
        # cv2.line(img, (0, self.grid_y1), (self.frame_width, self.grid_y1), self.grid_color, 1, 1)
        # cv2.line(img, (0, self.grid_y2), (self.frame_width, self.grid_y2), self.grid_color, 1, 1)


        # # For 50%
        # cv2.line(img, (0, self.grid_y1_5), (self.frame_width, self.grid_y1_5), self.drum_color_2, 1, 1)
        # cv2.line(img, (0, self.grid_y2_5), (self.frame_width, self.grid_y2_5), self.drum_color_2, 1, 1)
        # cv2.line(img, (0, self.grid_y3_5), (self.frame_width, self.grid_y3_5), self.drum_color_2, 1, 1)


        cv2.rectangle(img, (self.coord_crash[0,0], self.coord_crash[0,1]), (self.coord_crash[1,0], self.coord_crash[1,1]), self.drum_color_1, 2)
        cv2.rectangle(img, (self.coord_hihat[0,0], self.coord_hihat[0,1]), (self.coord_hihat[1,0], self.coord_hihat[1,1]), self.drum_color_1, 2)
        cv2.rectangle(img, (self.coord_snare[0,0], self.coord_snare[0,1]), (self.coord_snare[1,0], self.coord_snare[1,1]), self.drum_color_1, 2)


        cv2.rectangle(img, (self.coord_tom1[0,0], self.coord_tom1[0,1]), (self.coord_tom1[1,0], self.coord_tom1[1,1]), self.drum_color_1, 2)
        cv2.rectangle(img, (self.coord_bass[0,0], self.coord_bass[0,1]), (self.coord_bass[1,0], self.coord_bass[1,1]), self.drum_color_1, 2)

        cv2.rectangle(img, (self.coord_ride[0,0], self.coord_ride[0,1]), (self.coord_ride[1,0], self.coord_ride[1,1]), self.drum_color_1, 2)
        cv2.rectangle(img, (self.coord_tom2[0,0], self.coord_tom2[0,1]), (self.coord_tom2[1,0], self.coord_tom2[1,1]), self.drum_color_1, 2)
        cv2.rectangle(img, (self.coord_floor[0,0], self.coord_floor[0,1]), (self.coord_floor[1,0], self.coord_floor[1,1]), self.drum_color_1, 2)




    def centroidDetection(self, img, item_num, img_counter):
        '''
            Detects the centroid of a given item
        '''

        item = self.DRUM_ITEMS[item_num]

        start = time.time()
        # Detect for blob
        maskLAB = cv2.inRange(img, self.min_rgb[item_num], self.max_rgb[item_num])
        #img_name = "thresholds_{}_{}.jpg".format(self.DRUM_ITEMS[item_num], img_counter)
        #cv2.imwrite("./AirDrums_v7_data/" + img_name, maskLAB)
        kernel = np.ones((10,10),np.uint8)
        dilation = cv2.dilate(maskLAB,kernel,iterations = 1)
        #img_name = "dilation_{}_{}.jpg".format(self.DRUM_ITEMS[item_num], img_counter)
        #cv2.imwrite("./AirDrums_v7_data/" + img_name, dilation)

        im2, contours, hierarchy = cv2.findContours(dilation,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        height,width = dilation.shape[:2]
        #img = np.zeros((height,width,3), np.uint8)
        c_areas = []

        for c in contours:
            c_area = cv2.contourArea(c)
            c_areas.append(c_area)

        # Find max contour
        # Check if no contours detected

        self.prev_pt_2[item_num, 0] = self.prev_pt[item_num, 0]
        self.prev_pt_2[item_num, 1] = self.prev_pt[item_num, 1]
        self.prev_pt[item_num, 0] = self.new_pt[item_num, 0]
        self.prev_pt[item_num, 1] = self.new_pt[item_num, 1]
        if (len(c_areas) != 0):
            max_c_area_index = c_areas.index(max(c_areas))
            #logger.debug(max_c_area_index)
            # Calculate moment and center of contour
            M = cv2.moments(contours[max_c_area_index])
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])


            self.new_pt[item_num, 0] = cX
            self.new_pt[item_num, 1] = cY


            end = time.time()
            #logger.debug("[CENTROID DETECTION]: Seconds elapsed: {}".format(end-start))
            
            # update through kalman filter
            
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




    def calculateDynamics(self, img, item_num):
        start = time.time()

        # Calculate dynamics given prev pt and new pt
        #logger.debug(self.new_pt[item_num])
        #logger.debug(self.prev_pt[item_num])
        dist = np.linalg.norm(self.new_pt[item_num]-self.prev_pt[item_num])
        self.velocities[item_num] = dist/self.DELTA_T
        self.accelerations[item_num]= (self.velocities[item_num] - self.prev_velocities[item_num])/self.DELTA_T
        self.dir_vertical[item_num] = self.new_pt[item_num,1] - self.prev_pt[item_num,1]
        self.dir_horizontal[item_num] = self.new_pt[item_num,0] - self.prev_pt[item_num,0]
        self.prev_velocities[item_num] = self.velocities[item_num]
        self.flags[item_num] -= 1

        #logger.debug('Velocity: %.2f pixels/second'%self.velocities[item_num])
        #logger.debug('Acceleration: {} pixels/second'.format(self.accelerations[item_num]))

        # Apply thresholding given acceleration

        #acceleration_str = "{:.2f}".format(self.accelerations[item_num])
        #cv2.putText(img, acceleration_str, (self.new_pt[item_num,0] - 50, self.new_pt[item_num,1]  - 50),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        end = time.time()
        #logger.debug("[DYNAMICS]: Seconds elapsed: {}".format(end-start))

    def detectTriggerThruDynamics(self, img, item_num):
        '''
            Detect trigger thru calculateDynamics()
        '''
        # For left and right sticks
        if item_num != 2:
            #logger.debug("[LEFT&RIGHT: CALCULATE DYNAMICS]")

            #logger.debug('flags: %d'%self.flags[item_num])
            # Triggered!
            if (self.accelerations[item_num] < -4000) and (self.dir_vertical[item_num] > 0) and (self.flags[item_num] < 0):
                #logger.debug('Acceleration: {} pixels/second'.format(self.accelerations[item_num]))
                self.flags[item_num] = 5

                # Detect which area was triggered
                self.detectArea(img,item_num)

        #else:
            # For bass drum
            #logger.debug("[BASS DRUM: CALCULATE DYNAMICS]")

    def detectArea(self, img, item_num):
        '''
            Detect area given left or right stick
        '''
        #logger.debug("[Detect area]: {}".format(self.DRUM_ITEMS[item_num]))
        #if self.new_pt[i, 0]

        # For first column
        if (self.new_pt[item_num, 0] <= self.grid_x1):
            if (self.new_pt[item_num, 1] <= self.grid_y1):
                #logger.debug("[DETECT AREA]: Crash")
                cv2.rectangle(img, (self.coord_crash[0,0], self.coord_crash[0,1]), (self.coord_crash[1,0], self.coord_crash[1,1]), self.drum_color_2, 2)
                cv2.putText(img, "CRASH", (self.coord_crash[2,0], self.coord_crash[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.drum_color_2, 2)

                if self.ifDrumSoundsOn:
                    self.drum_crash.play()

            elif (self.new_pt[item_num, 1] <= self.grid_y2):
                #logger.debug("[DETECT AREA]: Hi-hat")
                cv2.rectangle(img, (self.coord_hihat[0,0], self.coord_hihat[0,1]), (self.coord_hihat[1,0], self.coord_hihat[1,1]), self.drum_color_2, 2)
                cv2.putText(img, "HIHAT", (self.coord_hihat[2,0], self.coord_hihat[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.drum_color_2, 2)

                if self.ifDrumSoundsOn:
                    self.drum_hihat.play()
            else:
                #logger.debug("[DETECT AREA]: Snare")
                cv2.rectangle(img, (self.coord_snare[0,0], self.coord_snare[0,1]), (self.coord_snare[1,0], self.coord_snare[1,1]), self.drum_color_2, 2)
                cv2.putText(img, "SNARE", (self.coord_snare[2,0], self.coord_snare[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.drum_color_2, 2)

                if self.ifDrumSoundsOn:
                    self.drum_snare.play()

        elif (self.new_pt[item_num, 0] <= self.grid_x2):
            # 2nd Column
            if (self.new_pt[item_num, 1] <= self.grid_y2):
                #logger.debug("[DETECT AREA]: Tom1")
                cv2.rectangle(img, (self.coord_tom1[0,0], self.coord_tom1[0,1]), (self.coord_tom1[1,0], self.coord_tom1[1,1]), self.drum_color_2, 2)
                cv2.putText(img, "TOM1", (self.coord_tom1[2,0], self.coord_tom1[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.drum_color_2, 2)

                if self.ifDrumSoundsOn:
                    self.drum_tom1.play()

        else:
            if (self.new_pt[item_num, 1] <= self.grid_y1):
                #logger.debug("[DETECT AREA]: Ride")
                cv2.rectangle(img, (self.coord_ride[0,0], self.coord_ride[0,1]), (self.coord_ride[1,0], self.coord_ride[1,1]), self.drum_color_2, 2)
                cv2.putText(img, "RIDE", (self.coord_ride[2,0], self.coord_ride[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.drum_color_2, 2)

                if self.ifDrumSoundsOn:
                    self.drum_ride.play()

            elif (self.new_pt[item_num, 1] <= self.grid_y2):
                #logger.debug("[DETECT AREA]: Tom2")
                cv2.rectangle(img, (self.coord_tom2[0,0], self.coord_tom2[0,1]), (self.coord_tom2[1,0], self.coord_tom2[1,1]), self.drum_color_2, 2)
                cv2.putText(img, "TOM2", (self.coord_tom2[2,0], self.coord_tom2[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.drum_color_2, 2)

                if self.ifDrumSoundsOn:
                    self.drum_tom2.play()
            else:
                #logger.debug("[DETECT AREA]: Floor")
                cv2.rectangle(img, (self.coord_floor[0,0], self.coord_floor[0,1]), (self.coord_floor[1,0], self.coord_floor[1,1]), self.drum_color_2, 2)
                cv2.putText(img, "FLOOR", (self.coord_floor[2,0], self.coord_floor[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.drum_color_2, 2)

                if self.ifDrumSoundsOn:
                    self.drum_floor.play()




    def detectTriggerThruArea(self, img, item_num):
        '''
            Detect trigger thru lower half and upper half of each area
            0 - Left, 1 - Right, 2 - Bass

            If previous point was from the upper half of the area, and new pt is in lower half
            Means strike
        '''



        if (self.new_pt[item_num, 0] == 0) and (self.new_pt[item_num, 1] == 0):
            return



        mod_prev_pt = None
        if (self.prev_pt[item_num, 0] == 0) and (self.prev_pt[item_num,1] == 0):
            if (self.prev_pt_2[item_num, 0] == 0) and (self.prev_pt_2[item_num,1] == 0):
                return
            else:
                mod_prev_pt = self.prev_pt_2
        else:
            mod_prev_pt = self.prev_pt


        # Check for left and right sticks
        # For first column
        if (self.new_pt[item_num, 0] <= self.grid_x1):
            if (self.new_pt[item_num, 1] <= self.grid_y1) and (self.new_pt[item_num, 1] >= self.grid_y1_5):
                if ((mod_prev_pt[item_num, 1]<= self.grid_y1_5)):
                    #logger.debug("[DETECT AREA]: Crash")
                    cv2.rectangle(img, (self.coord_crash[0,0], self.coord_crash[0,1]), (self.coord_crash[1,0], self.coord_crash[1,1]), self.drum_color_2, 2)
                    cv2.putText(img, "CRASH", (self.coord_crash[2,0], self.coord_crash[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.drum_color_2, 2)
                    self.num_hits = self.num_hits + 1
                    if self.ifDrumSoundsOn:
                        self.drum_crash.play()

            elif (self.new_pt[item_num, 1] <= self.grid_y2) and (self.new_pt[item_num, 1] >= self.grid_y2_5):
                if ((mod_prev_pt[item_num, 1]<= self.grid_y2_5) and (mod_prev_pt[item_num, 1] >= self.grid_y1_5)):

                    #logger.debug("[DETECT AREA]: Hi-hat")
                    cv2.rectangle(img, (self.coord_hihat[0,0], self.coord_hihat[0,1]), (self.coord_hihat[1,0], self.coord_hihat[1,1]), self.drum_color_2, 2)
                    cv2.putText(img, "HIHAT", (self.coord_hihat[2,0], self.coord_hihat[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.drum_color_2, 2)
                    self.num_hits = self.num_hits + 1
                    if self.ifDrumSoundsOn:
                        self.drum_hihat.play()
            elif (self.new_pt[item_num, 1] <= self.frame_height) and (self.new_pt[item_num, 1] >= self.grid_y3_5):
                if ((mod_prev_pt[item_num, 1]<= self.grid_y3_5) and (mod_prev_pt[item_num, 1] >= self.grid_y2_5)):

                    #logger.debug("[DETECT AREA]: Snare")
                    #logger.debug("prev_pt: {}".format(mod_prev_pt[item_num]))
                    #logger.debug("new_pt: {}".format(self.new_pt[item_num]))

                    cv2.rectangle(img, (self.coord_snare[0,0], self.coord_snare[0,1]), (self.coord_snare[1,0], self.coord_snare[1,1]), self.drum_color_2, 2)
                    cv2.putText(img, "SNARE", (self.coord_snare[2,0], self.coord_snare[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.drum_color_2, 2)
                    self.num_hits = self.num_hits + 1
                    if self.ifDrumSoundsOn:
                        self.drum_snare.play()

        elif (self.new_pt[item_num, 0] <= self.grid_x2) and (self.new_pt[item_num,0] > self.grid_x1):
            # 2nd Column
            if (self.new_pt[item_num, 1] <= self.grid_y2) and (self.new_pt[item_num, 1] >= self.grid_y2_5):
                if ((mod_prev_pt[item_num, 1]<= self.grid_y2_5) and (mod_prev_pt[item_num, 1] >= self.grid_y1_5)):

                    #logger.debug("[DETECT AREA]: Tom1")
                    cv2.rectangle(img, (self.coord_tom1[0,0], self.coord_tom1[0,1]), (self.coord_tom1[1,0], self.coord_tom1[1,1]), self.drum_color_2, 2)
                    cv2.putText(img, "TOM1", (self.coord_tom1[2,0], self.coord_tom1[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.drum_color_2, 2)
                    self.num_hits = self.num_hits + 1
                    if self.ifDrumSoundsOn:
                        self.drum_tom1.play()

        elif (self.new_pt[item_num, 0] >= self.grid_x2):
            # for 3rd column
            if (self.new_pt[item_num, 1] <= self.grid_y1) and (self.new_pt[item_num, 1] >= self.grid_y1_5):
                if ((mod_prev_pt[item_num, 1]<= self.grid_y1_5)):

                    #logger.debug("[DETECT AREA]: Ride")
                    cv2.rectangle(img, (self.coord_ride[0,0], self.coord_ride[0,1]), (self.coord_ride[1,0], self.coord_ride[1,1]), self.drum_color_2, 2)
                    cv2.putText(img, "RIDE", (self.coord_ride[2,0], self.coord_ride[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.drum_color_2, 2)
                    self.num_hits = self.num_hits + 1
                    if self.ifDrumSoundsOn:
                        self.drum_ride.play()

            elif (self.new_pt[item_num, 1] <= self.grid_y2) and (self.new_pt[item_num, 1] >= self.grid_y2_5):
                if ((mod_prev_pt[item_num, 1]<= self.grid_y2_5)):

                    #logger.debug("[DETECT AREA]: Tom2")
                    cv2.rectangle(img, (self.coord_tom2[0,0], self.coord_tom2[0,1]), (self.coord_tom2[1,0], self.coord_tom2[1,1]), self.drum_color_2, 2)
                    cv2.putText(img, "TOM2", (self.coord_tom2[2,0], self.coord_tom2[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.drum_color_2, 2)
                    self.num_hits = self.num_hits + 1
                    if self.ifDrumSoundsOn:
                        self.drum_tom2.play()
            elif (self.new_pt[item_num, 1] <= self.frame_height) and (self.new_pt[item_num, 1] >= self.grid_y3_5):
                if ((mod_prev_pt[item_num, 1]<= self.grid_y3_5)):

                    #logger.debug("[DETECT AREA]: Floor")
                    cv2.rectangle(img, (self.coord_floor[0,0], self.coord_floor[0,1]), (self.coord_floor[1,0], self.coord_floor[1,1]), self.drum_color_2, 2)
                    cv2.putText(img, "FLOOR", (self.coord_floor[2,0], self.coord_floor[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.drum_color_2, 2)
                    self.num_hits = self.num_hits + 1
                    if self.ifDrumSoundsOn:
                        self.drum_floor.play()


    def detectBassTrigger(self, img, NUM_ITEMS, item_num):
        '''
            Case for detecting if bass was triggered
        '''

        #logger.debug("[DETECT BASS TRIGGER]")

        if (NUM_ITEMS == 3):
            item_num = 2


            self.calculateDynamics(img, item_num)
            if (self.accelerations[item_num] < -4000)  and (self.dir_vertical[item_num] > 0) and (self.flags[item_num] < 0):
                #print('acceleration: %.2f'%self.accelerations[item_num])
                #logger.debug('Acceleration: {} pixels/second'.format(self.accelerations[item_num]))
                self.flags[item_num] = 5

                # Detect which area was triggered
                #self.detectArea(img,item_num)

                # Check if bass area was triggered
                if (self.new_pt[item_num, 0] <= self.coord_bass[1,0]) and (self.new_pt[item_num,0] >= self.coord_bass[0, 0]) and (self.new_pt[item_num, 1] <= self.coord_bass[1,1]) and (self.new_pt[item_num, 1] >= self.coord_bass[0, 1]):
                    #logger.debug("[DETECT AREA]: Bass")
                    cv2.rectangle(img, (self.coord_bass[0,0], self.coord_bass[0,1]), (self.coord_bass[1,0], self.coord_bass[1,1]), self.drum_color_2, 2)
                    cv2.putText(img, "BASS", (self.coord_bass[2,0], self.coord_bass[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.drum_color_2, 2)

                    self.num_hits = self.num_hits + 1
                    if self.ifDrumSoundsOn:
                        self.drum_bass.play()
        else:


            if (self.new_pt[item_num, 0] == 0) and (self.new_pt[item_num, 1] == 0):
                return

            mod_prev_pt = None
            if (self.prev_pt[item_num, 0] == 0) and (self.prev_pt[item_num,1] == 0):
                if (self.prev_pt_2[item_num, 0] == 0) and (self.prev_pt_2[item_num,1] == 0):
                    return
                else:
                    mod_prev_pt = self.prev_pt_2
            else:
                mod_prev_pt = self.prev_pt

            #    elif (self.new_pt[item_num, 1] <= self.frame_height) and (self.new_pt[item_num, 1] >= self.grid_y3_5):
            if (self.new_pt[item_num, 0] <= self.grid_x2) and (self.new_pt[item_num,0] > self.grid_x1):

                # 2nd Column
                if (self.new_pt[item_num, 1] <= self.frame_height) and (self.new_pt[item_num, 1] >= self.grid_y3_5):

                    if ((mod_prev_pt[item_num, 1]<= self.grid_y3_5) and (mod_prev_pt[item_num, 1] >= self.grid_y2_5)):

                        #logger.debug("[DETECT AREA]: Bass")
                        cv2.rectangle(img, (self.coord_bass[0,0], self.coord_bass[0,1]), (self.coord_bass[1,0], self.coord_bass[1,1]), self.drum_color_2, 2)
                        cv2.putText(img, "BASS", (self.coord_bass[2,0], self.coord_bass[2,1]),cv2.FONT_HERSHEY_SIMPLEX, 0.5, self.drum_color_2, 2)

                        if self.ifDrumSoundsOn:
                            self.drum_bass.play()



if __name__ == '__main__':
    drums = AirDrums()
    # Comment out below line to remove drum sounds
    drums.init_drum_sounds()
    # 2 - for two sticks
    # 3 - for two sticks, and bass
    drums.init_calibrate(2)
    drums.playDrums()
