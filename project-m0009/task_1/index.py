from skimage import *
import os
import numpy as np
import collections

# FIRST TASK
# В цветовом пространстве greyscale требуется реализовать
# алкгоритм скалярного равномерного квантования с переменной
# скоростью для постепенного уменьшение уровней яркости 
# изображения. Сохранить изображение, в котором количество
# уровней яркости << 256, при этом визуально приемлемое качество. 
class Lab1_first:
    def __init__(self, urlImage = 'simple.jpg'):
        # upload image from directory
        self.image = io.imread(urlImage)
        self.lower_image = [self.dimming(self.make_grayscale(), 2**i) for i in range(3,8)] 
    
    def call(self):
        self.save_image('first_simple_gray.jpg', self.make_grayscale())
        self.save_image('first_simple_dimmig_8.jpg', self.lower_image[0])
        self.save_image('first_simple_dimmig_16.jpg', self.lower_image[1])
        self.save_image('first_simple_dimmig_32.jpg', self.lower_image[2])
        
    def save_image(self, name, image):
        PATH = './lab_1_pic/'

        if not os.path.isdir(PATH):
            os.makedirs(PATH)

        io.imsave(PATH + name, image)
        print('Save done')


    # must be private

    def make_grayscale(self):
        r_channel = self.image[:,:,0]

        return r_channel

    def dimming(self, image, level = 256):
        image_temp = np.round(image/level) * level
        image_temp = np.clip(image_temp, 0, 255).astype('uint8')

        return image_temp

# FIRST SECOND
# В технологии JPEG применяется формат YUV для 
# промежуточного представления изображения. В этом формате
# два канала (2 и 3) хранят информацию о цвете, а один канал - щ
# яркости. Требуется написать алгоритм 
# децимации цветоразностных каналов. Необходимо реализовать
# отдельно кодирование и декодрирование. 
class Lab1_second(Lab1_first):
    def __init__(self, urlImage = 'simple.jpg'):
        self.image = io.imread(urlImage)

        self.const_Y = np.array([.299, .587, .114])
        self.const_Cb = np.array([-.1687, -.3313, .5])
        self.const_Cr = np.array([.5, -.4187, -.0813])

        self.const_R = np.array([1,0, 1.402])
        self.const_G = np.array([1, -.34414, -.71414])
        self.const_B = np.array([1, 1.772, 0])


    def call(self):
        self.save_image('second_simple_yuv_1.jpg', self.from_rgb())
        self.save_image('second_simple_rgb.jpg', self.to_rgb())
        self.save_image('decimation_simple_yuv.jpg', self.do_decimation())
        self.save_image('decimation_simple_rgb.jpg', self.to_rgb('./lab_1_pic/decimation_simple_yuv.jpg'))

    # must be private

    def from_rgb(self):
        Y = self.image.dot(self.const_Y).T
        Cb = self.image.dot(self.const_Cb).T + 128
        Cr = self.image.dot(self.const_Cr).T + 128

        return np.uint8(np.array([Y,Cb,Cr]).T)

    def to_rgb(self, name = './lab_1_pic/second_simple_yuv_1.jpg' ):
        image = io.imread(name)
        img = image.astype(np.float)

        img[:, :, 1] -= 128
        img[:, :, 2] -= 128

        R = img.dot(self.const_R).T
        G = img.dot(self.const_G).T
        B = img.dot(self.const_B).T

        rgb = np.array([R,G,B]).T

        np.putmask(rgb, rgb > 255, 255)
        np.putmask(rgb, rgb < 0, 0)

        return np.uint8(rgb)

    def do_decimation(self):
        image = io.imread('./lab_1_pic/second_simple_yuv_1.jpg')
        self.decimation(image[:, :, 1])
        self.decimation(image[:, :, 2])

        return image

    def decimation(self, channel):
        for i in range(0, channel.shape[0], 2):
            for j in range(0, channel.shape[1], 2):
                channel[i][j+1] = channel[i][j]
            channel[i-1] = channel[i]

# THIRD TASK
# Для оценки работы алгоритмов в задании 1 и 2, необходимо
# посчитать энтропию и среднеквадратичную ошибку
class Lab1_third:
    def __init__(self):
        self.simple_image = io.imread('simple.jpg')
        self.yuv_image = io.imread('./lab_1_pic/second_simple_yuv_1.jpg')
        self.dec_image = io.imread('./lab_1_pic/decimation_simple_rgb.jpg')

    def call(self):
        self.mse(self.simple_image, self.yuv_image)
        self.mse(self.simple_image, self.dec_image)
        self.entropy(self.simple_image)

    def mse(self, image1, image2):
        print(((image1-image2)**2).mean())

    def entropy(self, image):
        count = collections.Counter(list(image.reshape(-1)))
        counts = np.array(list(count.values()))
        prob = counts / sum(counts)

        print(count[1] / sum(counts[1]))
        print(-np.sum(np.log2(prob) * prob))

if __name__ == '__main__':
    lab_one = Lab1_first().call()
    # lab_one = Lab1_second().call()
    # lab_one = Lab1_third().call()

