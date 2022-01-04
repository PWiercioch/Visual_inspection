import numpy as np
import matplotlib.pyplot as plt
import cv2
import random


class Picture:
    def __init__(self, path, dim, blurr_intensity=3):
        self._original = cv2.imread(path, cv2.IMREAD_COLOR)
        self._original = cv2.resize(self._original, dim, interpolation=cv2.INTER_AREA)
        self.greyscale = cv2.cvtColor(self._original, cv2.COLOR_BGR2GRAY)
        self.blurred = cv2.GaussianBlur(self.greyscale, (blurr_intensity, blurr_intensity), sigmaX=0, sigmaY=0)
        self.empty = np.zeros(np.shape(self._original))

        ret, self.thresh = cv2.threshold(self.greyscale, 150, 255, cv2.THRESH_BINARY)

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
        cv2.imshow('None approximation', image_copy)

    def show_contour_points(self, base_image, contour_image):
        image_copy3 = base_image.copy()
        for i, contour in enumerate(contour_image):  # loop over one contour area
            for j, contour_point in enumerate(contour):  # loop over the points
                # draw a circle on the current contour coordinate
                cv2.circle(image_copy3, ((contour_point[0][0], contour_point[0][1])), 2, (0, 255, 0), 2, cv2.LINE_AA)


        # see the results
        cv2.imshow('CHAIN_APPROX_SIMPLE Point only', image_copy3)


    def sobel_edges(self):
        self.sobelx = cv2.Sobel(src=self.blurred, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=3)
        self.sobely = cv2.Sobel(src=self.blurred, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=3)
        self.sobelxy = cv2.Sobel(src=self.blurred, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=3)

    def canny_edges(self, t1, t2):
        self.canny = cv2.Canny(image=self.blurred, threshold1=t1, threshold2=t2)

    def get_contours(self, img, m='simple'):
        if m == 'none':
            method = cv2.CHAIN_APPROX_NONE
        elif m == 'simple':
            method = cv2.CHAIN_APPROX_SIMPLE

        self.contours, self.hierarchy = cv2.findContours(image=img, mode=cv2.RETR_TREE, method=method)
