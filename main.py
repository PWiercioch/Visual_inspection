from Detector import *
from Device import *
from confidentials import CAM_ADDRES
import pyinputplus


if __name__ == "__main__":
    device = pyinputplus.inputMenu(['Image', 'Camera', 'Or quit'], prompt='Select input device\n', default='Or quit', limit=3)

    # device = 'Image'

    if device == 'Or quit':
        Device.close()
    elif device == 'Image':
        device = Image(1.3, r'pictures/regular_shapes/aruco_test.jpg')
    elif device =='Camera':
        device = Camera(0.5, CAM_ADDRES)

    detector = Detector(device)

    while True:
        detector.pre_process_image(device.get_image())
        detector.get_contours(detector.thresh)
        detector.show_contours()
        detector.measure()

        device.display()
        key = cv2.waitKey(device.wait_time)
        if device.close_condition(key):
            break

    Device.close()

    # picture = Detector(r'pictures/regular_shapes/black_1.jpg', (500, 500), blurr_intensity=9)
    #
    # picture.sobel_edges()
    # picture.canny_edges(picture.thresh, 120, 220)
    #
    # picture.get_contours(picture.canny)
    #
    # picture.show_contour_points(picture.empty, picture.contours)
    #
    # print(f'Found {len(picture.contours)} contour \nFitrst one with with {picture.contours[0].shape[0]} points')
    #
    # for cnt in picture.contours:
    #     # Get rect
    #     rect = cv2.minAreaRect(cnt)
    #     (x, y), (w, h), angle = rect
    #
    #     # Calculate dimensions
    #     object_width = w / picture.pixel_cm_ratio
    #     object_height = h / picture.pixel_cm_ratio
    #
    #     # Display rectangle
    #     box = cv2.boxPoints(rect)
    #     box = np.int0(box)
    #     cv2.circle(picture._original, (int(x), int(y)), 5, (0, 0, 255), -1)
    #     cv2.polylines(picture._original, [box], True, (255, 0, 0), 2)
    #
    #     # Display dimensions
    #     cv2.putText(picture._original, "Width {} cm".format(round(object_width, 1)), (int(x - 50), int(y - 15)),
    #                 cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)
    #     cv2.putText(picture._original, "Height {} cm".format(round(object_height, 1)), (int(x - 50), int(y + 20)),
    #                 cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)
