import cv2

import skin_detection as sd

def skin_percentage(img):
	img=sd.keep_skin(img)
	(b, g, r)=cv2.split(img)

	skin=sum(sum(b/255))
	total=len(b)*len(b[0])

	percentage=skin/total*100

	return percentage


def main():
	with open("image_samples/non_nudity/percentages.txt", 'w') as fp:
		for i in range(1, 16):
			img=cv2.imread("image_samples/non_nudity/image"+str(i)+".jpg")

			fp.write("%.2f\n" % skin_percentage(img))

	with open("image_samples/nudity/percentages.txt", 'w') as fp:
		for i in range(1, 16):
			img=cv2.imread("image_samples/nudity/image"+str(i)+".jpg")

			fp.write("%.2f\n" % skin_percentage(img))


if __name__=="__main__":
    main()