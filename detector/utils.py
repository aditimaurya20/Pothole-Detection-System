from ultralytics import YOLO
import cv2
import requests
import time
from django.core.mail import send_mail
from datetime import datetime

model = YOLO("runs/detect/train-6/weights/best.pt")

last_alert_time = 0


# ---------------- LOCATION ----------------
def get_location():
    try:
        res = requests.get("https://ipinfo.io/json")
        data = res.json()
        loc = data.get("loc", "0,0").split(",")
        return float(loc[0]), float(loc[1])
    except:
        return 0.0, 0.0


# ---------------- IMAGE DETECTION ----------------
def detect_image_pothole(image_path, output_path):

    results = model(image_path)
    img = cv2.imread(image_path)

    detected = False
    severity = "Low"

    for r in results:
        boxes = r.boxes

        if boxes is not None and len(boxes) > 0:
            detected = True

            if len(boxes) > 3:
                severity = "High"
            elif len(boxes) > 1:
                severity = "Medium"

            for box in boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                cv2.rectangle(img, (x1,y1), (x2,y2), (0,0,255), 2)
                cv2.putText(img, "Pothole", (x1,y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

    cv2.imwrite(output_path, img)

    return detected, severity


# ---------------- VIDEO DETECTION ----------------

def detect_video_pothole(video_path, output_path):

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return False

    fourcc = cv2.VideoWriter_fourcc(*"avc1")

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0 or fps is None:
        fps = 25

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    detected = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)

        for r in results:
            boxes = r.boxes

            if boxes is not None and len(boxes) > 0:
                detected = True

                for box in boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    cv2.rectangle(frame, (x1,y1), (x2,y2), (0,0,255), 2)
                    cv2.putText(frame, "Pothole", (x1,y1-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)

        out.write(frame)

    cap.release()
    out.release()

    return detected
# ---------------- SEND EMAIL FUNCTION ----------------

def send_pothole_email(location, pothole_count):

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = f"""
🚨 ALERT: Pothole Detected

A pothole has been detected in uploaded road video.

📍 Location:
{location}

🕒 Detection Time:
{current_time}

🛣 Total Potholes Detected:
{pothole_count}

⚠️ Please inspect the road immediately.

Regards,
AI Pothole Detection System
"""

    send_mail(
        subject="🚨 Pothole Detected Alert",
        message=message,
        from_email="shrutikakachare61@gmail.com",
        recipient_list=["mauryaaditi137@gmail.com"],
        fail_silently=False
    )
# ---------------- LIVE DETECTION ----------------
def detect_live():

    global last_alert_time

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        print("Camera not working")
        return

    frame_count = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame_count += 1

        detected = False

        # Process only every 3rd frame (faster)
        if frame_count % 3 == 0:

            results = model(frame)

            for r in results:

                boxes = r.boxes

                if boxes is not None and len(boxes) > 0:

                    detected = True

                    for box in boxes:

                        x1, y1, x2, y2 = map(int, box.xyxy[0])

                        conf = float(box.conf[0])

                        # Bounding box
                        cv2.rectangle(frame, (x1,y1), (x2,y2), (0,0,255), 2)

                        # Label + confidence
                        cv2.putText(
                            frame,
                            f"Pothole {conf:.2f}",
                            (x1,y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6,
                            (0,0,255),
                            2
                        )

        status = "POTHOLE DETECTED" if detected else "NO POTHOLE"

        cv2.putText(
            frame,
            status,
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0,0,255) if detected else (0,255,0),
            3
        )

        if detected and time.time() - last_alert_time > 30:

            lat, lon = get_location()

            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            message = f"""
            🚨 ALERT: Pothole Detected

            A pothole has been detected by the AI-based monitoring system.

            📍 Location:
            Latitude: {lat}
            Longitude: {lon}

            🕒 Detection Time:
            {current_time}

            ⚠️ Please inspect and repair the road section immediately.

            Regards,
            AI Pothole Detection System
            """

            send_mail(
                subject="🚨 Road Damage Alert - Pothole Detected",
                message=message,
                from_email="shrutikakachare61@gmail.com",
                recipient_list=["mauryaaditi137@gmail.com"],
                fail_silently=False
            )

            last_alert_time = time.time()

        frame = cv2.resize(frame, (900, 600))

        cv2.imshow("Live Detection", frame)

        # ESC key to quit
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()