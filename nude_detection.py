import sys
import cv2

import analyze_image as ai

def nudity(img):
	percentage=ai.skin_percentage(img)

	if percentage>=20:
		return True
	else:
		return False


def main():	
	if len(sys.argv)!=2:
		print("usage: python3 nude_detection.py file_name")
		exit()

	img=cv2.imread(sys.argv[1])

	if nudity(img):
		print("This image probably contains nudity.")
	else:
		print("This image probably does not contain nudity.")


if __name__=="__main__":
    main()