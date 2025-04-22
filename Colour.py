import cv2
import numpy as np

# Callback function for mouse event
def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE:
        hsv = param['hsv']
        if y < hsv.shape[0] and x < hsv.shape[1]:
            hsv_value = hsv[y, x]
            print(f"HSV at ({x}, {y}): H={hsv_value[0]}, S={hsv_value[1]}, V={hsv_value[2]}")

# Open default camera
cap = cv2.VideoCapture(0)

cv2.namedWindow("Video")
hsv_param = {'hsv': None}
cv2.setMouseCallback("Video", mouse_callback, hsv_param)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    hsv_param['hsv'] = hsv_frame

    cv2.imshow("Video", frame)

    # Exit with ESC key
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
