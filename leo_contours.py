import os as os
import cv2 as cv
import numpy as np
from os import walk
import time as time
import random as r
from clases.fileLetters import FileLetters
from clases.rect import Rect

import sys

# print(sys.path)

mypath = '/home/silkking/Workspace/Anses/Leo/filter_captcha/'

def generateContours(filename):	
	img = cv.imread(mypath + filename)

	edged = cv.Canny(img, 30, 150)

	(image, cnts, petesParaTodos) = cv.findContours(edged.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
	return cnts

def isRectBigEnough(rect):
	limitXMax = 21
	limitMinX = 7
	limitMinY = 6
	return rect.maxX - rect.minX > limitMinX and rect.maxY - rect.minY > limitMinY

def generateRectParams(filename):
	fileLetters = FileLetters(filename, [])

	cnts = generateContours(filename)
	for index, letter in enumerate(cnts):
		rect = Rect(0, 0, 0, 0)
		for indexWidth, pointsXY_feo in enumerate(letter):
				pointsXY = pointsXY_feo[0]
				if(indexWidth == 0):
					rect = Rect(pointsXY[0],pointsXY[0] , pointsXY[1], pointsXY[1])
				else:
					if(pointsXY[0] < rect.minX):
						rect.minX = pointsXY[0]
					if(pointsXY[0] > rect.maxX):
						rect.maxX = pointsXY[0]
					if(pointsXY[1] < rect.minY):
						rect.minY = pointsXY[1]
					if(pointsXY[1] > rect.maxY):
						rect.maxY = pointsXY[1]
		
		if(isRectBigEnough(rect)):
			fileLetters.addToList(rect)
	return fileLetters

def cropLetter(params):
	pass

filesParameters = []
color = (255, 0, 255) 

thickness = 1
print(len(os.listdir(mypath)))
for filename in os.listdir(mypath):
	fileLetters = generateRectParams(filename)
	fileLetters.sortLetters()
	filesParameters.append(fileLetters)

for i in range(0,len(filesParameters)):
	if len(filesParameters[i].letters) == 6:
		image = cv.imread(mypath + filesParameters[i].filename)
		fileParams = filesParameters[i]
		for j in range(0,6):
			letras = fileParams.letters[j]
			new_im = image[letras.minY:letras.maxY, letras.minX:letras.maxX]
			cv.imwrite('letters/goods/' + str(fileParams.filename)[j] + '/' + str(r.randint(0, 1000000)) + '.jpg', new_im)


