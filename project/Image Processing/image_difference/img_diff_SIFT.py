import cv2
import numpy as np

img1 = cv2.imread("test1.jpg")
img2 = cv2.imread("test2.jpg")

sift = cv2.xfeatures2d.SIFT_create()
kp_1, desc_1 = sift.detectAndCompute(img1, None)
kp_2, desc_2 = sift.detectAndCompute(img2, None)

index_params = dict(algorithm=0, trees=5)
search_params = dict() #checks=50
flann = cv2.FlannBasedMatcher(index_params, search_params)

matches = flann.knnMatch(desc_1, desc_2, k=2)

good_points = []
for m, n in matches:
    if m.distance < 0.6*n.distance: #factor : 0.6
        good_points.append(m)

number_keypoints = 0
if len(kp_1) <= len(kp_2):
    number_keypoints = len(kp_1)
else:
    number_keypoints = len(kp_2)


print("1st image keypoints: " + str(len(kp_1)))
print("2nd image keypoints: " + str(len(kp_2)))
print("good matches:", len(good_points))
print("good matches percentage: ", len(good_points) / number_keypoints * 100)

result = cv2.drawMatches(img1, kp_1, img2, kp_2, good_points, None)

cv2.imshow("result", cv2.resize(result, None, fx=0.4, fy=0.4))
cv2.imwrite("feature_matching_result.jpg", result)

cv2.imshow("1st image", cv2.resize(img1, None, fx=0.4, fy=0.4))
cv2.imshow("2nd image", cv2.resize(img2, None, fx=0.4, fy=0.4))
cv2.waitKey(0)
cv2.destroyAllWindows()