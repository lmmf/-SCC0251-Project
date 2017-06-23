#wun with "python demo.py"

import cv2

#import local file
import skin_detection as sd

#the function is written again here because the skin was already detected in main
#if the original one was used, it would run much slower (detect skin twice)
def skin_percentage(img):
	#the image is split into its color channels
	(b, _, _)=cv2.split(img)

	#skin is the amount of skin pixels (counts how many white pixels there are)
	skin=sum(sum(b/255))
	#total is the total area (pixels in the matrix)
	total=len(b)*len(b[0])

	#percentage of skin in total area
	percentage=skin/total*100

	return percentage


#the function is written again here because the skin was already detected in main
#if the original one was used, it would run much slower (detect skin twice)
def nudity(percentage):
	#23 was found to be a good amount
	return True if percentage>=23 else False


def main():
	#read the two images in the main folder
	img1=cv2.imread("image1.jpg")
	img2=cv2.imread("image2.jpg")

	#detects the skin
	img1_skin=sd.keep_skin(img1)
	img2_skin=sd.keep_skin(img2)

	#calculates the percentage
	percentage1=skin_percentage(img1_skin)
	percentage2=skin_percentage(img2_skin)

	#prints the final result and the percentage of skin
	if nudity(percentage1):
		print("Image 1 probably contains nudity, as there is "+
			"%.2f%% skin showing." % percentage1)
	else:
		print("Image 1 probably does not contain nudity, as there is "+
			"%.2f%% skin showing." % percentage1)
	if nudity(percentage2):
		print("Image 2 probably contains nudity, as there is "+
			"%.2f%% skin showing." % percentage2)
	else:
		print("Image 2 probably does not contain nudity, as there is "+
			"%.2f%% skin showing." % percentage2)

	#shows the original and resulting image for image1.jpg
	cv2.imshow("Image 1 original", img1)
	cv2.imshow("Image 1 result", img1_skin)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

	#shows the original and resulting image for image2.jpg
	cv2.imshow("Image 2 original", img2)
	cv2.imshow("Image 2 result", img2_skin)
	cv2.waitKey(0)
	cv2.destroyAllWindows()


if __name__=="__main__":
    main()