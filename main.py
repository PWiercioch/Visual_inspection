from Picture import *


if __name__ == "__main__":
    picture = Picture(r'pictures/top_2.jpg', (300, 300), blurr_intensity=3)

    picture.show_original()
    # picture.show_blurred()

    picture.sobel_edges()
    picture.canny_edges(120, 220)

    picture.get_contours(picture.canny)

    # picture.show_sobel_edges()
    picture.show_canny_edges()

    picture.show_greyscale()
    picture.show_threshold()
    picture.show_contours()

    picture.show_contour_points(picture._original, (picture.contours[15],))
