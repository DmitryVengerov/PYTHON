from skimage import *
from skimage.exposure import histogram
from skimage.util import random_noise
from scipy.ndimage.filters import median_filter
from PIL import Image, ImageFilter, ImageChops
import os
import numpy as np
import collections
import warnings
import matplotlib.pyplot as plt

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
        self.grayImage = self.read_file('./lab_2_pic/gray_simple.jpg')
        self.spImage = self.read_file('./lab_2_pic/sp_gray_simple.jpg')

        self.spGrayImage = self.read_file('./lab_2_pic/sp_gray_simple.jpg')
        self.spMedianImage = self.read_file('./lab_2_pic/sp_median_filter.jpg')

        self.pct = 10
        self.kernel = np.array([[1/9,1/9,1/9], [1/9,1/9,1/9], [1/9,1/9,1/9]])
        
    def call(self):
        # self.save_image('gray_simple.jpg', self.makeGrayscale())
        # self.makeHistogram()

        # self.save_image('linearStretch.jpg', self.linearStretch())
        # self.image = self.read_file('./lab_2_pic/linearStretch.jpg')
        # self.makeHistogram()

        # self.save_image('diff.jpg', self.difference())
        # self.save_image('docked.jpg', self.docking())

        # self.save_image('exp_simple.jpg', self.eachChannel())
        # self.image = self.read_file('./lab_2_pic/exp_simple.jpg')
        # self.makeHistogram()

        # self.save_image('gray_word_simple.jpg', self.grayWorld())

        # self.save_image('docking_gray_wold.jpg', self.dockingGrayWorld())

        # self.save_image('spGray_simple.jpg', self.spGray())
        # self.save_image('sp_median_filter.jpg', self.medianFilter())
        
        # self.save_image('gray_diff_filtered.jpg', self.differenceFilter())
        # self.save_image('grat_convolution.jpg', self.convolution())
        self.average()

    # тут серим
    def makeGrayscale(self):
        r_channel = self.image[:,:,0]
        return r_channel    

    # тут делаем гистограмму
    def makeHistogram(self):
        hist, bins = np.histogram(self.image.flatten(), 256, [0, 256])
        plt.hist(self.image.flatten(), 256, [0, 256], color='black')
        plt.xlim([0, 256])
        plt.show()

    # тут робастое растяжение 
    def linearStretch(self):
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
    
    def differenceFilter(self):
        return np.abs(img_as_float(self.spMedianImage), img_as_float(self.spGrayImage))

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

        # стыковка изображения
    
    def dockingGrayWorld(self):
        image = self.image
        Image = self.grayWorld()

        for px in range(len(image) // 2, len(Image)):
            image[px] = Image[px]

        return image.astype('uint8')  
    
    def spGray(self): 
        return random_noise(self.grayImage, mode='s&p', seed=None, clip=True)
    
    def medianFilter(self):
        return median_filter(self.spImage, 3)

    # 2.4
    def convolution(self):
        kernel = np.flipud(np.fliplr(self.kernel))
        output = np.zeros_like(self.grayImage)
        img_padded = np.zeros((self.grayImage.shape[0] + 2, self.grayImage.shape[1] + 2))
        img_padded[1 : -1, 1 : -1] = self.grayImage

        for x in range(self.grayImage.shape[1]):
            for y in range(self.grayImage.shape[0]):
                output[y, x] = (kernel * img_padded[y: y+3, x: x+3]).sum()

        return output

    def average(self):
        # pass
        self.save_image('average_gray.jpg',self.grayImage.filter(ImageFilter.SMOOTH))




if __name__ == '__main__':
    lab_two = LabTwo().call()