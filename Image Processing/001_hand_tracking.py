import cv2
import time
import mediapipe as mp

cap = cv2.VideoCapture(0)  # default camera

mpHand = mp.solutions.hands
hands = mpHand.Hands(max_num_hands=1)
hands = mpHand.Hands()
mpDraw = mp.solutions.drawing_utils
pTime = 0
cTime = 0

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(imgRGB)
    print(results.multi_hand_landmarks) # abi süper proje

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHand.HAND_CONNECTIONS)

            for id, lm in enumerate(handLms.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # bilek
                if id == 0:
                    cv2.circle(img, (cx, cy), 9, (255, 0, 255), cv2.FILLED)
                # serçe parmak
                if id == 20:
                    cv2.circle(img, (cx, cy), 9, (255, 0, 255), cv2.FILLED)

    # fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, "FPS:" + str(int(fps)), (10, 75), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)

    # Klavyeden herhangi bir tuşa basılınca döngüden çık
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Döngüden çıktıktan sonra kamera ve pencereyi serbest bırak
cap.release()
cv2.destroyAllWindows()
