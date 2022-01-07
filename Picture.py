import numpy as np
import matplotlib.pyplot as plt
import cv2
import random


class Picture:
    def __init__(self, path, dim, thershold_lower=130, threshold_upper=255, sigma=0, blurr_intensity=3):
        self._original = cv2.imread(path, cv2.IMREAD_COLOR)
        self._original = cv2.resize(self._original, dim, interpolation=cv2.INTER_AREA)

        # Load Aruco detector
        self.parameters = cv2.aruco.DetectorParameters_create()
        self.aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)

        self.aruco_perimeter = self.detect_aruco()
        self.pixel_cm_ratio = self.aruco_perimeter / 20

        self.greyscale = cv2.cvtColor(self._original, cv2.COLOR_BGR2GRAY)
        self.blurred = cv2.GaussianBlur(self.greyscale, (blurr_intensity, blurr_intensity), sigmaX=sigma, sigmaY=sigma)
        self.empty = np.zeros(np.shape(self._original))

        ret, self.thresh = cv2.threshold(self.greyscale, thershold_lower, threshold_upper, cv2.THRESH_BINARY)



    def detect_aruco(self):
        # Get Aruco marker
        corners, _, _ = cv2.aruco.detectMarkers(self._original, self.aruco_dict, parameters=self.parameters)

        # Draw polygon around the marker
        int_corners = np.int0(corners)
        cv2.polylines(self._original, int_corners, True, (0, 255, 0), 5)

        # Aruco Perimeter
        try:
            ratio = cv2.arcLength(corners[0], True)
        except:
            ratio = 1

        return ratio

    def show_original(self):
        cv2.imshow('Original image', self._original)

    def show_blurred(self):
        cv2.imshow('Blurred image', self.blurred)

    def show_greyscale(self):
        cv2.imshow('Greyscale image', self.greyscale)

    def show_threshold(self):
        cv2.imshow('Threshold image', self.thresh)

    def show_sobel_edges(self):
        cv2.imshow('Sobel edge detection in X direction', self.sobelx)
        cv2.imshow('Sobel edge detection in Y direction', self.sobely)
        cv2.imshow('Sobel edge detection in both directions', self.sobelxy)

    def show_canny_edges(self):
        cv2.imshow('Canny edge detection', self.canny)

    def show_contours(self):
        image_copy = self.empty.copy()
        cv2.drawContours(image=image_copy, contours=self.contours, contourIdx=-1, color=(0, 255, 0), thickness=2,
                         lineType=cv2.LINE_AA)
        cv2.imshow('Contours', image_copy)

    def show_contour_points(self, base_image, contour_image, size=None):
        image_copy3 = base_image.copy()
        for i, contour in enumerate(contour_image):# loop over one contour area
            if size:
                if contour.shape[0] == size:
                    for j, contour_point in enumerate(contour):  # loop over the points
                        cv2.circle(image_copy3, ((contour_point[0][0], contour_point[0][1])), 2, (0, 255, 0), 2, cv2.LINE_AA)
            else:
                for j, contour_point in enumerate(contour):  # loop over the points
                    # draw a circle on the current contour coordinate
                    cv2.circle(image_copy3, ((contour_point[0][0], contour_point[0][1])), 2, (0, 255, 0), 2, cv2.LINE_AA)


        # see the results
        cv2.imshow('CHAIN_APPROX_SIMPLE Point only', image_copy3)


    def sobel_edges(self, d=1, size=3):
        self.sobelx = cv2.Sobel(src=self.blurred, ddepth=cv2.CV_64F, dx=d, dy=0, ksize=size)
        self.sobely = cv2.Sobel(src=self.blurred, ddepth=cv2.CV_64F, dx=0, dy=d, ksize=size)
        self.sobelxy = cv2.Sobel(src=self.blurred, ddepth=cv2.CV_64F, dx=d, dy=d, ksize=size)

        self.sobel_converted = self.convert_2_channels_to_grayscale(self.sobelxy)

    def canny_edges(self, img, t1, t2):
        self.canny = cv2.Canny(image=img, threshold1=t1, threshold2=t2)

    def convert_2_channels_to_grayscale(self, img):
        max = img.max()
        min = img.min()
        mean = (max+min)/2
        delta = (max-min)/2
        output = np.zeros((np.shape(img)[0],np.shape(img)[1],3))

        for r_i, row in enumerate(img):
            for p_i, pixel in enumerate(row):
                val = (1 + (pixel-mean)/delta)/2
                output[r_i,p_i] = [val, val, val]

        return output


    def get_contours(self, img, m='simple'):
        if m == 'none':
            method = cv2.CHAIN_APPROX_NONE
        elif m == 'simple':
            method = cv2.CHAIN_APPROX_SIMPLE

        self.contours, self.hierarchy = cv2.findContours(image=img, mode=cv2.RETR_EXTERNAL, method=method)
