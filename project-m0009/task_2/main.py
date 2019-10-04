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
import cv2 as cv

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

    def get_histogram(self, image, name):
        plt.hist(image.ravel(), bins = range(257))
        plt.xlim([0, 256])
        self.save_image(name, plt)
        # plt.show()
    
    def get_difference(self, source_image, modified_image, name):
        for px in range(len(source_image) // 2, len(modified_image)):
            source_image[px] = modified_image[px]
        return self.save_image(name, source_image.astype('uint8'))
    
    def get_map(self, source_image, modified_image, name):
        return self.save_image(name, np.abs(source_image - modified_image))
    
    def get_convolution(self, image, kernel):
        output = np.zeros_like(image)
        img_padded = np.zeros((image.shape[0] + 2, image.shape[1] + 2))
        img_padded[1 : -1, 1 : -1] = image

        for x in range(image.shape[1]):
            for y in range(image.shape[0]):
                output[y, x] = (kernel * img_padded[y: y+3, x: x+3]).sum()

        return output
    
    def get_docking(self, source_image, modified_image,):
        for px in range(len(source_image) // 2, len(modified_image)):
            source_image[px] = modified_image[px]

        return source_image.astype('uint8') 


class LabTwo(image_service):
    def __init__(self):
        self.image = self.read_file('simple.jpg')
        #self.linearImage = self.read_file('./lab_2_pic_test/linear_stretch.jpg')
       	self.grayImage = self.read_file('./lab_2_pic/gray_simple.jpg')
        #self.spImage = self.read_file('./lab_2_pic/sp_gray_simple.jpg')

        #self.spGrayImage = self.read_file('./lab_2_pic/sp_gray_simple.jpg')
        #self.spMedianImage = self.read_file('./lab_2_pic/sp_median_filter.jpg')

        #self.pct = 10
        self.kernel = np.array([[1/9,1/9,1/9], [1/9,1/9,1/9], [1/9,1/9,1/9]])
        
    def call(self):
        #self.save_image('gray_simple.jpg', self.makeGrayscale())
        #self.makeHistogram()
        #self.save_image('linearStretch.jpg', self.linearStretch())
        #self.image = self.read_file('./lab_2_pic/linearStretch.jpg')
        #self.makeHistogram()
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
        self.save_image('averaging.jpg', self.convolution())
        self.average()
        self.autoav()
        # self.shift_1()
        # self.auto_shift()
        # self.diff_shiftmap()
        # self.gauss_filter()
        # self.auto_gauss()
        # self.get_docking_gauss()
        # self.diff_gauss()
	    # self.sharp()
        # self.autosharp()
        # self.get_docking_autosharp()
        # self.diff_autosharp()
        # self.unsharped_mask()
        # self.unsharped_mask_diff()
        # self.unsharped_mask_map()
        pass
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
        output = np.zeros_like(self.grayImage)
        img_padded = np.zeros((self.grayImage.shape[0] + 2, self.grayImage.shape[1] + 2))
        img_padded[1 : -1, 1 : -1] = self.grayImage

        for x in range(self.grayImage.shape[1]):
            for y in range(self.grayImage.shape[0]):
                output[y, x] = (self.kernel * img_padded[y: y+3, x: x+3]).sum()

        return output

    def average(self):
        self.save_image('average_gray.jpg',self.grayImage.filter(ImageFilter.SMOOTH))
    
    def autoav(self):
        pilgray = Image.open('./lab_2_pic/gray_simple.jpg')
        autoav = pilgray.filter(ImageFilter.SMOOTH)
        autoav.save('./lab_2_pic/autoav.jpg')
        self.save_image('autoav_diff.jpg', (img_as_float(autoav) - img_as_float(pilgray)))

    # 2.5
    def shift_1(self):
        grayImage = self.read_file('./lab_2_pic/gray_simple.jpg')
        kernel = np.array([[0,0,0], [1,0,0], [0,0,0]])
        shift_1 = self.convolution_shift(grayImage, kernel)
        self.save_image('shift_1.jpg', shift_1)

    # TODO:
    # must be DRY
    def convolution_shift(self, image, kernel):
        output = np.zeros_like(image)
        img_padded = np.zeros((image.shape[0] + 2, image.shape[1] + 2))
        img_padded[1 : -1, 1 : -1] = image

        for x in range(image.shape[1]):
            for y in range(image.shape[0]):
                output[y, x] = (kernel * img_padded[y: y+3, x: x+3]).sum()

        return output
    
    # autoshift
    def auto_shift(self):
        grayImage = Image.open('./lab_2_pic/gray_simple.jpg')
        autoshift = ImageChops.offset(grayImage, 1, 0)
        autoshift.save('./lab_2_pic/autoshift.jpg')
    
    def diff_shiftmap(self):
        shift_1 = self.read_file('./lab_2_pic/shift_1.jpg')
        autoshift = self.read_file('./lab_2_pic/autoshift.jpg')
        self.save_image('diff_autoshift.jpg', np.abs(shift_1 - autoshift))

    # gauss filter
    def gauss_filter(self):
        kernel = np.array([[0.09, 0.12, 0.09], [0.12, 0.15, 0.12], [0.09, 0.12, 0.09 ]])
        grayImage = self.read_file('./lab_2_pic/gray_simple.jpg')
        gauss = self.convolution_shift(grayImage, kernel)
        self.save_image('gauss.jpg', gauss)

    def auto_gauss(self):
        grayImage = Image.open('./lab_2_pic/gray_simple.jpg')
        autoGauss = grayImage.filter(ImageFilter.GaussianBlur)
        autoGauss.save('./lab_2_pic/autogauss.jpg')
    
    def get_docking_gauss(self):
        return self.save_image('docking_gauss.jpg', self.docking_gauss())

    def docking_gauss(self):
        image = self.read_file('./lab_2_pic/gray_simple.jpg')
        autoGauss = self.read_file('./lab_2_pic/autogauss.jpg')

        for px in range(len(image) // 2, len(autoGauss)):
            image[px] = autoGauss[px]

        return image.astype('uint8') 

    def diff_gauss(self):
        image = self.read_file('./lab_2_pic/gray_simple.jpg')
        autoGauss = self.read_file('./lab_2_pic/autogauss.jpg')
        self.save_image('map_gauss.jpg', np.abs(image - autoGauss))

    # повышение резкости 
    def sharp(self):
	    image = self.read_file('./lab_2_pic/gray_simple.jpg')
	    kernel = np.array([[0, -0.04, 0],[-0.04, 2, -0.04],[0,-0.04,0]])
	    sharpened = self.convolution_shift(image, kernel)
	    self.save_image('sharped.jpg', sharpened)

    def autosharp(self):
        grayImage = Image.open('./lab_2_pic/gray_simple.jpg')
        autosharp = grayImage.filter(ImageFilter.SHARPEN)
        autosharp.save('./lab_2_pic/autosharp.jpg')

    def get_docking_autosharp(self):
        return self.save_image('docking_autosharp.jpg', self.docking_autosharp())

    def docking_autosharp(self):
        image = self.read_file('./lab_2_pic/gray_simple.jpg')
        autosharp = self.read_file('./lab_2_pic/sharped.jpg')

        for px in range(len(image) // 2, len(autosharp)):
            image[px] = autosharp[px]

        return image.astype('uint8') 

    def diff_autosharp(self):
        image = self.read_file('./lab_2_pic/gray_simple.jpg')
        autosharp = self.read_file('./lab_2_pic/sharped.jpg')
        self.save_image('map_autosharp.jpg', np.abs(image - autosharp))

    # unsharped mask 
    def unsharped_mask(self):
        image = self.read_file('./lab_2_pic/gray_simple.jpg')

        gaussian_3 = cv.GaussianBlur(image, (9, 9), 10.0)
        unsharped_img = cv.addWeighted(image, 1.5, gaussian_3, -0.5, 0, image)
        cv.imwrite('./lab_2_pic/unsharp_img.jpg', unsharped_img)

    def unsharped_mask_diff(self):
        image = self.read_file('./lab_2_pic/gray_simple.jpg')
        unsharped = self.read_file('./lab_2_pic/unsharp_img.jpg')

        for px in range(len(image) // 2, len(unsharped)):
            image[px] = unsharped[px]

        self.save_image('unsharped_mask_diff.jpg', image.astype('uint8'))


    def unsharped_mask_map(self):
        image = self.read_file('./lab_2_pic/gray_simple.jpg')
        unsharped = self.read_file('./lab_2_pic/unsharp_img.jpg')
        self.save_image('unsharped_mask_map.jpg', np.abs(image - unsharped))

# class 

if __name__ == '__main__':
    LabTwo().call()

