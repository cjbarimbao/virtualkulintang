import cv2
import numpy as np
import time
import datetime
import pandas as pd

"""
program: image segmentation using rg chromaticity + blob detection + hit detection
change log:
    04/15/23 @ initialization: increasing frame width to accomodate gongs
    04/15/23 @ main detection: downsampling included to minimize lag during detection while accomodating increase in width
    05/02/23 @ image segmentation: modified segmentation using histogram backprojection
"""

class segmentation(object):
    def __init__(self):
        self.frame_width = 854
        self.frame_height = 480
        self.pixel_width = 427
        self.pixel_height = 240
        self.center = (int(self.pixel_width/2), int(self.pixel_height/2))
        self.radius = 100
        self.diameter = int(2*self.radius)
        self.label = ("Left", "Right")

        self.center_color = (255, 0, 0)
        self.bound_color = (0, 255, 0)
        self.detection_point = np.array([[0, 0], [0, 0]])
        #self.dp_update_0 = False
        #self.dp_update_1 = False

        self.patch_size = 30
        self.patch_half = int(self.patch_size/2)
        self.patch_retrieved = False

        self.cam = None
        self.total_markers = 2
        
        self.patch = [np.zeros((30,30,3)), np.zeros((30,30,3))]
        self.patch = np.array(self.patch)
        self.patch_r = [np.zeros((30,30)), np.zeros((30,30))]
        self.patch_r = np.array(self.patch_r)
        self.patch_g = [np.zeros((30,30)), np.zeros((30,30))]
        self.patch_g = np.array(self.patch_g)
        self.patch_r_int = [np.zeros((30,30)), np.zeros((30,30))]
        self.patch_g_int = [np.zeros((30,30)), np.zeros((30,30))]

        #self.masked = [np.zeros((self.frame_height,self.frame_width,3)), np.zeros((self.frame_height,self.frame_width,3))]
        #self.masked = np.array(self.masked)
        #self.frame_r = [np.zeros((self.frame_height,self.frame_width)), np.zeros((self.frame_height,self.frame_width))]
        #self.frame_r = np.array(self.frame_r)
        #self.frame_g = [np.zeros((self.frame_height,self.frame_width)), np.zeros((self.frame_height,self.frame_width))]
        #self.frame_g = np.array(self.frame_g)

        self.bins = 32
        #self.hmatrix = np.zeros((self.bins, self.bins), dtype = 'int')
        #self.hmatrix1d = np.zeros((self.bins*self.bins), dtype = 'int')

    def frame_subtraction(self, prev_frame, current_frame):
        # get the green channel of the current frame and subtract the green channel of the previous frame
        # return the difference image
        prev = prev_frame[:,:,1]
        curr = current_frame[:,:,1]

        return cv2.subtract(curr,prev)
    
    def downsample(self, frame):
        '''
        reduce resolution
        '''
        res = (self.pixel_width, self.pixel_height)
        return cv2.resize(frame, res, interpolation = cv2.INTER_NEAREST)
    
    def main_detection(self):
        t = []
        self.cam = cv2.VideoCapture(0)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH,self.frame_width)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT,self.frame_height)
        while True:    
            start = time.time()
            _, prev_frame = self.cam.read()
            _, current_frame = self.cam.read()
            prev_frame = self.downsample(prev_frame)
            current_frame = self.downsample(current_frame)
            prev_frame = cv2.flip(prev_frame, 1)
            current_frame = cv2.flip(current_frame, 1)
            result = self.frame_subtraction(prev_frame, current_frame)
            masked = cv2.bitwise_and(current_frame, current_frame, mask = result)
            end = time.time()
            t.append(end-start)
            #disp_res = np.array(np.zeros(current_frame.shape))
            #disp_res[:,:,1] = result
            title = "Frame Subtraction"
            display = np.concatenate((current_frame, masked), axis = 0)
            cv2.namedWindow(title, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(title, self.frame_width, self.frame_height*2)
            cv2.imshow(title, display)

            if cv2.waitKey(1) == 27:
                break

        self.cam.release()
        cv2.destroyAllWindows()
        print("Quitting Detection...")
        # print average execution time
        avg_t = sum(t)/len(t)
        now = datetime.datetime.now()
        print(now.strftime("%Y-%m-%d %H:%M:%S"))
        print("Average execution time: {0:.2f} milliseconds".format(avg_t*1000))
        print("Average frame rate: ", 1/avg_t)


if __name__ == '__main__':
    start = segmentation()
    start.main_detection()

