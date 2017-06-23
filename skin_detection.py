import sys
import cv2
import numpy as np

def erode_dilate(img):
	kernel=np.ones((3, 3), np.uint8)
	img_enhanced=cv2.erode(img, kernel, iterations=1)
	img_enhanced=cv2.dilate(img_enhanced, kernel, iterations=1)

	return img_enhanced


def filter(img):
	img_hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	(h, s, v)=cv2.split(img_hsv)

	img=np.float32(img)
	(b, g, r)=cv2.split(img)

	for (x, y), _ in np.ndenumerate(b):
		if (	(b[x, y]>160 and r[x, y]<180 and g[x, y]<180) or
				(g[x, y]>160 and r[x, y]<180 and b[x, y]<180) or
				(b[x, y]<100 and r[x, y]<100 and g[x, y]<100) or
				(g[x, y]>200) or
				#(r[x, y]+g[x, y]>400) or
				#(g[x, y]>150 and b[x, y]<90) or
				(b[x, y]/(b[x, y]+g[x, y]+r[x, y])>0.4) or
				(g[x, y]/(b[x, y]+g[x, y]+r[x, y])>0.4) or
				(r[x, y]<102 and 100<g[x, y]<140 and 110<b[x, y]<160)):
			b[x, y]=r[x, y]=g[x, y]=0
		elif not(0<=h[x, y]<=20 and 30<=s[x, y]<=255 and 80<=v[x, y]<=255):
			b[x, y]=r[x, y]=g[x, y]=0
		else:
			b[x, y]=r[x, y]=g[x, y]=255

	img_filtered=cv2.merge((b, g, r))
	img_filtered=cv2.convertScaleAbs(img_filtered)

	return img_filtered
			


def calibrate(img):
	img_hls=cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
	img_hls=np.float32(img_hls)
	(h, l, s)=cv2.split(img_hls)

	max_s=np.amax(s)
	min_s=np.amin(s)
	max_h=np.amax(h)
	s=(s-min_s)/(max_s-min_s)*255
	#h=(h-min_s)/(max_h-min_s)

	img_calibrated=cv2.merge((h, l, s))
	img_calibrated=cv2.convertScaleAbs(img_calibrated)
	img_calbgr=cv2.cvtColor(img_calibrated, cv2.COLOR_HLS2BGR)

	return img_calbgr

def keep_skin(img):
	img_cal=calibrate(img)
	img_fil=filter(img_cal)
	img_enh=erode_dilate(img_fil)

	return img_enh


def main():
	if len(sys.argv)!=2:
		print("usage: python3 skin_detection.py file_name")
		exit()

	img=cv2.imread(sys.argv[1])

	img_skin=keep_skin(img)

	cv2.imshow("Original", img)
	cv2.imshow("Result", img_skin)
	cv2.waitKey(0)


if __name__=="__main__":
    main()