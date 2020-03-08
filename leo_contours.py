import os as os
import cv2 as cv
import numpy as np
from os import walk
import time as time
import random as r



file = '/home/silkking/Workspace/Anses/Leo/filter_captcha/00710_filtered.jpg'
mypath = '/home/silkking/Workspace/Anses/Leo/filter_captcha/'
saveRoute = '/home/silkking/Workspace/Anses/'
badRects = 0
goodRects = 0
# saveName = 'img_edges.jpg'
filesParameters = []
for filenames in os.listdir(mypath):
	letterParameters = []
	letterParameters.append(filenames)
	# print(filenames)
	img = cv.imread(mypath + filenames)

	edged = cv.Canny(img, 30, 150)

	# print(edged, len(edged), len(edged[0]))
	# cv.imwrite('/home/silkking/Workspace/Captcha reader/img_edges.jpg',edged)

	(image, cnts, _) = cv.findContours(edged.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

	contours = cv.drawContours(img, cnts, -1, (255,255,255), 1)
	#print(cnts)
	# print(len(cnts),len(cnts[0]), len(cnts[1]), len(cnts[2]))
	cv.imshow("Contours", contours)

	# cv.imwrite(saveRoute + saveName,contours)

	# print(img.shape)
	color = (255, 0, 255) 

	# Line thickness of 2 px 
	thickness = 1
	new_im = ""
	
	for index, letter in enumerate(cnts):
		minX = 0
		minY = 0
		maxX = 0
		maxY = 0
		for indexWidth, pointsXY_feo in enumerate(letter):
				pointsXY = pointsXY_feo[0]
				if(indexWidth == 0):
					
					minX = pointsXY[0]
					maxX = pointsXY[0]
					minY = pointsXY[1]
					maxY = pointsXY[1]
				else:
					if(pointsXY[0] < minX):
						minX = pointsXY[0]
					if(pointsXY[0] > maxX):
						maxX = pointsXY[0]
					if(pointsXY[1] < minY):
						minY = pointsXY[1]
					if(pointsXY[1] > maxY):
						maxY = pointsXY[1]
		
		limitXMax = 21
		limitMinX = 7
		limitMinY = 16
		# if(maxX - minX > limitXMax):
		# 	divide = 2
		# 	while((maxX - minX)/divide > limitXMax):
		# 		divide += 1
		# 	for rectIndex in range(divide):
		# 		img = cv.rectangle(img, (minX + int((maxX - minX)/divide) * rectIndex, minY), (minX + int((maxX - minX)/divide) * (rectIndex+1),maxY), color=color, thickness=thickness)	
		# 	# img = cv.rectangle(img, (int((maxX + minX)/2), minY), (maxX,maxY), color=color, thickness=thickness)
		# 	rects += divide
		if(maxX - minX > limitMinX and maxY - minY > limitMinY):
			letterParameters.append([(minX, minY), (maxX,maxY)])
	


	filesParameters.append(letterParameters)
goodFiles = []

for index, params in enumerate(filesParameters):
	newParams = []
	newParams.append(params[0])
	rects = 0	
	minX = 0
	minY = 0
	maxX = 0
	maxY = 0
	img = cv.imread(mypath + params[0])
	for i in range(1, len(params)):
		if(i == 1):
			minX = params[i][0][0]
			maxX = params[i][1][0]
			minY = params[i][0][1]
			maxY = params[i][1][1]
		else:
			if(params[i][0][0] < minX):
				minX = params[i][0][0]
			if(params[i][1][0] > maxX):
				maxX = params[i][1][0]
			if(params[i][0][1] < minY):
				minY = params[i][0][1]
			if(params[i][1][1] > maxY):
				maxY = params[i][1][1]
	avgSizeX = (maxX - minX) / 6 * 1.1
	# print(maxX, minX, params)
	# exit()

	for i in range(1, len(params)):
		minX = params[i][0][0]
		maxX = params[i][1][0]
		rectsToDivideInto = max(int(round((maxX - minX) / avgSizeX, 0)), 1)

		# print(rectsToDivideInto)
		rects += rectsToDivideInto
		for rect in range(rectsToDivideInto):
			rectMinX = minX + rect * (maxX - minX) / rectsToDivideInto 
			rectMaxX = minX + (rect + 1) * (maxX - minX) / rectsToDivideInto 
			# img = cv.rectangle(img, (rectMinX, minY), (rectMaxX,maxY), color=color, thickness=thickness)
			newParams.append([(rectMinX, minY), (rectMaxX,maxY)])




	if(rects != 6):
		# cv.imwrite(saveRoute + 'letters/bads/' + params[0], img)
		badRects += 1
		# print(params[0], rects)
	else: 
		goodFiles.append(newParams)
		# cv.imwrite(saveRoute + 'letters/goods/' + params[0], img)
		goodRects += 1
	
for ind, params in enumerate(goodFiles):
	img = cv.imread(mypath + params[0])
	letters = list(params[0].split("_")[0])
	# print(letters)
	for i in range(1,len(params)):
		# im1 = im.crop((left, top, right, bottom)) 
		# print(params[i][0][0],params[i][1][0], params[i][0][1],params[i][1][1])
		crop_img = img[params[i][0][0]:params[i][1][0], params[i][0][1]:params[i][1][1]]
		# print(crop_img)
		cv.imwrite('letters/goods/' + letters[i - 1] + '/' + str(r.randint(0, 1000000)) + '.jpg', crop_img)

# print(badRects, goodRects)

# print(new_im)
# cv.imshow("Contours", new_im)
			
