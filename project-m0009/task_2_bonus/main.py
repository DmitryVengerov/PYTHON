from numpy import random
from sklearn.metrics import mean_squared_error as mse
from scipy.stats import entropy
from copy import deepcopy

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class UniformScalarQuantizer:
    '''
    Сгенерировать массив из 100 значений, которые представляют собой выборку из нормального распределения с мат. 
    ожиданием = 0 и дисперсией = 1. 
    Проквантовать равномерным скалярным квантователем с переменной скоростью. 
    Количество квантов: от 7 до 9 на выбор студента.
    Найти среднеквадратичную ошибку и энтропию. Реализовать оптимальный вариант (с меньшей среднеквадратичной ошибкой) квантователя.
    '''
    def __init__(self):
        self.mu = 5
        self.sigma = 1
        self.size = 100
        self.quants = 8
        self.data = self.create_data(self.mu, self.sigma, self.size)
        self.step = self.count_step(self.data, self.quants)
        self._min = min(self.data)
    def call(self):
        quanted_data = self.quantize(self.data, self.step)
        restored_data = self.resotre(quanted_data, self.step, self._min)
        intervals = self.set_intervals(self.step, self.quants, self._min)
        restored_data = np.clip(restored_data, min(intervals), max(intervals))
        self.get_info(self.data, restored_data)      
        self.paint_plot(self.data, restored_data, intervals)
        pass
    # генерация выборки
    def create_data(self, mu, sigma, size):
        return random.normal(mu, sigma, size = size)
    # подсчет шага квантования
    def count_step(self, data, quants):
        return (max(data) - min(data)) / max(1, quants - 1)
    # квантование
    def quantize(self, data, step):
        return np.round([(i - min(data)) / step for i in data])
    # восстановление
    def resotre(self, data, step, _min):
        return [i * step + _min for i in data]
    # нахождение интервала квантов
    def set_intervals(self, step, quant, _min):
        return [step * i + _min for i in range(quant)]
    # функция отрисовки графиков
    def paint_plot(self, data, restored_data, intervals):
        for i in range(len(intervals)):
            plt.plot([0, len(restored_data)], [intervals[i], intervals[i]], color = '#000000')
        plt.plot(data, marker='o', ls='-', color='red')
        plt.plot(restored_data, marker='o', color='#4682b4')
        plt.show()
    def get_info(self, data, resotred_data):
        print('mse: ', mse(data, resotred_data))
        print('entropy of data: ', entropy(data))
        print('entropy of restored data: ', entropy(data))

class UnevenScalarQuantizer(UniformScalarQuantizer):
    '''
    Количество квантов: такое же как в предыдущей части задания. 
    Использовать неравномерный скалярный квантователь построенный по алгоритму Ллойда-Макса.
    Найти среднеквадратичную ошибку и энтропию. Сравнить с равномерным скалярным квантователем. 
    Интерпретировать результат сравнения.
    '''
    def __init__(self):
        self.mu = 5
        self.sigma = 1
        self.size = 100
        self.quants = 8
        self.data = self.create_data(self.mu, self.sigma, self.size)
        self.copydata = deepcopy(self.data)
        pass
    def call(self):
        centroids, clusters = self.predict(self.data, self.quants)
        centroids = sorted(centroids)
        _min = min(self.data)
        restored_data = self.quantize(self.copydata, centroids)
        restored_data = np.clip(restored_data, min(centroids), max(centroids))
        # self.paint_plot(self.copydata, restored_data, centroids)
        self.get_info(self.copydata, restored_data)
        pass
    # функция выбора интервала
    def set_intervals(self, data, centroid, ax = 1):
        return np.linalg.norm(data - centroid, axis = ax)
    # функция для определния центроидов и принадлежности к кластерам
    def predict(self, data, quants):
        size = len(data)
        data_uniq = np.unique(data)
        data_uniq_num = [i for i in range(len(np.unique(data)))]
        centroids = random.choice(data, quants, replace = False)
        clusterts = np.zeros(size)
        for k in range(size):
            for j in range(quants):
                if data[k] == data_uniq[j]:
                    data[k] = data_uniq_num[j]
            clusterts[k] = data[k]
        while True:
            centroids_old = deepcopy(centroids)
            err = self.set_intervals(centroids, centroids_old, None)
            if err == 0:
                clusterts = clusterts.astype(int)
                centroids = centroids
                return centroids, clusterts
    # квантование по центроидам
    def quantize(self, data, centroids):
        for i in range(len(data)):
            for k in range(len(centroids) - 1):
                if (data[i] > centroids[k] and (data[i] < centroids[k + 1])):
                    data[i] = centroids[k]
        return data
    # подсчет энтропии
    def entropy(self, data, base = None):
        value, counts = np.unique(data, return_counts = True)
        norm_counts = counts / counts.sum()
        base = np.e if base is None else base
        return -(norm_counts * np.log(norm_counts)/np.log(base)).sum()
    def get_info(self, data, resotred_data):
        print('mse: ', mse(data, resotred_data))
        print('entropy of data: ', self.entropy(data)) 
        print('entropy of restored data: ', self.entropy(data))

