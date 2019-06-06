from skimage import *
import os
import numpy as np
import collections
import warnings
import matplotlib.pyplot as plt

# save_image(name, image)
# read_file(name)
# get_histogramm(image)
class image_service:
    def __init__(self):
        pass

    def save_image(self, name, image):
        PATH = './lab_1_pic/'

        if not os.path.isdir(PATH):
            os.makedirs(PATH)

        io.imsave(PATH + name, image)
        print('Save done')

    def read_file(self, name):
        return io.imread(name)

    def get_histogram(self, image):
        plt.hist(image.ravel(), bins = range(257))
        plt.xlim([0, 256])
        plt.show()

# FIRST TASK
class Lab2_first(image_service):
    def __init__(self):
        self.simple_image = self.read_file('simple.jpg')

    def call(self):
    	self.linear_stretch()


    def map_diff(self, image1, image2):
    	pass
    
    def linear_stretch(self):
    	k = round(self.simple_image.size * .05)
    	print(self.simple_image.ravel())
    	print(k)
    	pass

# SECOND TASK
class Lab2_second(image_service):
	pass

# THIRD TASK
class Lab2_third(image_service):
	pass

# FOUR TASK
class Lab2_four(image_service):
	pass
        

if __name__ == '__main__':
    lab_two = Lab2_first().call()