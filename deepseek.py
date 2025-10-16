import base64
from volcenginesdkarkruntime import Ark
from flask import Flask, render_template
from flask import request
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# 初始化Ark客户端
client = Ark(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key="1746a7bb-34e9-42d9-95a3-86f4e53bcb5e",
)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        # 获取上传的文件和文字
        image = request.files['image']
        text = request.form['text']

        if image:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(image_path)

            # 将图片转换为Base64
            image_base64 = image_to_base64(image_path)
            if not image_base64:
                return "无法获取图片数据", 500

            # 构建请求，使用Base64格式
            try:
                response = client.chat.completions.create(
                    model="deepseek-r1-250528",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{image_base64}"
                                    },
                                },
                                {"type": "text", "text": text},
                            ],
                        }
                    ],
                )
                result = str(response.choices[0].message.content)
            except Exception as e:
                result = f"调用API出错: {str(e)}"

            return render_template("index.html", text=result)

    return render_template("index.html", text="")


@app.route('/')
def image_to_base64(file_path):
    """将本地图片文件转换为Base64编码"""
    try:
        with open(file_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string
    except Exception as e:
        print(f"图片转换失败: {e}")
        return None
