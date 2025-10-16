import time
import cv2
import sqlite3
import base64
from datetime import datetime
from flask import Flask, render_template, Response
from geopy import Nominatim
from geopy.exc import GeocoderTimedOut
from ultralytics import YOLO

app = Flask(__name__)

# 初始化数据库
conn = sqlite3.connect('detection.db')
cursor = conn.cursor()
cursor.execute('''
               CREATE TABLE IF NOT EXISTS detections
               (
                   id             INTEGER PRIMARY KEY AUTOINCREMENT,
                   detection_time DATETIME,
                   gps_location   TEXT,
                   object_class   TEXT,
                   image_data     TEXT
               )''')
conn.commit()

# 尝试连接USB Camera，通常设备索引为1
camera = cv2.VideoCapture(0)
if not camera.isOpened():
    print(f"无法连接到USB Camera (索引 )，尝试默认摄像头")
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("无法连接到任何摄像头")
        raise Exception("摄像头初始化失败")

model = YOLO('yolo11n.pt')

timestamp = 0
raw_frame = None
detected_frame = None
detected_results = []


def save_detection_info(class_name, image_data):
    # 获取当前GPS位置
    geolocator = Nominatim(user_agent="underwater_detection_system")
    try:
        # location = geolocator.geocode("me", timeout=10)
        gps_location = f"{118.81122}, {32.068251}"
    except GeocoderTimedOut:
        gps_location = "未知位置"
    detection_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect('detection.db')
    cursor = conn.cursor()
    cursor.execute('''
                   INSERT INTO detections (detection_time, gps_location, object_class, image_data)
                   VALUES (?, ?, ?, ?)
                   ''', (detection_time, gps_location, class_name, image_data))
    conn.commit()
    conn.close()


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/raw_frame')
def get_raw_frame():
    global timestamp, raw_frame, detected_frame, detected_results

    if time.time() - timestamp > 0.1:
        # 获取画面
        success, raw_frame = camera.read()
        timestamp = time.time()

        detected_results = model(raw_frame)
        detected_frame = detected_results[0].plot()

        # 将图片转为Base64字符串
        ret, buffer = cv2.imencode('.jpg', detected_frame)
        image_data = base64.b64encode(buffer).decode('utf-8')

        # 保存检测信息
        if time.time() - timestamp > 3:
            for result in detected_results:
                boxes = result.boxes.cpu().numpy()
                for box in boxes:
                    class_id = int(box.cls[0])
                    class_name = model.names[class_id]
                    save_detection_info(class_name, image_data)

    ret, buffer = cv2.imencode('.jpg', raw_frame)
    frame = buffer.tobytes()
    return Response(frame, mimetype='image/jpeg')


@app.route('/detected_frame')
def get_detected_frame():
    global detected_frame
    ret, buffer = cv2.imencode('.jpg', detected_frame)
    frame = buffer.tobytes()
    return Response(frame, mimetype='image/jpeg')


@app.route('/detection_info')
def get_detection_info():
    global detected_results

    detections = []
    for result in detected_results:
        boxes = result.boxes.cpu().numpy()
        for box in boxes:
            class_id = int(box.cls[0])
            class_name = model.names[class_id]
            confidence = float(box.conf[0])
            x1 = int(box.xyxy[0][0])
            y1 = int(box.xyxy[0][1])
            x2 = int(box.xyxy[0][2])
            y2 = int(box.xyxy[0][3])

            detections.append({
                'name': class_name,
                'confidence': confidence,
                'x1': x1,
                'y1': y1,
                'x2': x2,
                'y2': y2
            })

    print(detections)

    return {'detections': detections}


@app.route('/history')
def history():
    return render_template('history.html')


@app.route('/map')
def map():
    return render_template('map.html')


@app.route('/history_data')
def get_history_data():
    conn = sqlite3.connect('detection.db')
    cursor = conn.cursor()
    cursor.execute('''
                   SELECT detection_time, gps_location, object_class, image_data
                   FROM detections
                   ORDER BY detection_time DESC
                   LIMIT 100
                   ''')
    history_data = cursor.fetchall()
    conn.close()

    columns = ['detection_time', 'gps_location', 'object_class', 'image_data']
    data = [dict(zip(columns, row)) for row in history_data]

    return {'history_data': data}


if __name__ == '__main__':
    app.run(debug=True)
