import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import pyautogui
import numpy as np

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Initialize Hand Detector
detector = HandDetector(maxHands=1, detectionCon=0.8)

# Get screen size
screen_w, screen_h = pyautogui.size()

# Smoothing variables
plocX, plocY = 0, 0
clocX, clocY = 0, 0
smoothening = 7
frameR = 100

while True:
    success, img = cap.read()
    if not success:
        print("Camera not detected.")
        break

    hands, img = detector.findHands(img, flipType=True)

    if hands:
        hand = hands[0]
        lmList = hand["lmList"]

        # Ensure landmarks exist
        if len(lmList) >= 9:
            # Extract only (x, y)
            x1, y1 = lmList[8][0:2]   # Index finger tip
            x2, y2 = lmList[4][0:2]   # Thumb tip

            # Draw visual circles
            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)

            # Map finger position to screen size
            screen_x = np.interp(x1, (frameR, 1280 - frameR), (0, screen_w))
            screen_y = np.interp(y1, (frameR, 720 - frameR), (0, screen_h))

            # Smooth cursor movement
            clocX = plocX + (screen_x - plocX) / smoothening
            clocY = plocY + (screen_y - plocY) / smoothening
            pyautogui.moveTo(screen_w - clocX, clocY)
            plocX, plocY = clocX, clocY

            # Calculate distance manually (no unpacking issues)
            distance = int(np.hypot(x2 - x1, y2 - y1))

            # Click if fingers close together
            if distance < 40:
                cv2.circle(img, (x1, y1), 15, (0, 255, 0), cv2.FILLED)
                pyautogui.click()

    cv2.imshow("Finger Cursor", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


