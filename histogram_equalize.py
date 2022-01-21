## HISTOGRAM EQUALIZER
import cv2
import numpy as np
import os

def my_hist_equalizer(img):
    arr = np.zeros((256))
    row, col = img.shape
    new_img = np.zeros((row,col))

    ''' Creating Frequency array named "arr" '''
    for i in range(row):
        for j in range(col):
            arr[img[i,j]] += 1
        
    sorted_pixel = list(set(sorted(img.flatten())))
    min_freq, max_freq = min(arr) , max(arr)

    '''Creating Cumulative density function (cdf) Array'''
    cdf = []
    for i in range(len(sorted_pixel)):
        if len(cdf) != 0:
            cdf.append(cdf[-1] + arr[sorted_pixel[i]])
        else:
            cdf.append(arr[sorted_pixel[i]])

    ''' Creating hv Values for corresponding pixels'''        
    hv = []
    min_cdf= min(cdf)
    for i in cdf:
        hv.append(round(((i - min_cdf)/ (row*col - min_cdf)) * 255 ))

    ''' This dictionary holds the current pixel value (key) and its hv Value (value)'''
    pixel_hv_dict = dict(zip(sorted_pixel, hv))

    for i in range(row):
        for j in range(col):
            new_img[i,j] = pixel_hv_dict[img[i,j]]
    return new_img


path = "dataset"
imagePaths = [os.path.join(path,f) for f in os.listdir(path)]

for image in imagePaths:
    img = cv2.imread(image, 0)
    new_img_arr = my_hist_equalizer(img)

    cv2.imwrite(image.split('/')[-1] , new_img_arr)
    print(new_img_arr)
