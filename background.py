import cv2
cap = cv2.VideoCapture(0)

while cap.isOpened():
    check, bg = cap.read()
    if check:
        cv2.imshow("bgimage",bg)

        if cv2.waitKey(5)==ord('s'):
            cv2.imwrite("bgimage.jpg",bg)
            break
        
cap.release()
cv2.destroyAllWindows()

cap = cv2.VideoCapture(0)

while cap.isOpened():
    check, bg = cap.read()
    if not check:
        print("Error: Could not access webcam.")
        break

    cv2.imshow("Background Capture - Press 's' to save", bg)

    # Press 's' to save background image
    if cv2.waitKey(5) == ord('s'):
        cv2.imwrite("bgimage.jpg", bg)
        print("Background saved as bgimage.jpg")
        break

cap.release()
cv2.destroyAllWindows()
