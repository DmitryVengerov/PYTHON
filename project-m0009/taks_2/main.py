from skimage import *
from skimage.exposure import histogram
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
        PATH = './lab_2_pic/'

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
class LabTwo(image_service):
    def __init__(self):
        self.image = self.read_file('simple.jpg')
        self.linearImage = self.read_file('./lab_2_pic/linear_stretch.jpg')
        self.pct = 10
        
    def call(self):
        # self.save_image('gray_simple.jpg', self.make_grayscale())
        # self.makeHistogram()

        # self.save_image('linear_stretch.jpg', self.linear_stretch())
        # self.image = self.read_file('./lab_2_pic/linear_stretch.jpg')
        # self.makeHistogram()

        # self.save_image('diff.jpg', self.difference())
        # self.save_image('docked.jpg', self.docking())

        # self.save_image('exp_simple.jpg', self.eachChannel())
        # self.image = self.read_file('./lab_2_pic/exp_simple.jpg')
        # self.makeHistogram()

        self.save_image('gray_word_simple.jpg', self.grayWorld())

    # тут серим
    def make_grayscale(self):
        r_channel = self.image[:,:,0]
        return r_channel    

    # тут делаем гистограмму
    def makeHistogram(self):
        hist, bins = np.histogram(self.image.flatten(), 256, [0, 256])
        plt.hist(self.image.flatten(), 256, [0, 256], color='black')
        plt.xlim([0, 256])
        plt.show()

    # тут робастое растяжение 
    def linear_stretch(self):
        y, x = histogram(self.image)

        xMin = int(np.percentile(x, self.pct))
        xMax = int(np.percentile(x, 100 - self.pct))

        linearImage = np.array([np.array([
                np.clip(np.uint8((px - xMin) * (255/(xMax-xMin))), 0, 255)
                for px in row]) for row in self.image])
        
        return linearImage
    
    # карта разности
    def difference(self):
        return np.abs(self.image - self.linearImage)

    # стыковка изображения
    def docking(self):
        image = self.image
        linearImage = self.linearImage

        for px in range(len(image) // 2, len(linearImage)):
            image[px] = linearImage[px]

        return image.astype('uint8')  

    def exp(self, image):

        y, x = histogram(image)
        
        xMin = int(np.percentile(x, 0))
        xMax = int(np.percentile(x, 100))

        image = np.array([np.array([np.uint8((px - xMin) * (255 / (xMax - xMin))) for px in row]) for row in image])

        return image

    def eachChannel(self):
        image = self.image

        r = self.exp(image[:, :, 0])
        g = self.exp(image[:, :, 1])
        b = self.exp(image[:, :, 2])

        return np.dstack((r, g, b))

    def grayWorld(self):
        av = np.mean(self.image)

        r = np.clip((av / np.mean(self.image[:, :, 0])) * self.image[:, :, 0], 0, 255)
        g = np.clip((av / np.mean(self.image[:, :, 1])) * self.image[:, :, 1], 0, 255)
        b = np.clip((av / np.mean(self.image[:, :, 2])) * self.image[:, :, 1], 0, 255)

        return np.dstack((r, g, b)).astype('uint8')

    
if __name__ == '__main__':
    lab_two = LabTwo().call()