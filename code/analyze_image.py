#run with "python analyze_image.py"
#skin_detection.py, must be in the same folder as this and the folder image_samples must be in the superfolder
#image_samples must contain the 15 images on each subfolder (nudity and non_nudity)

#SCC0251 - Processamento de Imagens
#PROJETO FINAL
#Identificação de nudez ou pornografia em imagens
#Nome								Número USP
#Felipe Kazuyoshi Takara 			8921026
#Leonardo Mellin Moreira Ferreira 	7982767

import cv2

#import local file
import skin_detection as sd

def skin_percentage(img):
	#the skin is detected and image is split into its color channels
	img=sd.keep_skin(img)
	(b, _, _)=cv2.split(img)

	#skin is the amount of skin pixels (counts how many white pixels there are)
	skin=sum(sum(b/255))
	#total is the total area (pixels in the matrix)
	total=len(b)*len(b[0])

	#percentage of skin in total area
	percentage=skin/total*100

	return percentage


def main():
	#open every sample image (both nudity and non-nudity) and analyzes it
	with open("../image_samples/non_nudity/percentages.txt", 'w') as fp:
		for i in range(1, 16):
			img=cv2.imread("../image_samples/non_nudity/image"+str(i)+".jpg")
			#the percentage of skin for each image is written in a file
			fp.write("%.2f\n" % skin_percentage(img))
	with open("../image_samples/nudity/percentages.txt", 'w') as fp:
		for i in range(1, 16):
			img=cv2.imread("../image_samples/nudity/image"+str(i)+".jpg")
			#the percentage of skin for each image is written in a file
			fp.write("%.2f\n" % skin_percentage(img))


if __name__=="__main__":
    main()