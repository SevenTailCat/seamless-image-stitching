# import the necessary packages
import numpy as np
import imutils
import cv2
class Stitcher:
    def __init__(self):
        # determine if we are using OpenCV v3.X
        self.isv3 = imutils.is_cv3()
    def stitch(self, images, ratio=0.9, reprojThresh=4.0,
        showMatches=False):
        # unpack the images, then detect keypoints and extract
        # local invariant descriptors from them
        (imageB, imageA) = images
        (kpsA, featuresA) = self.detectAndDescribe(imageA)
        (kpsB, featuresB) = self.detectAndDescribe(imageB)
        # match features between the two images
        M = self.matchKeypoints(kpsA, kpsB,
            featuresA, featuresB, ratio, reprojThresh)
        # if the match is None, then there aren't enough matched
        # keypoints to create a panorama
        if M is None:
            return None
        # otherwise, apply a perspective warp to stitch the images
        # together
        (matches, H, status) = M
        # and find the four top corners
        top = self.find_the_top(H, imageA.shape)
        last_w = int(min(top[0][0],top[1][0]))
        result = cv2.warpPerspective(imageA, H,(imageA.shape[1] + last_w, max(imageA.shape[0],imageB.shape[0])))
        # result[0:imageB.shape[0], 0:imageB.shape[1]] = imageB
        # print top
        result = self.two_in_one(result,imageB,max(top[0][0],top[1][0]),last_w)
        # check to see if the keypoint matches should be visualized
        if showMatches:
            vis = self.drawMatches(imageA, imageB, kpsA, kpsB, matches,
                status)
            # return a tuple of the stitched image and the
            # visualization
            return (result, vis)
        # return the stitched image
        return result
    def detectAndDescribe(self, image):
        # convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # check to see if we are using OpenCV 3.X
        if self.isv3:
            # detect and extract features from the image
            descriptor = cv2.xfeatures2d.SIFT_create()
            (kps, features) = descriptor.detectAndCompute(image, None)
        # otherwise, we are using OpenCV 2.4.X
        else:
            # detect keypoints in the image
            detector = cv2.FeatureDetector_create("SIFT")
            kps = detector.detect(gray)
            # extract features from the image
            extractor = cv2.DescriptorExtractor_create("SIFT")
            (kps, features) = extractor.compute(gray, kps)
        # convert the keypoints from KeyPoint objects to NumPy
        # arrays
        kps = np.float32([kp.pt for kp in kps])
        # return a tuple of keypoints and features
        return (kps, features)
    def matchKeypoints(self, kpsA, kpsB, featuresA, featuresB,
        ratio, reprojThresh):
        # compute the raw matches and initialize the list of actual
        # matches
        matcher = cv2.DescriptorMatcher_create("BruteForce")
        rawMatches = matcher.knnMatch(featuresA, featuresB, 2)
        matches = []
        # loop over the raw matches
        for m in rawMatches:
            # ensure the distance is within a certain ratio of each
            # other (i.e. Lowe's ratio test)
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                matches.append((m[0].trainIdx, m[0].queryIdx))
        # computing a homography requires at least 4 matches
        if len(matches) > 4:
            # construct the two sets of points
            ptsA = np.float32([kpsA[i] for (_, i) in matches])
            ptsB = np.float32([kpsB[i] for (i, _) in matches])
            # compute the homography between the two sets of points
            (H, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC,
                reprojThresh)
            # return the matches along with the homograpy matrix
            # and status of each matched point
            return (matches, H, status)
        # otherwise, no homograpy could be computed
        return None
    def drawMatches(self, imageA, imageB, kpsA, kpsB, matches, status):
        # initialize the output visualization image
        (hA, wA) = imageA.shape[:2]
        (hB, wB) = imageB.shape[:2]
        # print hA,wA,hB,wB
        vis = np.zeros((max(hA, hB), wA + wB, 3), dtype="uint8")
        vis[0:hA, 0:wA] = imageA
        vis[0:hB, wA:] = imageB
        # loop over the matches
        for ((trainIdx, queryIdx), s) in zip(matches, status):
            # only process the match if the keypoint was successfully
            # matched
            if s == 1:
                # draw the match
                ptA = (int(kpsA[queryIdx][0]), int(kpsA[queryIdx][1]))
                ptB = (int(kpsB[trainIdx][0]) + wA, int(kpsB[trainIdx][1]))
                cv2.line(vis, ptA, ptB, (0, 255, 0), 1)
        # return the visualization
        return vis
    def find_the_top(self, H, shape):
        # left top
        [w,h,tem] = shape
        v2 = [0,0,1]
        v1 = np.dot(H,v2)
        top=[]
        top.append([v1[0]/v2[2],v1[1]/v2[2]])

        # left bottom
        v2[0] = 0
        v2[1] = w
        v2[2] = 1
        v1 = np.dot(H , v2)
        top.append([v1[0] / v2[2],v1[1] / v2[2]])

        # right top
        v2[0] = h
        v2[1] = 0
        v2[2] = 1
        v1 = np.dot(H, v2)
        top.append([v1[0] / v2[2], v1[1] / v2[2]])
        return top
    def two_in_one(self,imageA,imageB,begin_w,last_w):
        (hA,wA,tem) = imageA.shape
        (hB,wB,tem) = imageB.shape
        h = min(hA,hB)
        over = int(wA -begin_w-last_w)
        begin_w = int(begin_w)
        imageA[0:h,0:begin_w] = imageB[0:h,0:begin_w]
        for now_w in range(begin_w,wB):
            for now_h in range(0,h):
                alpha = (now_w*1.0 - begin_w) / over * 1.0
                if ((imageA[now_h][now_w][0]==0) & (imageA[now_h][now_w][1]==0) & (imageA[now_h][now_w][2]==0)):
                    alpha = 0
                imageA[now_h][now_w][0] = imageA[now_h][now_w][0] * alpha + imageB[now_h][now_w][0] * (1 - alpha)
                imageA[now_h][now_w][1] = imageA[now_h][now_w][1] * alpha + imageB[now_h][now_w][1] * (1 - alpha)
                imageA[now_h][now_w][2] = imageA[now_h][now_w][2] * alpha + imageB[now_h][now_w][2] * (1 - alpha)
        return imageA