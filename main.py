from Picture import *


if __name__ == "__main__":
    picture = Picture(r'pictures/regular_shapes/black_1.jpg', (500, 500), blurr_intensity=9)

    picture.show_original()
    # picture.show_blurred()

    picture.sobel_edges()
    picture.canny_edges(picture.thresh, 120, 220)

    picture.get_contours(picture.canny)

    # picture.show_sobel_edges()
    # picture.show_canny_edges()

    # picture.show_greyscale()
    # picture.show_threshold()
    # picture.show_contours()

    picture.show_contour_points(picture.empty, picture.contours)

    print(f'Found {len(picture.contours)} contour \nFitrst one with with {picture.contours[0].shape[0]} points')

    for cnt in picture.contours:
        # Get rect
        rect = cv2.minAreaRect(cnt)
        (x, y), (w, h), angle = rect

        # Calculate dimensions
        object_width = w / picture.pixel_cm_ratio
        object_height = h / picture.pixel_cm_ratio

        # Display rectangle
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.circle(picture._original, (int(x), int(y)), 5, (0, 0, 255), -1)
        cv2.polylines(picture._original, [box], True, (255, 0, 0), 2)

        # Display dimensions
        cv2.putText(picture._original, "Width {} cm".format(round(object_width, 1)), (int(x - 50), int(y - 15)),
                    cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)
        cv2.putText(picture._original, "Height {} cm".format(round(object_height, 1)), (int(x - 50), int(y + 20)),
                    cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 2)

    picture.show_original()