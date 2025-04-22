import cv2
import numpy as np

# Step 1: Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def preprocess_frame(frame):
    """
    Resize, blur, and convert the frame to grayscale.
    """
    resized = cv2.resize(frame, (640, 480))
    blurred = cv2.GaussianBlur(resized, (5, 5), 0)
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    return gray

def hsv_threshold(frame):
    """
    Apply HSV color thresholding to isolate floor colors.
    """
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define range for floor color in HSV (example for light grey)
    lower_floor = np.array([95, 40, 120])
    upper_floor = np.array([115, 110, 200])
    
    mask = cv2.inRange(hsv, lower_floor, upper_floor)
    return mask

def texture_filter(frame):
    """
    Apply texture filtering (edge detection).
    """
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Apply Canny edge detection
    edges = cv2.Canny(gray, 50, 150)
    
    return edges

# Step 2: Frame capture loop
print("Webcam stream started. Press 'q' to quit.")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Step 1: Preprocess frame
        gray = preprocess_frame(frame)

        # Step 2: HSV Thresholding (Floor detection based on color)
        floor_mask = hsv_threshold(frame)
        
        # Step 3: Texture Filtering (Edge detection to avoid non-floor areas)
        edges = texture_filter(frame)
        
        # Combine HSV mask and edges mask (logical AND) to get the floor area
        hybrid_mask = cv2.bitwise_and(floor_mask, cv2.bitwise_not(edges))

        # Step 4: Display masks and results
        cv2.imshow("Original", frame)
        cv2.imshow("Floor Mask (HSV)", floor_mask)
        cv2.imshow("Edges (Texture)", edges)
        cv2.imshow("Hybrid Mask", hybrid_mask)

        key = cv2.waitKey(30) & 0xFF

        # Handle key press
        if key == ord('q') or key == 27:  # 27 = ESC key
            print("Exit key detected. Quitting...")
            break

except KeyboardInterrupt:
    print("\nKeyboardInterrupt detected. Exiting...")

finally:
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("Resources released. Program terminated.")
