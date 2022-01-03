import numpy as np
import matplotlib.pyplot as plt
import cv2


class Picture:
    def __init__(self, path, blurr_intensity=3):
        self._original = cv2.imread(path,flags=0)
        self.blurred = cv2.GaussianBlur(self._original, (blurr_intensity, blurr_intensity), sigmaX=0, sigmaY=0)

    def show_original(self):
        cv2.imshow('Original image', self._original)

    def show_blurred(self):
        cv2.imshow('Blurred image', self.blurred)

    def show_sobel_edges(self):
        cv2.imshow('Sobel edge detection in X direction', self.sobelx)
        cv2.imshow('Sobel edge detection in Y direction', self.sobely)
        cv2.imshow('Sobel edge detection in both directions', self.sobelxy)

    def show_canny_edges(self):
        cv2.imshow('Canny edge detection', self.canny)

    def sobel_edges(self):
        self.sobelx = cv2.Sobel(src=self.blurred, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=3)
        self.sobely = cv2.Sobel(src=self.blurred, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=3)
        self.sobelxy = cv2.Sobel(src=self.blurred, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=3)

    def canny_edges(self, t1, t2):
        self.canny = cv2.Canny(image=self.blurred, threshold1=t1, threshold2=t2)
