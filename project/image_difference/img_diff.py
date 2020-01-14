# import the necessary packages
from skimage.measure import compare_ssim
import argparse
import imutils
import cv2
import numpy as np

# load the two input images
imageA = cv2.imread("sam5.jpg")
imageB = cv2.imread("sam6.jpg")
#imageB = cv2.bitwise_not(imageA)

def ssim(imageA,imageB):
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score,diff) = compare_ssim(grayA, grayB, full=True)
    return score

def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    res = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    res /= float(imageA.shape[0] * imageA.shape[1])

    return res

def psnr(imageA, imageB):
    mse = np.mean( (imageA - imageB) ** 2 )
    if mse == 0:
        return 100
    else:
        return cv2.PSNR(imageA, imageB)

s = ssim(imageA, imageB)
print("SSIM: {}".format(s))

m = mse(imageA, imageB)
print("MSE: {}".format(m))

d=psnr(imageA, imageB)
print("PSNR: {}".format(d))

# show the output images
cv2.imshow("Original", imageA)
cv2.imshow("Modified", imageB)
cv2.waitKey(0)