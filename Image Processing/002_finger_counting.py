import cv2
import time
import mediapipe as mp

cap = cv2.VideoCapture(0) # defult camera
cap.set(3, 640) # set width(3)
cap.set(4, 480) # set height(4)

mpHand = mp.solutions.hands # Hands modeli
hands = mpHand.Hands() # Hands modelini kullanmak için hands değişkenine atıyoruz
mpDraw = mp.solutions.drawing_utils # Elimizdeki noktaları birleştirmek için
pTime = 0
cTime = 0
tipIds = [4, 8, 12, 16, 20] # Baş ve işaret parmaklarının uç noktalarının id'leri

while True:
    success, img = cap.read() # Kameradan görüntü alıyoruz
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Görüntüyü RGB formatına çeviriyoruz

    results = hands.process(imgRGB) # Görüntüyü hands modeline gönderiyoruz
    print(results.multi_hand_landmarks) # Görüntüdeki ellerin noktalarını alıyoruz

    lmList = [] # Noktaları tutmak için boş bir liste oluşturuyoruz
    if results.multi_hand_landmarks: # Eğer görüntüde el varsa
        for handLms in results.multi_hand_landmarks: # Her bir el için
            mpDraw.draw_landmarks(img, handLms, mpHand.HAND_CONNECTIONS) # Noktaları birleştiriyoruz

            for id, lm in enumerate(handLms.landmark): # Her bir nokta için
                h, w, _ = img.shape # Görüntünün yüksekliğini ve genişliğini alıyoruz
                cx, cy = int(lm.x*w), int(lm.y*h) # Noktaların koordinatlarını alıyoruz
                lmList.append([id, cx, cy]) # Noktaları listeye ekliyoruz
                
                # # isaret uc = 8
                # if id == 8:
                #     cv2.circle(img, (cx, cy), 10, (255, 0, 255), cv2.FILLED)
                # # isaret uc = 6
                # if id == 6:
                #     cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)

    if len(lmList) != 0:
        fingers = [] # Parmakları tutmak için boş bir liste oluşturuyoruz

        # Sağ sol el tespiti
        if lmList[tipIds[0]][1] < lmList[tipIds[0]-1][1]:
            hangiel = "sol el"
        else:
            hangiel = "sag el"
        cv2.putText(img, hangiel, (360, 75), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 255), 5)

        # Baş parmak
        if lmList[tipIds[0]][1] < lmList[tipIds[0]-1][1]: # Eğer baş parmak kıvrılmışsa
            fingers.append(1) # parmak kıvrılmış olarak listeye ekliyoruz
        else: # Eğer baş parmak kıvrılmamışsa
            fingers.append(0) # parmak kıvrılmamış olarak listeye ekliyoruz
        # 4 parmak
        for id in range(1,5): # Her bir parmak için
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]: # Eğer parmak kıvrılmışsa
                fingers.append(1) # parmak kıvrılmış olarak listeye ekliyoruz
            else: # Eğer parmak kıvrılmamışsa
                fingers.append(0) # parmak kıvrılmamış olarak listeye ekliyoruz

        totalFingers = fingers.count(1) # Kıvrılmış parmak sayısını alıyoruz
        # print(totalFingers)
        cv2.putText(img, str(totalFingers), (30, 125), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 255), 5) # Kıvrılmış parmak sayısını ekrana yazdırıyoruz
        # resim , yazı , konum , font , boyut , renk , kalınlık

    # fps
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, "FPS:" + str(int(fps)), (15, 350), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)


    cv2.imshow("Image", img) # Görüntüyü ekranda gösteriyoruz
    cv2.waitKey(1) # 1 milisaniye bekliyoruz
      # Klavyeden herhangi bir tuşa basılınca döngüden çık
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Döngüden çıktıktan sonra kamera ve pencereyi serbest bırak
cap.release()
cv2.destroyAllWindows()
