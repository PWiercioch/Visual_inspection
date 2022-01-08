import numpy as np
import cv2


class Detector:
    def __init__(self, device):
        self.device = device
        # Load Aruco detector
        self.parameters = cv2.aruco.DetectorParameters_create()
        self.aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)


    def measure(self):
        self.aruco_perimeter = self.detect_aruco()
        if self.aruco_perimeter:
            self.pixel_cm_ratio = self.aruco_perimeter / 20
            self.aruco_bool = True

            for cnt in self.contours:
                # Get rect
                rect = cv2.minAreaRect(cnt)
                (x, y), (w, h), angle = rect

                # Calculate dimensions
                object_width = w / self.pixel_cm_ratio
                object_height = h / self.pixel_cm_ratio

                # Display rectangle
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                cv2.circle(self.device.img, (int(x), int(y)), 5, (0, 0, 255), -1)
                cv2.polylines(self.device.img, [box], True, (255, 0, 0), 2)

                # Display dimensions
                cv2.putText(self.device.img, "Width {} cm".format(round(object_width, 1)), (int(x - 50), int(y - 15)),
                            cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)
                cv2.putText(self.device.img, "Height {} cm".format(round(object_height, 1)), (int(x - 50), int(y + 20)),
                            cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)


    def detect_aruco(self):
        # Get Aruco marker
        corners, _, _ = cv2.aruco.detectMarkers(self.device.img, self.aruco_dict, parameters=self.parameters)

        # Draw polygon around the marker
        int_corners = np.int0(corners)
        cv2.polylines(self.device.img, int_corners, True, (0, 255, 0), 5)

        # Aruco Perimeter
        if corners:
            return cv2.arcLength(corners[0], True)
        else:
            return None

    def get_contours(self):
        method = cv2.CHAIN_APPROX_SIMPLE

        self.contours, self.hierarchy = cv2.findContours(image=self.pre_processed_image, mode=cv2.RETR_EXTERNAL, method=method)

    def pre_process_image(self, img):
        greyscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.empty = np.zeros(np.shape(img))
        return greyscale

    def show_contours(self):
        image_copy = self.empty.copy()
        cv2.drawContours(image=image_copy, contours=self.contours, contourIdx=-1, color=(0, 255, 0), thickness=2,
                         lineType=cv2.LINE_AA)
        cv2.imshow('Contours', image_copy)

    def show_contour_points(self, base_image, contour_image):
        image_copy3 = base_image.copy()
        for i, contour in enumerate(contour_image):# loop over one contour area
            # assign random color - seems like it is not working
            color = tuple(np.random.choice(range(256), size=3).tolist())  # tolist() converts numpy int32 to regular python int - required by opencv
            print(color)
            for j, contour_point in enumerate(contour):  # loop over the points
                cv2.circle(image_copy3, ((contour_point[0][0], contour_point[0][1])), radius=1, color=color, thickness=3)

        # see the results
        cv2.imshow('CHAIN_APPROX_SIMPLE Point only', image_copy3)


class Threshold_Detector(Detector):
    def __init__(self, device, t1, t2):
        Detector.__init__(self, device)
        self.t1 = t1
        self.t2 = t2

    def pre_process_image(self, img):
        greyscale = Detector.pre_process_image(self, img)
        ret, self.pre_processed_image = cv2.threshold(greyscale, self.t1, self.t2, cv2.THRESH_BINARY)


class Canny_Detector(Detector):
    def __init__(self, device, blurr_intensity, sigma, t1, t2):
        Detector.__init__(self, device)
        self.blurr_intensity = blurr_intensity
        self.sigma = sigma
        self.t1 = t1
        self.t2 = t2

    def pre_process_image(self, img):
        greyscale = Detector.pre_process_image(self, img)
        blurred = cv2.GaussianBlur(greyscale, (self.blurr_intensity, self.blurr_intensity), sigmaX=self.sigma, sigmaY=self.sigma)
        self.pre_processed_image = cv2.Canny(image=blurred, threshold1=self.t1, threshold2=self.t2)



