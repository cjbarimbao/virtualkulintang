import cv2
import numpy as np
import time
import datetime

"""
program: image segmentation using rg chromaticity + blob detection + hit detection
change log:
    04/15/23 @ initialization: increasing frame width to accomodate gongs
    04/15/23 @ main detection: downsampling included to minimize lag during detection while accomodating increase in width
    05/02/23 @ image segmentation: modified segmentation using histogram backprojection
    05/07/23 @ blob detection: working centroid detection using numpy where and average on pixels with maximum histogram values
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

        self.BINS = 32


    def calibration(self):
        self.cam = cv2.VideoCapture(0)
        frame_center = (int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH)/2), int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT)/2))
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH,self.frame_width)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT,self.frame_height)
        j = 0
        for i in range(self.total_markers):
            while True:
                ret_val, frame = self.cam.read()
                if j == 0:
                    j = j + 1
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
        g_int_append = np.append(self.patch_g_int[0].flatten(), self.patch_g_int[1].flatten())
        r_int_append = np.append(self.patch_r_int[0].flatten(), self.patch_r_int[1].flatten())
        self.hmatrix, _, _ = np.histogram2d(g_int_append, r_int_append, bins = self.BINS, range = [[0,self.BINS-1],[0,self.BINS-1]])
        self.hmatrix_g = np.tril(self.hmatrix)
        self.hmatrix_r = np.triu(self.hmatrix)
        self.hmatrix1d = self.hmatrix.flatten()
        self.hmatrix_g1d = self.hmatrix_g.flatten()
        self.hmatrix_r1d = self.hmatrix_r.flatten()
        # save histogram matrix and r g values of the patch (in integer form)
        """ with open('calibration.npy', 'wb') as f:
            np.save(f, self.hmatrix)
            np.save(f, self.hmatrix_g)
            np.save(f, self.hmatrix_r)
            np.save(f, self.patch_g_int[0])
            np.save(f, self.patch_r_int[0])
            np.save(f, self.patch_g_int[1])
            np.save(f, self.patch_r_int[1]) """


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
        return cv2.resize(frame, res, interpolation = cv2.INTER_NEAREST)


    def image_segmentation(self, frame):
        """
        image_segmentation(frame)

        Returns the backprojection of the frame using the histogram matrix

        Parameters
        ----------
        frame : the downsampled RGB frame

        Returns
        -------
        bp_g : ndarray
            An array representation of the frame's backprojection on the green channel
        bp_r : ndarray
            AN array representation of the frame's backprojection on the red channel
        """

        np.seterr(invalid='ignore')
        I = frame.sum(axis=2)
        I[I == 0] = 100000

        self.frame_r = frame[:,:,2] / I
        self.frame_g = frame[:,:,1] / I
        
        frame_r_int = (self.frame_r*(self.BINS-1)).astype(int)
        frame_g_int = (self.frame_g*(self.BINS-1)).astype(int)

        bp_g = self.hmatrix_g1d[frame_g_int.flatten()*self.BINS + frame_r_int.flatten()].reshape(self.frame_r.shape)
        bp_r = self.hmatrix_r1d[frame_g_int.flatten()*self.BINS + frame_r_int.flatten()].reshape(self.frame_r.shape)

        self.masked_r = cv2.bitwise_and(frame, frame, mask = bp_r.astype(np.uint8))
        self.masked_g = cv2.bitwise_and(frame, frame, mask = bp_g.astype(np.uint8))
        
        return bp_g, bp_r


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
            An array representation of the centroid of the blob (y,x) 
            where y is the row and x is the column location in the original frame
        """
        
        center = [0,0]

        indices = np.where(frame == np.amax(frame))
        center[0] = indices[0].mean()
        center[1] = indices[1].mean()

        center = np.array(center, dtype=np.uint16) 

        return center
    
    def disp_centroid(self, frame, Cr, Cg):
        # draw centroid
        cv2.circle(frame, (Cr[1], Cr[0]), 5, (255, 0, 0), -1)
        cv2.putText(frame, "centroid", (Cr[1] - 25, Cr[0] - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        cv2.circle(frame, (Cg[1], Cg[0]), 5, (255, 0, 0), -1)
        cv2.putText(frame, "centroid", (Cg[1] - 25, Cg[0] - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        return frame

    def main_detection(self):
        ''' Main Code '''
        t = []
        i = 0
        while True:
            
            start = time.time()
            ret_val, frame = self.cam.read()
            frame = self.downsample(frame)
            frame = cv2.flip(frame, 1)
            bp_g, bp_r = self.image_segmentation(frame)
            #-------- blob detection ---------
            
            centroid_r = self.blob_detection(bp_r)
            centroid_g = self.blob_detection(bp_g)
            end = time.time()
            t.append(end - start)
            
            #----- display detected blob -----
            if (centroid_r.size != 0 and centroid_g.size != 0):
                try:
                    frame = self.disp_centroid(frame, centroid_r, centroid_g)
                except: 
                    print(centroid_r, centroid_g)
            
            #display = np.concatenate((frame, numpy_mask), axis = 0)

            title = "Numpy Detection"
            cv2.namedWindow(title, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(title, int(self.frame_width), int(self.frame_height))
            cv2.imshow(title, frame)

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
        print("Average numpy where + mean execution time: {0:.2f} milliseconds".format(avg_t*1000))
        print("Average frame rate: ", 1/avg_t)


if __name__ == '__main__':
    start = segmentation()
    start.calibration()
    start.main_detection()
