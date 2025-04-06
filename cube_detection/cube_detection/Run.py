from ultralytics import YOLO
import cv2

model = YOLO("runs/detect/model2/weights/best.pt")

cap = cv2.VideoCapture(1)
print("Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    results = model(frame, save=False, conf=0.25)  # confidence can be changes here
    annotated_frame = results[0].plot()
    cv2.imshow("Rubix detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break