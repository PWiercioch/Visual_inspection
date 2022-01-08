from Detector import *
from Device import *
from confidentials import CAM_ADDRES
import pyinputplus


if __name__ == "__main__":
    device = pyinputplus.inputMenu(['Image', 'Smartphone', 'Webcam', 'Or quit'], prompt='Select input device\n', default='Or quit', limit=3)

    if device == 'Or quit':
        Device.close()
    elif device == 'Image':
        device = Image(1.3, r'pictures/regular_shapes/white_5_aruco.jpg')
    elif device == 'Smartphone':
        device = Smartphone(0.75, CAM_ADDRES)
    elif device == 'Webcam':
        device = Webcam(1.2)

    while True:
        detector_type = pyinputplus.inputMenu(['None', 'Threshold', 'Canny'], prompt='Select detector type\n', default='None', limit=3)

        if detector_type == 'None':
            while True:
                device.get_image()
                device.display()
                key = cv2.waitKey(device.wait_time)
                if device.close_condition(key):
                    break
        else:
            if detector_type == 'Threshold':
                detector_params = input("Input detector paramters seperated by spaces:\nlower threshold\nUpper Threshold\nMethod: binary or inverse")
                detector_params = detector_params.split()
                detector = Threshold_Detector(device, int(detector_params[0]), int(detector_params[1]), detector_params[2])
            elif detector_type == 'Canny':
                detector_params = input("Input detector paramters seperated by spaces:\nBlur intensity\nBlur sigma\nlower threshold\nUpper Threshold")
                detector_params = detector_params.split()
                detector = Canny_Detector(device, int(detector_params[0]), int(detector_params[1]),
                                          int(detector_params[2]), int(detector_params[3]))

            print('\nPress q to quit')

            while True:
                detector.pre_process_image(device.get_image())
                cv2.imshow('Greyscale', detector.greyscale)
                cv2.imshow('Pre processed image', detector.pre_processed_image)
                detector.get_contours()
                detector.measure()
                detector.show_contours()

                device.display()
                key = cv2.waitKey(device.wait_time)
                if device.close_condition(key):
                    break

        decision = pyinputplus.inputYesNo('Choose different detector?')
        if decision =='no':
            break

    Device.close()
