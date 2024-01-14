import cv2
import mediapipe as mp
import time

mpPose = mp.solutions.pose # Pose modeli
pose = mpPose.Pose() # Pose modelini pose değişkenine atadık

mpDraw = mp.solutions.drawing_utils # Pose modeli için çizim araçları
cap = cv2.VideoCapture("Videos\production_id_5192157 (360p).mp4") # Videoyu okuduk
ptime = 0 # FPS hesaplamak için önceki zamanı tuttuk

while True:
    success, img = cap.read() # Videodan frame okuduk
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Videodaki frame'i RGB formatına çevirdik
    results = pose.process(imgRGB) # Frame'i pose modeline gönderdik
    print(results.pose_landmarks) # Frame'deki landmark'ları ekrana yazdırdık

    if results.pose_landmarks: # Eğer landmark varsa
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS) # Landmark'ları çizdirdik

        for id, lm in enumerate(results.pose_landmarks.landmark): 
            # Landmark'ların id ve koordinatlarını ekrana yazdırdık
            h, w, c = img.shape # Frame'in yüksekliğini ve genişliğini aldık
            cx, cy = int(lm.x*w), int(lm.y*h) # Landmark'ın koordinatlarını aldık

            if id == 4: # Sol omuz
                cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
                # resim, merkez, yarıçap, renk, kalınlık

    ctime = time.time() # Şimdiki zamanı aldık
    fps = 1/(ctime-ptime) # FPS hesapladık
    ptime = ctime # Önceki zamanı güncelledik

    cv2.putText(img, "Fps:"+ str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3) 
    # resim, yazı, koordinat, font, boyut, renk, kalınlık
    

    cv2.imshow("Image", img) # Frame'i gösterdik
    cv2.waitKey(1) # 1 sn bekledik