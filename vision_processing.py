import cv2
from ultralytics import YOLO

from config import DEVICE, RTSP_URLS, FRAME_SKIP
import database

yolo_model = YOLO('yolov8n.pt')  # Load YOLOv8n model
yolo_model.to(DEVICE)

def process_frame(cam_id, frame):
    results = yolo_model(frame)
    for result in results:
        for pred in result.boxes.data.tolist():
            x1, y1, x2, y2, conf, cls = map(int, pred[:6])
            label = yolo_model.names[cls]
            database.save_zebra_crossing_data(cam_id, label, 1)

def process_camera(cam_id):
    cap = cv2.VideoCapture(RTSP_URLS[f'cam{cam_id}'])
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_count += 1
        if frame_count % FRAME_SKIP == 0:
            process_frame(cam_id, frame)
    cap.release()