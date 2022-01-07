import cv2
from confidentials import CAM_ADDRES


video = cv2.VideoCapture(0)
video.open(CAM_ADDRES)

while True:
    check, frame = video.read()

    resized_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    cv2.imshow("Video", resized_frame)

    # Press q to quit
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

video.release()
cv2.destroyAllWindows()