import numpy as np
import math
import numpy.random as random
import matplotlib.pyplot as plt
import sys

#import mnist.py

from scipy import misc

class ConvolutionalLayer():
    cache = np.array([0])  #Used to store the values for back-propagation
    weights = np.array([0])  #Weights for each connection between neurons represented as a matrix

    def __init__(self, width, height, depth, filter_num, fsize, stride, zero_padding):
        #width, height = dimensions of input
        #depth = number of inputs
        #filters = number of filters, fsize = side length of filter
        #stride = number of units moved during convolution by filter
        #zero_padding = number of zero "outlines" to surround input with during convolution
        self.width = width
        self.height = height
        self.depth = depth
        self.filter_num = filter_num
        self.fsize = fsize
        self.stride = stride
        self.zero_padding = zero_padding

        self.filters = [[np.random.uniform(-1, 1, (self.fsize,self.fsize)) for layer in range(self.depth)] for filter_col in range(self.filter_num)]
        self.bias = np.random.uniform(0, 1, self.filter_num)
        #self.cache = np.zeros((rows,1))
        #self.weights = np.random.uniform(-np.sqrt(1./cols), np.sqrt(1./cols), (rows, cols+1))

        #self.mem_weights = np.zeros(self.weights.shape)

        #self.filters =
    def forward(self, inputArr):
        #filters = list of all filters
        #outputs = list(?) of outputs
        self.o_width = int((self.width - self.fsize)/self.stride) + 1
        self.o_height = int((self.height - self.fsize)/self.stride) + 1


        output = np.zeros((self.filter_num, o_height, o_width))

        for f in range(self.filter_num):
            for layer in range(self.depth):
                for i in range(self.o_height):
                    for j in range(self.o_width):
                        #section = input section (x_ij)
                        #section = np.zeros((self.fsize,self.fsize))

                        section = inputArr[i*self.stride:i*self.stride + self.fsize:1, j*self.stride:j*self.stride + self.fsize:1, layer]
                        """
                        for m in range(self.fsize):
                            for n in range(self.fsize):
                                section[m][n] = inputArr[m + i*self.stride][n + j*self.stride][layer]
                        """
                        #print(np.shape(inputArr), np.shape(section), np.shape(self.filters[f][layer]))
                        output[f][i][j] += np.sum(np.multiply(section, self.filters[f][layer])) + bias[f] #use the proper filter for each one
                    #print(i)
                    #sys.stdout.flush()

        return output




    def backward(self, gradient):
        dzdx = np.zeros((self.o_height, self.o_width, self.depth))

        for f in range(self.filter_num):
            for layer in range(self.depth):
                dzdf = np.zeros((self.fsize, self.fsize))
                #dzdx = np.zeros((self.o_height, self.o_width))

                for i in range(self.fsize):
                    for j in range(self.fsize):
                        #iteration TODO
                        for m in range(self.o_height):
                            for n in range(self.o_width):
                                dzdf[i][j] += self.cache[i + m*self.stride][j + n*self.stride][layer] * gradient[m*self.stride][n*self.stride][f]
                                self.bias[f] += gradient[m*self.stride][n*self.stride][f]

                                dzdx[m][n][layer] += self.filters[f][layer][i][j] * gradient[m*self.stride - i][n*self.stride - j][f]

                self.filters[f][layer] += dzdw




        return dzdx


class MaxPoolingLayer():

    def __init__(self, chunk_width, chunk_height, averageValues=False):
        self.chunk_width = chunk_width
        self.chunk_height = chunk_height
        self.averageValues = averageValues

    def forward(self, inputArr):
        new_height = int(len(inputArr) / chunk_height)
        new_width = int(len(inputArr) / chunk_width)
        overhang_h = len(inputArr) % chunk_height
        overhang_w = len(inputArr) % chunk_width

        pooled_arr = np.zeros((len(inputArr), new_height, new_width))

        max_positions = [[np.zeros(2) for x in range(new_width + np.sign(overhang_w))] for y in range(new_height + np.sign(overhang_h))]

        for layer in range(len(inputArr)):
            for i in range(new_height + np.sign(overhang_h)):
                for j in range(new_width + np.sign(overhang_w)):
                    max_value = 0
                    max_x = 0
                    max_y = 0
                    for m in range(chunk_height if (i < new_height) else overhang_h):
                        for n in range(chunk_width if (j < new_width) else overhang_w):
                            if(inputArr[layer][i*chunk_height + m][j*chunk_width + n] > max_value):
                                max_value = inputArr[layer][i*chunk_height + m][j*chunk_width + n]
                                max_x = j*chunk_width + n
                                max_y = i*chunk_height + m
                    pooled_arr[layer][i][j] = max_value

    def backward(self, gradient):



test_layer = ConvolutionalLayer(820,500,3,2,10,1,0);
img = misc.imread("boi.png")

new_imgs = test_layer.forward(img)

print(new_imgs)

plt.imshow(new_imgs[0], interpolation='nearest')
plt.show()
