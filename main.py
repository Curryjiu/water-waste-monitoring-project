from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/db.sqlite3'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 在应用上下文内创建数据库
# with app.app_context():
#     db_dir = os.path.dirname(app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', ''))
#     os.makedirs(db_dir, exist_ok=True)
#     db.create_all()

class Object(db.Model):
    id = db.Column(db.TEXT, primary_key=True)
    category = db.Column(db.TEXT)
    time = db.Column(db.TEXT)
    image_base64 = db.Column(db.TEXT)

#app.route("/api/image",)
@app.route("/api/get_image")
def get_image(image_base64:str):
    print()


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
    app.run(host="0.0.0.0", debug=True, port=9988)