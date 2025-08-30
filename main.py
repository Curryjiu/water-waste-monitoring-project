import sqlite3

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import request
from datetime import datetime
import base64
import numpy as np
import cv2
from ultralytics import YOLO
import io
from PIL import Image

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/db.sqlite3'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Object(db.Model):
    id = db.Column(db.TEXT, primary_key=True)
    category = db.Column(db.TEXT)
    time = db.Column(db.TEXT)
    image_base64 = db.Column(db.TEXT)


def create_database():
    db_name = "database/db.sqlite3"
    """创建SQLite数据库并初始化表结构"""
    # 检查数据库文件是否已存在
    if os.path.exists(db_name):
        print(f"数据库文件 {db_name} 已存在，将删除并重新创建")
        os.remove(db_name)

    try:
        # 连接到数据库（如果不存在则创建）
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        print(f"成功创建数据库: {db_name}")

        # 创建用户表
        cursor.execute('''
                       CREATE TABLE object
                       (
                           id            TEXT PRIMARY KEY,
                           category      TEXT NOT NULL,
                           time         TEXT NOT NULL,
                           image_base64 TEXT NOT NULL
                       )
                       ''')


        # 提交事务
        conn.commit()
        print("表结构创建完成并插入示例数据")

        # 验证数据
        cursor.execute("SELECT COUNT(*) FROM users")
        print(f"用户表记录数: {cursor.fetchone()[0]}")

        cursor.execute("SELECT COUNT(*) FROM orders")
        print(f"订单表记录数: {cursor.fetchone()[0]}")

    except sqlite3.Error as e:
        print(f"数据库操作错误: {e}")
        conn.rollback()
    finally:
        if conn:
            conn.close()
            print("数据库连接已关闭")


def process_image_with_yolo(image_base64):
    """
    使用YOLO11模型处理base64编码的图像，检测目标并添加检测框，返回处理后的base64图像

    参数:
        image_base64: 原始图像的base64编码字符串

    返回:
        处理后的图像的base64编码字符串
    """
    try:
        # 1. 将base64编码转换为OpenCV图像格式
        # 移除可能存在的base64前缀（如"data:image/jpeg;base64,"）
        if ',' in image_base64:
            image_base64 = image_base64.split(',')[1]

        # 解码base64字符串为字节数据
        image_data = base64.b64decode(image_base64)

        # 将字节数据转换为numpy数组
        nparr = np.frombuffer(image_data, np.uint8)

        # 解码为OpenCV图像（BGR格式）
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if image is None:
            raise ValueError("无法解码图像数据，可能是无效的base64编码")

        # 2. 加载YOLO11模型并进行目标检测
        # 可以根据需要替换为其他版本，如yolo11s.pt, yolo11m.pt, yolo11l.pt, yolo11x.pt
        model = YOLO('yolo11n.pt')
        results = model(image)

        # 3. 在图像上绘制检测框和类别信息
        for result in results:
            boxes = result.boxes
            for box in boxes:
                # 获取边界框坐标
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # 获取类别和置信度
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                class_name = model.names[cls]

                # 绘制边界框（绿色，线宽2）
                cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # 绘制类别和置信度文本
                text = f"{class_name}: {conf:.2f}"
                cv2.putText(image, text, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # 4. 将处理后的图像转回base64编码
        # 转换颜色空间（BGR -> RGB）
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # 转换为PIL图像
        pil_image = Image.fromarray(rgb_image)

        # 保存到字节流
        buffer = io.BytesIO()
        pil_image.save(buffer, format="JPEG", quality=95)

        # 编码为base64
        processed_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        # 添加数据URL前缀
        return f"data:image/jpeg;base64,{processed_base64}"

    except Exception as e:
        print(f"处理图像时出错: {str(e)}")
        raise  # 重新抛出异常，让调用者处理


# 使用示例:
# processed_image = process_image_with_yolo(image_base64)


# app.route("/api/image",)
@app.route("/api/image", methods=['POST'])
def get_image():
    data = request.get_json()
    image_base64 = data.get('image_base64')
    image_base64 = process_image_with_yolo(image_base64)

    if image_base64:
        try:
            # 生成当前时间
            current_time = datetime.now().isoformat()

            # 创建新的Object实例
            new_object = Object(
                id=current_time,
                category="",
                time=current_time,
                image_base64=image_base64
            )

            engine = create_engine('sqlite:///database/db.sqlite3')
            Session = sessionmaker(bind=engine)
            session = Session()
            session.add(new_object)
            session.commit()

            return "OK"
        except Exception as e:
            # 处理数据库操作异常
            db.session.rollback()
            return f"Database error: {str(e)}", 500
        finally:
            db.session.close()
    return "Missing image_base64 parameter", 400


@app.route('/')
def index():
    engine = create_engine('sqlite:///database/db.sqlite3')
    Session = sessionmaker(bind=engine)
    session = Session()
    objects = session.query(Object).all()
    objects_list = [{
        'id': obj.id,
        'category': obj.category,
        'time': obj.time,
        'image_base64': obj.image_base64
    } for obj in objects]
    session.close()
    return render_template("main.html", objects=objects_list)


if __name__ == "__main__":
    create_database()
    app.run(host="0.0.0.0", debug=True, port=9988)
