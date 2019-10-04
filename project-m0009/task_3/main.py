from skimage.util.shape import view_as_windows
from skimage.io import imread, imshow, imsave
from skimage import *
from scipy.fftpack import dct, idct
from collections import Counter, namedtuple

import os
import math
import numpy as np
import warnings
import math
import heapq

class Image_service:
  def __init__(self):
    pass

  def save_image(self, name, image):
    PATH = './lab_3_pic/'

    if not os.path.isdir(PATH):
      os.makedirs(PATH)
    
    io.imsave(PATH + name, image)
    print('Save done')
  

class Compression(Image_service):
  def __init__(self, urlImage = 'simple.jpg'):
    self.image = imread(urlImage)
    self.lum = np.array([
                [16, 11, 10, 16, 24, 40, 51, 61],
                [12, 12, 14, 19, 26, 58, 60, 55],
                [14, 13, 16, 24, 40, 57, 69, 56],
                [14, 17, 22, 29, 51, 87, 80, 62],
                [18, 22, 37, 56, 68, 109, 103, 77],
                [24, 35, 55, 64, 81, 104, 113, 92],
                [49, 64, 78, 87, 103, 121, 120, 101],
                [72, 92, 95, 98, 112, 100, 103, 99],
                ])

    self.chrom = np.array([
                [17, 18, 24, 47, 99, 99, 99, 99],
                [18, 21, 26, 66, 99, 99, 99, 99],
                [24, 26, 56, 99, 99, 99, 99, 99],
                [47, 66, 99, 99, 99, 99, 99, 99],
                [99, 99, 99, 99, 99, 99, 99, 99],
                [99, 99, 99, 99, 99, 99, 99, 99],
                [99, 99, 99, 99, 99, 99, 99, 99],
                [99, 99, 99, 99, 99, 99, 99, 99],
                ])
  
  def call(self):
    Y, Cb, Cr, wY, wCb, x, y, huffman_alph = self.compression()
    img = self.decompression(Y, Cb, Cr, wY, wCb, x, y, huffman_alph)
    self.save_image('new_image.jpg', img)

    pass

  def ycbct_rgb(self, image):

    image[:, :, 1] -= 128
    image[:, :, 2] -= 128
    coefficents = [[1, 0, 1.402], [1, -.34414, -.71414], [1, 1.772, 0]]
    new_image = np.dot(image, np.transpose(coefficents))
    new_image = np.clip(new_image, 0, 255)
    return new_image.astype('uint8')
  
  def rgb_ycbct(self, image):
    coefficents = [[0.299, 0.587, 0.114], [-0.1687, -0.3313, 0.5], [0.5, -0.4187, -0.0813]]
    new_image = np.dot(image, np.transpose(coefficents))
    new_image[:, :, 1] += 128
    new_image[:, :, 2] += 128
    return new_image.astype('uint8')

  def get_decimation(self, image):
    x, y = image.shape[0] // 2, image.shape[1] // 2
    t = view_as_windows(image, (2,2), step=2)
    temp = [[]]
    k = 0
    for elem in t:
        for i in elem:
            if k < y:
                temp[-1].append(int(i.mean()))
                k += 1
            else:
                k = 1
                temp.append([])
                temp[-1].append(int(i.mean()))
    #new = np.array(np.repeat(np.repeat(temp, 2, axis=1), 2, axis=0))
    return np.array(temp)

  # def get_decimation(self, image):
  #   self.decimation(image[:, :, 1])
  #   self.decimation(image[:, :, 2])

  #   return image

  # def decimation(self, channel):
  #     for i in range(0, channel.shape[0], 2):
  #         for j in range(0, channel.shape[1], 2):
  #             channel[i][j+1] = channel[i][j]
  #         channel[i-1] = channel[i]

  def recovery(image, new):
    if image.shape[1] % 2 != 0 and image.shape[0] % 2 == 0:
        new = np.hstack((new, np.reshape(image[:, -1], (-1, 1))))
    if image.shape[1] % 2 == 0 and image.shape[0] % 2 != 0:
        new = np.vstack((new, np.reshape(image[-1, :], (1, -1))))
    if image.shape[1] % 2 != 0 and image.shape[0] % 2 != 0:
        new = np.vstack((new, np.reshape(image[-1, :], (1, -1))[-1][:-1]))
        new = np.hstack((new, np.reshape(image[:, -1], (-1, 1))))
    return new

  def refect_across_edge(self, image, a):
    new_image = image.copy()
    height, width = image.shape[0] % a, image.shape[1] % a
    if width != 0:
      if width % 2 == 0:
        k = (a - width) // 2
        new_image = np.hstack((new_image, np.flip(new_image[:, -k:], 1)))
        new_image = np.hstack((np.flip(new_image[:, :k], 1), new_image))
      else:
        k = (a - width) // 2
        new_image = np.hstack((new_image, np.flip(new_image[:, -(k+1):], 1)))
        new_image = np.hstack((np.flip(new_image[:, :k], 1), new_image))
    if height != 0:
      if height % 2 == 0:
        k = (a - height) // 2
        new_image = np.vstack((new_image, np.flip(new_image[-k:, :], 0)))
        new_image = np.vstack((np.flip(new_image[:k, :], 0), new_image))
      else:
        k = (a - height) // 2
        new_image = np.vstack((new_image, np.flip(new_image[-(k+1):, :], 0)))
        new_image = np.vstack((np.flip(new_image[:k, :], 0), new_image))
    return new_image

  def quantize(self, block, param):
    if param == 'lum':
        return np.round(block / self.lum)
    else:
        return np.round(block / self.chrom)

  def recovery_quantize(self, block, param):
    if param == 'lum':
        return np.round(block * self.lum)
    else:
        return np.round(block * self.chrom)

  def code(self, layer, param):
    code_block = []
    for i in range(layer.shape[0]):
        code_block.append([])
        for j in range(layer.shape[1]):
            layer[i, j] = layer[i, j] - 128
            layer[i, j] = dct(dct(layer[i, j].T, norm='ortho').T, norm='ortho')
            layer[i, j] = self.quantize(layer[i, j], param)
            code_block[i].append(self.zigzag_walk(layer[i, j], 8))
    return code_block

  def zigzag_walk(self, block, n):
    temp = []
    zigzag_block = []
    for i in range(n):
        for j in range(i + 1):
            if block != []:
                temp.append(block[i - j, j])
            else:
                temp.append((i - j, j))
        if i % 2 != 0:
            temp.reverse()
        for j in range(len(temp)):
            zigzag_block.append(temp[j])
        temp = []
    for k in range(1, n):
        temp = []
        val = -1
        for j in range(k, n):
            val += 1
            if block != []:
                temp.append(block[n - 1 - val, j])
            else:
                temp.append((n - 1 - val, j))
        if k % 2 == 0:
            temp.reverse()
        for d in range(len(temp)):
            zigzag_block.append(temp[d])
        
    return zigzag_block

  def recovery_blocks(self, code_block):
    layer = []
    for i in range(len(code_block)):
        layer.append([])
        for j in range(len(code_block[0])):
            layer[i].append([])
            a = self.zigzag_walk([], 8)
            temp = [[0 for i in range(8)] for j in range(8)]
            for k in range(8):
                for d in range(8):
                    temp[a[k * 8 + d][0]][a[k * 8 + d][1]] = code_block[i][j][k * 8 + d]
            layer[i][j] = temp.copy()
    return layer

  def decode(self, layer, param):
    layer = np.array(layer)
    for i in range(len(layer)):
        for j in range(len(layer[0])):
            layer[i, j] = self.recovery_quantize(layer[i, j], param)
            layer[i, j] = idct(idct(layer[i, j].astype('int').T, norm='ortho').T, norm='ortho')
            layer[i, j] = layer[i, j] + 128
            layer[i, j] = layer[i, j]
    return layer

  def recovery_layer(self, layer, n):
    rec_layer = [[0 for i in range(len(layer[0]) * n)] for j in range(len(layer) * n)]
    for i in range(len(layer)):
        for j in range(len(layer[i])):
            for k in range(len(layer[i][j])):
                for d in range(len(layer[i][j][k])):
                    rec_layer[i * n + k][j * n + d] = layer[i][j][k][d]
    return rec_layer
  
  def huffman_encode(self, counter):
    h = []
    for ch, freq in counter.items():
        h.append((freq, len(h), Leaf(ch)))
    heapq.heapify(h)
    count = len(h)
    while len(h) > 1:
        freq1, _count1, left = heapq.heappop(h)
        freq2, _count2, right = heapq.heappop(h)
        heapq.heappush(h, (freq1 + freq2, count, Node(left, right)))
        count += 1
    code = {}
    if h:
        [(_freq, _count, root)] = h
        root.walk(code, "")
    return code

  def return_dict(self, sequence):
    counter = Counter()
    for k in sequence:
        for i in k:
            for j in i:
                for elem in j:
                    counter[str(elem)] += 1
    return counter
  
  def return_code_str(self, sequence, huffman_alph):
    s = ""
    for i in sequence:
        for j in i:
            for elem in j:
                try:
                    s += huffman_alph[str(elem)]
                except RuntimeWarning as e:
                    print(elem)
                    break
    return s

  def huffman_decode(self, encoded, code, w):
    a = 0
    b = 0
    sx = []
    enc_ch = ""
    for ch in encoded:
        enc_ch += ch
        if enc_ch in code:
            if a == 0 and b == 0:
                sx.append([])
                sx[-1].append([])
            elif a != 0 and b == 0:
                sx[-1].append([])
            sx[-1][-1].append(int(code[enc_ch]))
            enc_ch = ""
            b += 1
            if b == 64:
                b = 0
                a += 1
            if a == w:
                a = 0
    return sx
  
  def recovery_size(self, layer, w, h):
    x, y = abs(layer.shape[0] - w) // 2, (layer.shape[1] - h) // 2
    cx, cy = 0, 0
    if x == 0:
        cx = w
    if y == 0:
        cy = h
    return layer[x:-x+cx, y:-y+cy]
  # Сжатие
  def compression(self):
    image = self.image

    # размеры изображения
    x = image.shape[0]
    y = image.shape[1]

    # Переводим в YCbCr
    new_image = self.rgb_ycbct(image)
    
    # Дополняем до кратности 16 и сразу делаем децимацию 
    Y = self.refect_across_edge(new_image[:, :, 0].astype('int'), 16)
    Cb = self.get_decimation(self.refect_across_edge(new_image[:, :, 1], 16)).astype('int')
    Cr = self.get_decimation(self.refect_across_edge(new_image[:, :, 2], 16)).astype('int')
    
    # Разбиваем слои на блоки 8 на 8
    Y = view_as_windows(Y, (8,8), step = 8)
    Cb = view_as_windows(Cb, (8,8), step = 8)
    Cr = view_as_windows(Cr, (8,8), step = 8)

    # Центрируем, делаем дискретное косинусное преобразование, квантуем и преобразуем блоки зигзаг обходом.
    Y = self.code(Y, 'lum')
    Cb = self.code(Cb, 'chrom')
    Cr = self.code(Cr, 'chrom')

    # Считаем, сколько блоков входит в строку
    wY = len(Y[0])
    wCb = len(Cb[0])

    # Подсчитываем количество одинаковых значений
    counter = self.return_dict((Y, Cb, Cr))

    # Строим алфовит хаффмана
    huffman_alph = self.huffman_encode(counter)

    # Возвращаем кодированные слои методом Хаффмана
    Y = self.return_code_str(Y, huffman_alph)
    Cb = self.return_code_str(Cb, huffman_alph)
    Cr = self.return_code_str(Cr, huffman_alph)

    # Разворачиваем алфавит
    huffman_alph = {v:k for k, v in huffman_alph.items()}

    # Возвращаем слои Y, Cb, Cr, количество входящих блоков в строку, размеры изображения, развернутый алфавит
    return Y, Cb, Cr, wY, wCb, x, y, huffman_alph

  def decompression(self, Y, Cb, Cr, wY, wCb, w, h, huffman_alph):
    # Декодируем слои
    Y = self.huffman_decode(Y, huffman_alph, wY)
    Cb = self.huffman_decode(Cb, huffman_alph, wCb)
    Cr = self.huffman_decode(Cr, huffman_alph, wCb)

    # Восстанавливаем блоки из одномерных массивов
    Y = self.recovery_blocks(Y)
    Cb = self.recovery_blocks(Cb)
    Cr = self.recovery_blocks(Cr)

    # Восстанавливаем квантованную последовательность, обратную DCT, и центрируем назад
    Y = self.decode(Y, 'lum')
    Cb = self.decode(Cb, 'chrom')
    Cr = self.decode(Cr, 'chrom')

    # Восстанавливаем слои без блоков
    Y = self.recovery_layer(Y, 8)
    Cb = self.recovery_layer(Cb, 8)
    Cr = self.recovery_layer(Cr, 8)

    # Восстанавливаем слои, копируя каждый элемент в блок 2 на 2 (Обратная децимация)
    Cb = np.array(np.repeat(np.repeat(Cb, 2, axis=1), 2, axis=0))
    Cr = np.array(np.repeat(np.repeat(Cr, 2, axis=1), 2, axis=0))

    # Y делаем nbgf тгьзн
    Y = np.array(Y)

    # Восстанавливаем размерность до исходной
    Y = self.recovery_size(Y, w, h)
    Cb = self.recovery_size(Cb, w, h)
    Cr =  self.recovery_size(Cr, w, h)
    
    # Переводим в RGB
    new_image = self.ycbct_rgb((np.dstack((Y, Cb, Cr))))
    return new_image
  

class Node(namedtuple("Node", ["left", "right"])):
    def walk(self, code, acc):
        self.left.walk(code, acc + "0")
        self.right.walk(code, acc + "1")

class Leaf(namedtuple("Leaf", ["char"])):
    def walk(self, code, acc):
        code[self.char] = acc or "0"

if __name__ == '__main__':
  Compression().call()