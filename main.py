from Picture import *


if __name__ == "__main__":
    picture = Picture(r'pictures/infill_1.jpg', blurr_intensity=3)

    picture.show_original()
    # picture.show_blurred()

    picture.sobel_edges()
    picture.canny_edges(100, 200)

    # picture.show_sobel_edges()
    picture.show_canny_edges()
