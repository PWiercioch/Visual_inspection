from Utils import *
import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":
    path_to_pic = r'pictures/hex_10.jpg'

    pic = plt.imread(path_to_pic)

    plt.figure()
    plt.imshow(pic)
