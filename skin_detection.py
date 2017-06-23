#run with "python skin_detection.py file_name"
#file_name is the image to be analyzed, it must be in the same folder as this

#SCC0251 - Processamento de Imagens
#PROJETO FINAL
#Identificação de nudez ou pornografia em imagens
#Nome								Número USP
#Felipe Kazuyoshi Takara 			8921026
#Leonardo Mellin Moreira Ferreira 	7982767

#The color values for skin were based out of these articles:
#https://goo.gl/vUSKaj
#https://goo.gl/oCdw2V

import sys
import cv2
import numpy as np

def erode_dilate(img):
	#the kernel is chosen
	kernel=np.ones((3, 3), np.uint8)
	#the image is eroded and then dilated, it is done to reduce unwanted small skin portions
	img_enhanced=cv2.erode(img, kernel, iterations=1)
	img_enhanced=cv2.dilate(img_enhanced, kernel, iterations=1)

	return img_enhanced


def filter(img):
	#the image is converted and split into hue, saturation and value
	img_hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	(h, s, v)=cv2.split(img_hsv)

	#the image is split into blue, green and red
	img=np.float32(img)
	(b, g, r)=cv2.split(img)

	#iterate through every pixel in the image and remove unwanted colors
	for (x, y), _ in np.ndenumerate(b):
		if (	(b[x, y]>160 and r[x, y]<180 and g[x, y]<180) or #too blue
				(g[x, y]>160 and r[x, y]<180 and b[x, y]<180) or #too green
				(b[x, y]<100 and r[x, y]<100 and g[x, y]<100) or #too dark
				(g[x, y]>200) or #green
				#the following two were not used because they worsen detection
				#(r[x, y]+g[x, y]>400) or #close to yellow
				#(g[x, y]>150 and b[x, y]<90) or #próximo ao amarelo
				(b[x, y]/(b[x, y]+g[x, y]+r[x, y])>0.4) or #too blue
				(g[x, y]/(b[x, y]+g[x, y]+r[x, y])>0.4) or #too green
				(r[x, y]<102 and 100<g[x, y]<140 and 110<b[x, y]<160)): #ocean
			b[x, y]=r[x, y]=g[x, y]=0 #values that do not fit are turned to black
		#skin values in hsv
		elif not(0<=h[x, y]<=20 and 30<=s[x, y]<=255 and 80<=v[x, y]<=255):
			b[x, y]=r[x, y]=g[x, y]=0 #values that do not fit are turned to black
		else:
			b[x, y]=r[x, y]=g[x, y]=255 #other values are turned to white

	#the colors are merged back into one image
	img_filtered=cv2.merge((b, g, r))
	img_filtered=cv2.convertScaleAbs(img_filtered)

	return img_filtered
			


def calibrate(img):
	#the image color system is converted to HLS
	img_hls=cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
	img_hls=np.float32(img_hls)
	#the image is split into hue, luminosity and saturation
	(h, l, s)=cv2.split(img_hls)

	#the max and min values for saturation and hue are defined
	max_s=np.amax(s)
	min_s=np.amin(s)
	max_h=np.amax(h)
	#saturation is normalized
	s=(s-min_s)/(max_s-min_s)*255
	#hue should be normalized, but it worsens detection
	#h=(h-min_s)/(max_h-min_s)

	#the channels are merged back into an image
	img_calibrated=cv2.merge((h, l, s))
	img_calibrated=cv2.convertScaleAbs(img_calibrated)
	#the image is converted back to RGB
	img_calbgr=cv2.cvtColor(img_calibrated, cv2.COLOR_HLS2BGR)

	return img_calbgr

def keep_skin(img):
	#calibrates colors
	img_cal=calibrate(img)
	#filter skin
	img_fil=filter(img_cal)
	#remove noise
	img_enh=erode_dilate(img_fil)

	return img_enh


def main():
	#the image name must be passed by the user
	if len(sys.argv)!=2:
		print("usage: python3 skin_detection.py file_name")
		exit()

	#reads image
	img=cv2.imread(sys.argv[1])

	#apply skin detection algorithm
	img_skin=keep_skin(img)

	#shows original and result images
	cv2.imshow("Original", img)
	cv2.imshow("Result", img_skin)
	cv2.waitKey(0)
	cv2.destroyAllWindows()


if __name__=="__main__":
    main()