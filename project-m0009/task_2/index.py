from skimage import *
from skimage.exposure import histogram
from skimage.util import random_noise
from skimage.io import imread, imshow
from scipy.ndimage.filters import median_filter
from PIL import Image, ImageFilter, ImageChops

import os
import numpy as np
import collections
import warnings
import matplotlib.pyplot as plt
import cv2 as cv
import random

class ImageService:
  def __init__(self):
    pass

  def save_image(self, name, image):
    PATH = './lab_pic/'
    if not os.path.isdir(PATH):
      os.makedirs(PATH)
    io.imsave(PATH + name, image)
    print('Save done')

  def read_file(self, name):
    return io.imread(name)

  def get_histogram(self, image, name):
    plt.hist(image.ravel(), bins = range(257))
    plt.xlim([0, 256])
    plt.show()

  def get_difference(self, source_image, modified_image, name):
    for px in range(len(source_image) // 2, len(modified_image)):
      source_image[px] = modified_image[px]
    return self.save_image(name, source_image.astype('uint8'))

  def get_map(self, source_image, modified_image, name):
    return self.save_image(name, np.abs(source_image - modified_image))

  def get_convolution(self, image, kernel):
    output = np.zeros_like(image) 
    img_padded = np.zeros((image.shape[0] + 2, image.shape[1] + 2)) 
    img_padded[1: -1, 1: -1] = image
    for x in range(image.shape[1]):
      for y in range(image.shape[0]):
        output[y, x] = (kernel * img_padded[y: y + 3, x: x + 3]).sum()
    return output

  def get_docking(self, source_image, modified_image, ):
    for px in range(len(source_image) // 2, len(modified_image)):
      source_image[px] = modified_image[px]

    return source_image.astype('uint8')
  
  def map_difference(self, img1, img2):
    return img_as_ubyte(np.abs(img_as_float(img1) - img_as_float(img2)))

class First(ImageService):
  '''
  Используя стандартные функции постройте гистограмму яркостей изображения.
  Примените к изображению операцию «робастное линейное растяжение яркости» (в качестве порога возьмите 5-10% в зависимости от изображения).
  Включите в отчёт гистограмму, исходное и обработанные изображения, карту разности.
  Картой разности двух изображений называем изображение, 
  в котором яркость пикселей - это модуль разности между изображениями, 
  т.е. * карта разницы - это изображение, на котором показана разница между двумя изображениями.
  '''
  def __init__(self):
    self.image = self.read_file('simple.jpg')
  
  def call(self):
    # self.get_histogram(self.image.astype('uint8'), 'simple_hist.jpg')
    new_img = self.linear_tension(self.image)
    # self.save_image('linear_tension.jpg', new_img)
    
    # self.get_histogram(new_img, 'linear_tension_histogram.jpg')
    self.get_difference(new_img, self.image, 'map_simple.jpg')

  # Линейное растяжение
  def linear_tension(self, img):
    k = round(img.size * 0.05)
    values, _, = np.histogram(img.ravel(), bins=range(257))
    count = 0
    # Отбрасываем 5% самых больших и самых маленьких значений
    for i in range(len(values)):
      count += values[i]
      values[i] = 0
      if count > k:
        break
    count = 0
    for i in range(len(values) - 1, -1, -1):
      count += values[i]
      values[i] = 0
      if count > k:
        break
    for i in range(len(values)):
      if values[i] != 0:
        min_x = i - 1
        break
    for i in range(len(values) - 1, -1, -1):
      if values[i] != 0:
        max_x = i + 1
        break
    # Функция линейного выравнивания
    img = img.astype('float')
    img = (img - min_x) * (255 / (max_x - min_x))
    img = np.clip(img, 0, 255)
    return img.astype('uint8')

class Second(ImageService):
  '''
  Примените операции «линейное растяжение по каналам» и «серый мир» к изображению.
  Операцию «серый мир» нужно реализовать самостоятельно.
  Включите в отчёт код и состыкованное изображение результатов применения операций.
  '''
  def __init__(self):
    self.image_2 = self.read_file('simple_2.jpg')
  
  def call(self):
    result = self.channel_linear_stretching(self.image_2)
    # self.save_image('linear_stretching_simple_2.jpg', result)
    map_simple = self.map_difference(self.image_2, result)
    # self.save_image('map.jpg', map_simple)
    
    docking_simple = self.get_docking(self.image_2, result)
    # self.save_image('docking_simple.jpg', docking_simple)
    
    grey_world = self.greyworld(self.image_2)
    # self.save_image('grayword_simple.jpg', grey_world)
    
    map_grey_world = self.map_difference(self.image_2, grey_world)
    # self.save_image('grayworld_map.jpg', map_grey_world)
    
    grayworld_dock = self.get_docking(self.image_2, grey_world)
    # self.save_image('grayworld_docking.jpg', grayworld_dock)

  def channel_linear_stretching(self, img):
    img = img
    r = img[:, :, 0]
    g = img[:, :, 1]
    b = img[:, :, 2]
    max_x, min_x = r.max(), r.min()
    r = np.uint8((r - min_x) * (255 / (max_x - min_x)))
    max_x, min_x = g.max(), g.min()
    g = np.uint8((g - min_x) * (255 / (max_x - min_x)))
    max_x, min_x = b.max(), b.min()
    b = np.uint8((b - min_x) * (255 / (max_x - min_x)))
    return np.dstack((r, g, b))
  
  def greyworld(self, img):
    avg = np.mean(img)
    r, g, b = np.mean(img[:, :, 0]) / avg, np.mean(img[:, :, 1]) / avg, np.mean(img[:, :, 2]) / avg
    new_r = np.clip(img[:, :, 0] / r, 0, 255)
    new_g = np.clip(img[:, :, 1] / g, 0, 255)
    new_b = np.clip(img[:, :, 2] / b, 0, 255)
    new_img = np.uint8(np.dstack((new_r, new_g, new_b)))
    return new_img
  
class Third(ImageService):
  '''
  Зашумите изображение шумом типа «соль и перец». Подавите шум медианным фильтром, попробуйте разные размеры фильтра.
  Постройте карты разницы между исходным и зашумленным изображениями, и между скорректированным и исходным.
  Подумайте над способами получения этой разницы.
  В отчёт вставьте состыкованные исходное/обработанное изображения и карты разницы
  '''
  def __init__(self):
    self.image_2 = self.read_file('simple_2.jpg')

  def call(self):
    salt_image = self.salt_pepper(self.image_2, 1000)
    # self.save_image('salt_simple.jpg', salt_image)
    
    diff_salf = self.map_difference(salt_image, self.image_2)
    # self.save_image('diff_salt.jpg', diff_salf)

    median_image = self.medianFilter(self.image_2)
    # self.save_image('median_salt.jpg', median_image)

    diff_median = self.map_difference(median_image, self.image_2)
    # self.save_image('diff_median.jpg', diff_median)

    median_dock = self.get_docking(median_image, self.image_2)
    self.save_image('median_dock.jpg', median_dock)


  def salt_pepper(self, img, n):
    height, width = img.shape[0], img.shape[1]
    for i in range(n):
        h = random.randint(0, height - 1)
        w = random.randint(0, width - 1)
        img[h, w] = (255, 255, 255)
        h = random.randint(0, height - 1)
        w = random.randint(0, width - 1)
        img[h, w] = (0, 0, 0)
    return img
  
  def median_filter(self, img, n):
    height, width = img.shape[0], img.shape[1]
    value = n // 2
    coordinates = [[(i, j) for j in range(-value, value + 1)] for i in range(-value, value + 1)]
    new_img = img.copy()
    for i in range(height):
        for j in range(width):
            array = []
            for x in range(n):
                for y in range(n):
                    if (i + coordinates[x][y][0] >= 0) and (i + coordinates[x][y][0] < height) and (j + coordinates[x][y][1] >= 0) and (j + coordinates[x][y][1] < width):
                        array.append(img[i + coordinates[x][y][0], j + coordinates[x][y][1]])
                    else:
                        pass
            array.sort()
            if len(array) % 2 == 0:
                new_img[i, j] = round((array[len(array) // 2] + array[(len(array) // 2) - 1]) / 2)
            else:
                new_img[i, j] = array[len(array) // 2]
    return new_img  

  def medianFilter(self, image):
    return median_filter(image, 3)

class Fourth(ImageService):
  '''
  Самостоятельно напишите код для операции свёртки. Примените к изображению свёртки четырьмя разными 
  фильтрами размера 3x3: «усреднение», «сдвиг на 1», «гауссов», «повышение резкости». Для этого подберите разные ядра фильтра.
  Сравните результат работы собственного фильтра со встроенными функциями, для этого постройте карты разницы изображений.
  Включите в отчёт исходное и обработанные изображения, карты разности.
  '''
  def __init__(self):
    self.image_2 = self.read_file('simple_2.jpg')
    self.kernel = [[0,0,0], [1,0,0], [0,0,0]]

  def call(self):
    gray_image = self.makeGrayscale(self.image_2)
    # convolution_image = self.convolution(gray_image, self.kernel)
    # self.save_image('convolution_image.jpg', convolution_image)

    # offsetlib = ImageChops.offset(gray_image, 1, 0)
    # map_diff_fouth = self.map_difference(offsetlib, convolution_image)
    # self.save_image('map_diff_fouth.jpg', map_diff_fouth)
    
    # self.gauss_filter(gray_image)
    # увеличение резкости
    kernel = np.array([[0,-2,0],[-2,16,-2],[0,-2,0]]) * 1/8
    sharpening = self.convolution(gray_image, kernel)
    self.save_image('sharpening.jpg', sharpening)

  # Свертка
  def convolution(self, img, kernel, flag=True):
    output = np.zeros_like(img)
    img_padded = np.zeros((img.shape[0] + 2, img.shape[1] + 2))
    img_padded[1 : -1, 1 : -1] = img

    for x in range(img.shape[1]):
      for y in range(img.shape[0]):
        output[y, x] = (kernel * img_padded[y: y+3, x: x+3]).sum()

    return output

  def makeGrayscale(self, image):
    r_channel = image[:,:,0]
    return r_channel 
  
  def gauss_filter(self, image):
        kernel = np.array([[0.09, 0.12, 0.09], [0.12, 0.15, 0.12], [0.09, 0.12, 0.09 ]])
        gauss = self.convolution_shift(image, kernel)
        self.save_image('gauss.jpg', gauss)
      
  def convolution_shift(self, image, kernel):
    output = np.zeros_like(image)
    img_padded = np.zeros((image.shape[0] + 2, image.shape[1] + 2))
    img_padded[1 : -1, 1 : -1] = image

    for x in range(image.shape[1]):
        for y in range(image.shape[0]):
          output[y, x] = (kernel * img_padded[y: y+3, x: x+3]).sum()

    return output

class Fifth(ImageService):
  def __init__(self):
    self.image = self.makeGrayscale(imread('simple.jpg'))

  def call(self):
    kernel = np.array([[self.gaussian(1, x, y) for x in range(-2, 3)] for y in range(-2, 3)])
    s = sum(sum(kernel))
    kernel = kernel / s
    filter_gauss = self.convolution(self.image, kernel)
    self.save_image('filter_gauss.jpg', filter_gauss)

  def convolution(self, img, kernel, flag=True):
    output = np.zeros_like(img)
    img_padded = np.zeros((img.shape[0] + 2, img.shape[1] + 2))
    img_padded[1 : -1, 1 : -1] = img

    for x in range(img.shape[1]):
      for y in range(img.shape[0]):
        output[y, x] = (kernel * img_padded[y: y+3, x: x+3]).sum()

    return output

  def gaussian(self, sigma, x, y):
    return (1 / (2 * np.pi * sigma ** 2)) * np.e ** ((-x ** 2 - y ** 2) / (2 * sigma ** 2))
  
  def makeGrayscale(self, image):
    r_channel = image[:,:,0]
    return r_channel 




if __name__ == "__main__":
  # First().call()
  # Second().call()
  # Third().call()
  # Fourth().call()
  Fifth().call()