class VectorQuantizer:
    '''
    Проквантовать сгенерированную последовательность векторным квантователем. 
    Параметры кодовой книги – 8 слов по 2 элемента. 
    Оптимальная кодовая книга строится при помощи алгоритма Линде-Бузо-Грея (Linde-Buzo-Gray algorithm) – обобщение алгоритма Ллойда-Макса. 
    Аналог этого алгоритма: k-means.
    '''
    def __init__(self):
        self.mu = 0
        self.sigma = 1
        self.rows = 100
        self.cols = 2
        self.quants = 8
        self.error = .5 * 10**(-4)
        self.max_iter = 3000
        self.dataset = self.create_data(self.mu, self.sigma, self.rows, self.cols)

    def call(self):
        vq_lg = LBG(self.dataset, self.quants, self.error, self.max_iter)
        vq_lg.run()
        codebook = vq_lg.get_codebook()
        df = pd.DataFrame(data = self.dataset, columns = ['x', 'y'], index = range(self.rows))
        centroids = pd.DataFrame(data = codebook, columns = ['x', 'y'], index = range(self.quants))
        print(codebook)
        self.paint_plot(df, centroids)
    # генерация выборки 
    def create_data(self, mu, sigma, rows, cols):
        return np.random.normal(mu, sigma, (rows, cols))
    def paint_plot(self, df, centroids):
        plt.scatter('x', 'y', color = 'g', data = df)
        plt.scatter('x', 'y', color = 'b', data = centroids)
        plt.show()

class CLASTER:
    def __init__(self, centroid):
        self.patterns = []
        self.centroid = centroid
    # добавление паттернов
    def add_pattern(self, pattern):
        self.patterns.append(pattern)
    # установление центроидов
    def set_centroid(self, sentroid):
        self.centroid = sentroid
    # обновление центроидов
    def update_centroid(self):
        if len(self.patterns) != 0:
            pattern_matrix = np.asanyarray(self.patterns)
            mean_matrix = pattern_matrix.mean(0)
            self.centroid = list(mean_matrix)
    def set_intervals(self, pattern):
        return np.linalg.norm(np.asanyarray(self.centroid) - np.asanyarray(pattern))
    def clear_patterns(self):
        self.patterns = []
    def get_partial_distortion(self):
        partial_distortion = 0
        for index in range(len(self.patterns)):
            partial_distortion += np.linalg.norm(np.asanyarray(self.centroid) - np.asanyarray(self.patterns[index]))
        return partial_distortion
    def print_cluster(self):
        print("Centroids: ", self.centroid)

class LBG:
    def __init__(self, dataset, quants, error, iters):
        self.dataset = dataset
        self.quants = quants
        self.error = error
        self.iters = iters
        self.old_distortion = 0
        self.new_distortion = 0
        self.clusters = []
        self.codebook = []
    def run(self):
        self.generate_clusters()
        iters_partial = 1
        self.print_cluster()
        for i in range(2):
            self.clean_clusters()
            self.allocate_closest_cluster()
            self.update_centroid()
            self.set_distortion()
            iters_partial += 1
        while (iters_partial < self.iters) and (self.get_distortion_flag() > self.error):
            self.clean_clusters()
            self.allocate_closest_cluster()
            self.update_centroid()
            self.set_distortion()
            iters_partial += 1
        self.set_codebook()
    
    def set_codebook(self):
        for index in range(len(self.clusters)):
            self.codebook.append(self.clusters[index].centroid)
    
    def get_codebook(self):
        return np.asanyarray(self.codebook)
    
    def clean_clusters(self):
        for index in range(len(self.clusters)):
            self.clusters[index].clear_patterns()
    
    def add_clusters(self, centroid):
        cluster = CLASTER(centroid)
        self.clusters.append(cluster)
    
    def generate_clusters(self):
        indexes = np.random.choice(range(len(self.dataset)), self.quants, replace=False)
        for index in indexes:
            self.add_clusters(list(self.dataset[index]))
    
    def allocate_closest_cluster(self):
        for pattern in self.dataset:
            lowest_interval = float('inf')
            lowest_index = -1
            for index in range(len(self.clusters)):
                interval = self.clusters[index].set_intervals(list(pattern))
                if interval < lowest_index:
                    lowest_interval = interval
                    lowest_index = index
            self.clusters[lowest_index].add_pattern(list(pattern))
    
    def update_centroid(self):
        for index in range(len(self.clusters)):
            self.clusters[index].update_centroid()
    
    def set_distortion(self):
        distortion = 0
        for index in range(len(self.clusters)):
            distortion += self.clusters[index].get_partial_distortion()
        self.old_distortion = self.new_distortion
        self.new_distortion = distortion
    
    def get_distortion_flag(self):
        return (self.old_distortion - self.new_distortion) / self.new_distortion
    
    def print_cluster(self):
        for cluster in self.clusters:
            cluster.print_cluster()

if __name__ == '__main__':
    # UniformScalarQuantizer().call()
    # UnevenScalarQuantizer().call()
    VectorQuantizer().call()
    
    

