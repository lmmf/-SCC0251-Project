#run with "python nudity_detection.py file_name"
#file_name is the image to be analyzed, it must be in the same folder as this
#skin_detection.py and analyze_image.py must be in the same folder as this

#SCC0251 - Processamento de Imagens
#PROJETO FINAL
#Identificação de nudez ou pornografia em imagens
#Nome								Número USP
#Felipe Kazuyoshi Takara 			8921026
#Leonardo Mellin Moreira Ferreira 	7982767

import sys
import cv2

#import local file
import analyze_image as ai

def nudity(img):
	#the percentage is calculated
	percentage=ai.skin_percentage(img)

	#23% was the best value in our tests (20% wrong results for nudity and non-nudity)
	return True if percentage>=23 else False


def main():
	#the image name must be passed by the user
	if len(sys.argv)!=2:
		print("usage: python3 nudity_detection.py file_name")
		exit()

	#the image is read
	img=cv2.imread(sys.argv[1])

	#after analyzing the image and deciding, program informs the result to the user
	if nudity(img):
		print("This image probably contains nudity.")
	else:
		print("This image probably does not contain nudity.")


if __name__=="__main__":
    main()