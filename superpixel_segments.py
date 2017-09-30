# -*- coding: UTF-8 -*- 
from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float
import matplotlib.pyplot as plt
import numpy as np
import argparse
import cv2
 
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
#segments为ndarray，假设图片大小为h*w，那么segments中就有h条list，每个list有w条元素，属于同一超级像素内的值也相同
segments = slic(img_as_float(image), n_segments = 50, sigma = 5)
#print segments.shape
#print segments[80].shape
#print segments[9]
 
# show the output of SLIC
fig = plt.figure("Superpixels")
ax = fig.add_subplot(1, 1, 1)
ax.imshow(mark_boundaries(img_as_float(cv2.cvtColor(image, cv2.COLOR_BGR2RGB)), segments))
plt.axis("off")
plt.show()

#unique去除掉数组中相同的值
for (i, segVal) in enumerate(np.unique(segments)):
	# construct a mask for the segment
	print segVal
	print "[x] inspecting segment %d" % (i)
	mask = np.zeros(image.shape[:2], dtype = "uint8")
	#print (segments == segVal)
	#这里是通过布尔值进行索引，即属于当前区域（segVal）内的mask值置为255
	mask[segments == segVal] = 255
 
	# show the masked region
	cv2.imshow("Mask", mask)
	cv2.imshow("Applied", cv2.bitwise_and(image, image, mask = mask))
	cv2.waitKey(0)