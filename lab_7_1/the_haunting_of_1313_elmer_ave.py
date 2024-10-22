import cv2
import numpy as np
from matplotlib import pyplot as plt

image_path = 'halloween/lab7.png'
ghost_paths = ['halloween/candy_ghost.png', 'halloween/pampkin_ghost.png', 'halloween/scary_ghost.png']

def main():
    scene_image = cv2.imread(image_path)
    scene_image = cv2.cvtColor(scene_image, cv2.COLOR_BGR2GRAY)
    ghost_images = [cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2GRAY) for path in ghost_paths]

    sift = cv2.SIFT_create()

    scene_key_points, scene_descriptors = sift.detectAndCompute(scene_image, None)

    # FLANN parameters
    flann_index_kdtree = 1
    index_params = dict(algorithm=flann_index_kdtree, trees=5)
    search_params = dict(checks=50)  # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params, search_params)

    for ghost_image in ghost_images:
        img3 = scene_image.copy()

        ghost_key_points, ghost_descriptors = sift.detectAndCompute(ghost_image, None)

        matches = flann.knnMatch(scene_descriptors, ghost_descriptors, k = 2)

        good_matches = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)

        min_match_count = 10
        if len(good_matches) > min_match_count:
            src_pts = np.float32([scene_key_points[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
            dst_pts = np.float32([ghost_key_points[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

            homography, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC, 5.0)
            matches_mask = mask.ravel().tolist()

            h, w = ghost_image.shape
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
            dst = cv2.perspectiveTransform(pts, homography)

            img3 = cv2.polylines(img3, [np.int32(dst)], True, (255, 255, 255), 3)

        else:
            print('Not enough matches to draw a mask')
            matches_mask = None

        draw_params = dict(singlePointColor=None,
                           matchesMask=matches_mask,
                           flags=2)

        img3 = cv2.drawMatches(img3, scene_key_points, ghost_image, ghost_key_points, good_matches, None, **draw_params)

        plt.imshow(img3), plt.show()

main()
