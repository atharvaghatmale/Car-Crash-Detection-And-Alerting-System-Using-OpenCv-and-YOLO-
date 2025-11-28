import cv2
import pandas as pd
from ultralytics import YOLO
import cvzone
import send_email  
import time

model = YOLO('best.pt')

cap = cv2.VideoCapture('cr.mp4')

my_file = open("coco1.txt", "r")
data = my_file.read()
class_list = data.split("\n")

count = 0
last_sent_time = 0  
email_cooldown = 10  

while True:
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    count += 1
    if count % 3 != 0:  
        continue

    frame = cv2.resize(frame, (1020, 500))
    results = model.predict(frame)
    a = results[0].boxes.data
    px = pd.DataFrame(a).astype("float")

    for index, row in px.iterrows():
        x1, y1, x2, y2 = int(row[0]), int(row[1]), int(row[2]), int(row[3])
        d = int(row[5])
        c = class_list[d]

       
        if c == "Crash":  
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cvzone.putTextRect(frame, f'{c}', (x1, y1), 1, 1)
            

            
            current_time = time.time()
            if current_time - last_sent_time > email_cooldown:
                last_sent_time = current_time 

               
                crash_image = f"crash_{int(time.time())}.jpg"
                cv2.imwrite(crash_image, frame)

                # Send email with the new crash image
                send_email.SendMail(crash_image)
                print(f"🚨 Crash detected! Email sent with image {crash_image}")

    cv2.imshow("RGB", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
