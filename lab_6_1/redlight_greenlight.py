import cv2
import numpy as np
import time

stage_duration_sec = 5

vid = cv2.VideoCapture(0)
last_frames = []
stage_begin_time = time.time()
is_detecting_motion = True

while True:
    if time.time() - stage_begin_time >= stage_duration_sec:
        is_detecting_motion = not is_detecting_motion
        stage_begin_time = time.time()

    ret, frame = vid.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    if len(last_frames) >= 3:
        smooth_kernel = np.array([[0.1] * 3] * 3)
        frame_gray = cv2.filter2D(frame_gray, -1, smooth_kernel)

        mean_last = np.mean(np.array(last_frames + [frame_gray]), axis=0).astype(np.uint8)
        diff = np.fmin(mean_last - frame_gray, frame_gray - mean_last)

        _, diff = cv2.threshold(diff, 10, 255, cv2.THRESH_BINARY)

        diff = cv2.filter2D(diff, -1, smooth_kernel)

        zero_frame = np.array([[0] * diff.shape[1]] * diff.shape[0]).astype(np.uint8)

        if not is_detecting_motion:
            diff = zero_frame

        motion_map = cv2.merge([zero_frame, 255 - diff, diff])

        cv2.putText(img=motion_map, text='Red light' if is_detecting_motion else 'Green Light', org=(00, 470),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=1, color=(128, 128, 0), thickness=2, lineType=cv2.LINE_AA,
                    bottomLeftOrigin=False)

        cv2.imshow('vid', frame)
        cv2.imshow('motion', motion_map)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        last_frames.append(frame_gray)
        last_frames.pop(0)
    else:
        last_frames.append(frame_gray)

vid.release()
cv2.destroyAllWindows()
