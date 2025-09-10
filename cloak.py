import cv2
import numpy as np

# Open webcam
cap = cv2.VideoCapture(0)

# Load background image
bg = cv2.imread("bgimage.jpg")
if bg is None:
    print("Error: Background image not found. Run background.py first.")
    exit()

# Resize background to match webcam frame
bg = cv2.resize(bg, (int(cap.get(3)), int(cap.get(4))))

# HSV color ranges for cloaks
colors = {
    "red": [(np.array([0, 120, 70]), np.array([10, 255, 255])),
            (np.array([170, 120, 70]), np.array([180, 255, 255]))],
    "green": [(np.array([40, 40, 40]), np.array([90, 255, 255]))],
    "blue": [(np.array([94, 80, 2]), np.array([126, 255, 255]))]
}

current_color = "red"  # Default cloak color

print("Press 1=Red, 2=Green, 3=Blue | q=Quit")

while cap.isOpened():
    check, frame = cap.read()
    if not check:
        print("Error: Could not read frame.")
        break

    frame = cv2.flip(frame, 1)  # Mirror view
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create mask for selected color
    mask = None
    for (lower, upper) in colors[current_color]:
        m = cv2.inRange(hsv, lower, upper)
        mask = m if mask is None else cv2.bitwise_or(mask, m)

    # Clean mask
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
    mask = cv2.dilate(mask, kernel, iterations=1)

    # Invert mask
    mask_inv = cv2.bitwise_not(mask)

    # Cloak area → from background
    part1 = cv2.bitwise_and(bg, bg, mask=mask)

    # Rest of the frame → from live feed
    part2 = cv2.bitwise_and(frame, frame, mask=mask_inv)

    # Combine
    final = cv2.addWeighted(part1, 1, part2, 1, 0)

    cv2.putText(final, f"Cloak Color: {current_color.upper()}",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow("Invisibility Cloak", final)

    key = cv2.waitKey(5) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('1'):
        current_color = "red"
    elif key == ord('2'):
        current_color = "green"
    elif key == ord('3'):
        current_color = "blue"

cap.release()
cv2.destroyAllWindows()
