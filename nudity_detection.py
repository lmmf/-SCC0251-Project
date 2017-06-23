import sys
import cv2

#import de arquivo local
import analyze_image as ai

def nudity(img):
	percentage=ai.skin_percentage(img)

	return True if percentage>=23 else False


def main():	
	if len(sys.argv)!=2:
		print("usage: python3 nudity_detection.py file_name")
		exit()

	img=cv2.imread(sys.argv[1])

	if nudity(img):
		print("This image probably contains nudity.")
	else:
		print("This image probably does not contain nudity.")


if __name__=="__main__":
    main()