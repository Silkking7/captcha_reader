import cv2
import numpy as np

im_path = 'captcha_1.jpeg'

image = cv2.imread(im_path, 1)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# print(gray.at<uchar>(0,0))
print(gray.size)
print(gray[0,0])



mean = np.mean(gray)


def point_close_to_rect(x,y, letter):
	x_axis = (x+1 >= letter[0][0]) and (x-1 <= letter[0][1])
	y_axis = (y+1 >= letter[1][0]) and (y-1 <= letter[1][1])
	return bool(x_axis and y_axis)

def get_new_rect(x,y,letter):
	new_min_x = np.minimum(x, letter[0][0])
	new_min_y = np.minimum(y, letter[0][1])
	new_max_x = np.maximum(x, letter[1][0])
	new_max_y = np.maximum(y, letter[1][1])
	return (new_min_x, new_min_y), (new_max_x, new_max_y)

# Una letra va a estar contenida en un rectangulo donde se especifica la esquina superior izquierda e inferior derecha
# print(np.min(gray))
add = 3
mean = 37
init_x = 0
init_y = 0
letters = []

for i in range(0, len(gray)):
	for j in range(0, len(gray[i])):
		if(gray[i,j] < mean):
			print(gray[i,j])
			point_added = False
			print("New point found", i, j)

			for index, letter in enumerate(letters):
				if(point_close_to_rect(i,j,letter)):
					letters[index] = get_new_rect(i,j,letter)
					point_added = True
					break

			if(not point_added and len(letters) < 6):
				print("Adding new letter")
				letters.append(((i,j), (i+ init_x,j+init_y)))
			elif(len(letters) == 6):
				print("Letter quantity", len(letters))
				print("Excceded 6 letters and have a black x,y", i, j)

# for i in range(0, len(gray)):
# 	for j in range(0, len(gray[i])):
# 		if(gray[i,j] < mean):
# 			print(gray[i,j])
# 			point_added = False
# 			print("New point found", i, j)

# 			for index, letter in enumerate(letters):
# 				if(point_close_to_rect(i,j,letter)):
# 					letters[index] = get_new_rect(i,j,letter)
# 					point_added = True
# 					break

# 			if(not point_added and len(letters) < 6):
# 				print("Adding new letter")
# 				letters.append(((i,j), (i+ 19,j+3)))
# 			elif(len(letters) == 6):
# 				print("Letter quantity", len(letters))
# 				print("Excceded 6 letters and have a black x,y", i, j)
# Blue color in BGR 
color = (255, 0, 255) 
print(letters)
# Line thickness of 2 px 
thickness = 1
new_im = image
for index, letter in enumerate(letters):
	print("Drawing rect in letter")
	x = letter[0][0]
	y = letter[0][1]
	xw = letter[1][0]
	yh = letter[1][1]
	# new_im = cv2.rectangle(new_im, letter[0], letter[1], color=(255, 0, 255), thickness=thickness)
	new_im = cv2.rectangle(image, (letter[0][1], letter[0][0]), (letter[1][1],letter[1][0]), color=color, thickness=thickness)
	crop_img = image[x:xw, y:yh]
	cv2.imwrite('letters/letter_' + str(index) + '.jpg', crop_img)
# resized = cv2.resize(new_im, (75, 250), interpolation = cv2.INTER_AREA) 
# cv2.imshow("cropped", resized)

# if(len(letters) < 6):
# 	print("WARNING, less than 6 letters")
# image = cv2.imread('letters/letter_' + str(len(letters) - 1) + '.jpg', 1)
resized = cv2.resize(image, (500, 150), interpolation = cv2.INTER_AREA) 
cv2.imshow('image',resized)
# cv2.resizeWindow('image', 600,600)
cv2.waitKey(0)
cv2.destroyAllWindows()
        	