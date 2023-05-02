import cv2
import numpy as np
import time

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
        self.pixel_width = 854
        self.pixel_height = 480
        self.center = (int(self.pixel_width/2), int(self.pixel_height/2))
        self.radius = 59
        self.diameter = int(2*self.radius)
        self.label = ("Left", "Right")

        self.center_color = (255, 0, 0)
        self.bound_color = (0, 255, 0)
        self.detection_point = np.array([[0, 0], [0, 0]])
        self.dp_update_0 = False
        self.dp_update_1 = False

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

        self.masked = [np.zeros((480,854,3)), np.zeros((480,854,3))]
        self.masked = np.array(self.masked)
        self.frame_r = [np.zeros((480,854)), np.zeros((480,854))]
        self.frame_r = np.array(self.frame_r)
        self.frame_g = [np.zeros((480,854)), np.zeros((480,854))]
        self.frame_g = np.array(self.frame_g)

        self.bins = 32
        self.hmatrix = np.zeros((self.bins, self.bins), dtype = 'int')
        self.hmatrix1d = np.zeros((self.bins*self.bins), dtype = 'int')


    def calibration(self):
        self.cam = cv2.VideoCapture(0)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH,self.frame_width)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT,self.frame_height)

        for i in range(self.total_markers):
            while True:
                ret_val, frame = self.cam.read()
                mirrored = cv2.flip(frame, 1)
                mirrored = self.downsample(mirrored)
                image = cv2.circle(mirrored, self.center, self.radius + 1, self.center_color, 1)

                if i == 0:
                    title = "Calibration: Left"
                elif i == 1:
                    title = "Calibration: Right"
                cv2.namedWindow(title, cv2.WINDOW_NORMAL)
                cv2.resizeWindow(title, self.frame_width, self.frame_height)
                cv2.setMouseCallback(title, self.retrieve_patch, [mirrored, i])
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
        self.hmatrix, _, _ = np.histogram2d(g_int_append, r_int_append, bins = self.bins, range = [[0,self.bins],[0,self.bins]])
        self.hmatrix1d = self.hmatrix.flatten()


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
            self.patch_r_int[marker] = (self.patch_r[marker]*(self.bins-1)).astype(int)
            self.patch_g_int[marker] = (self.patch_g[marker]*(self.bins-1)).astype(int)

            self.patch_retrieved = True
             

    def downsample(self, frame):
        '''
        reduce resolution
        '''
        res = (854, 480)
        return cv2.resize(frame, res, interpolation = cv2.INTER_AREA)


    def image_segmentation(self, frame, marker_num, mean = 1, std = 1):

        # RG chromaticity of frame
        np.seterr(invalid='ignore')
        I = frame.sum(axis=2)
        I[I == 0] = 100000

        self.frame_r = frame[:,:,2] / I
        self.frame_g = frame[:,:,1] / I
        
        frame_r_int = (self.frame_r*(self.bins-1)).astype(int)
        frame_g_int = (self.frame_g*(self.bins-1)).astype(int)

        back_projection = np.zeros(self.frame_r.shape, dtype = 'uint8')
        back_projection = self.hmatrix1d[frame_g_int.flatten()*self.bins + frame_r_int.flatten()].reshape(self.frame_r.shape).astype(np.uint8)

        self.masked = cv2.bitwise_and(frame, frame, mask = back_projection)

        return back_projection


    def blob_detection(self, frame, masked, mask, marker_num):
        self.dp_update = False

        # Blob Detection
        kernel = np.ones((10,10),np.uint8)
        dilation = cv2.erode(mask, kernel, iterations = 1)
        image, contours, hierarchy = cv2.findContours(dilation,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        # Approximate contours to polygons + get bounding circles
        contours_poly = [None]*len(contours)
        centers = [None]*len(contours)
        radius = [None]*len(contours)
        for i, c in enumerate(contours):
            contours_poly[i] = cv2.approxPolyDP(c, 3, True)
            centers[i], radius[i] = cv2.minEnclosingCircle(contours_poly[i])

        # Find bounding circle for the marker (usually largest)
        centers = np.array(centers)
        radius = np.array(radius)
        if radius.size != 0:
            if radius.max() >= 20 and radius.max() < 200:
                max_index = np.where(radius == radius.max())
                #print(max_index)
                max = int(max_index[0][0])

                dp_x = int(centers[max][0])
                dp_y = int(centers[max][1] + radius[max])

                self.detection_point[marker_num, 0] = dp_x
                self.detection_point[marker_num, 1] = dp_y
                self.dp_update = True

        # Draw polygonal contour, bounding circles, and detection point
        if centers.size != 0:
            if self.dp_update == True:
                #cv2.drawContours(masked, contours_poly, max, self.bound_color)
                #cv2.circle(masked, (int(centers[max][0]), int(centers[max][1])), int(radius[max]), self.bound_color, 1)
                cv2.circle(frame, (int(centers[max][0]), int(centers[max][1])), int(radius[max]), self.bound_color, 1)
                cv2.circle(frame, (dp_x, dp_y), 5, self.center_color, -5)
                cv2.putText(frame, self.label[marker_num], (dp_x, dp_y + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)


    def main_detection(self):
        ''' Main Code '''
        i = 0
        while True:
            ret_val, frame = self.cam.read()
            frame = cv2.flip(frame, 1)

            start = time.time()

            frame = self.downsample(frame)

            mask = self.image_segmentation(frame, 0)
            for i in range(self.total_markers):
            #    mask = self.image_segmentation(frame, i)
                self.blob_detection(frame, self.masked[i], mask, i)

            end = time.time()

            print(end - start)


            display = np.concatenate((frame, self.masked), axis = 0)

            title = "Main Detection"
            cv2.namedWindow(title, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(title, self.frame_width, int(self.frame_height*2))
            #cv2.resizeWindow(title, self.frame_width, self.frame_height)
            cv2.imshow(title, display)
            #cv2.imshow(title, frame)

            if cv2.waitKey(1) == 27:
                break

        self.cam.release()
        cv2.destroyAllWindows()
        print("Quitting Detection...")



if __name__ == '__main__':
    start = segmentation()
    start.calibration()
    start.main_detection()
