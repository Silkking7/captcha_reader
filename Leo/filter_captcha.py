import os as os
import cv2 as cv
import numpy as np

cwd = os.getcwd()
file_list =  os.listdir(cwd)
file_list.pop(0)
# file_list.pop(0)
file_list.pop(-1)
print(file_list)

kernel = np.ones((3,2),np.uint8)

for i in range(0,len(file_list)):
	if file_list[i][0] in '0123456789':
		img = cv.imread(file_list[i]) # Importing Sample Test Image
		blue = img[:,:,1]
		ret, thresh1 = cv.threshold(blue, 150, 255, cv.THRESH_BINARY_INV) 
		dilation = cv.dilate(thresh1,kernel,iterations = 1)
		cv.imwrite(cwd + '/filter_captcha/' + file_list[i].split("_")[0] + '_filtered.jpg',dilation)
