import numpy as np
import cv2

img1 =cv2.imread("test1_1.jpg",cv2.IMREAD_GRAYSCALE)
img2 =cv2.imread("test1_2.jpg",cv2.IMREAD_GRAYSCALE)
img1 = cv2.resize(img1, None, fx=1.5, fy=2, interpolation=cv2.INTER_CUBIC)
img2 = cv2.resize(img2, None, fx=1.5, fy=2, interpolation=cv2.INTER_CUBIC)
res = None


orb=cv2.ORB_create()
kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(img2,None)



bf= cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
matches=bf.match(des1,des2)



matches = sorted(matches, key=lambda x:x.distance)
res=cv2.drawMatches(img1,kp1,img2,kp2,matches[:10],res,flags=0)



cv2.imshow("Feature Matching",res)

cv2.imwrite("test1.jpg",res)


cv2.waitKey(0)
cv2.destroyAllWindows()
