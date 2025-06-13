from flask import Flask, render_template, request, send_file
from captcha.image import ImageCaptcha
from io import BytesIO

from server import Server
from service import Service
from client import Client

app = Flask(__name__)

# 初始化 Server、Service、Client
server = Server()
service = server.service
client = Client(service, server.circuit.client)

@app.route("/", methods=["GET", "POST"])
def captcha():
    if request.method == "POST":
        user_input = request.form.get("captcha_input", "")
        is_verified = client.verify(user_input)
        server.regenerate_captcha()  # 每次訪問都生成新的 captcha
        if is_verified:
            return render_template("success.html")
        else:
            return render_template("fail.html")
    return render_template("index.html")

@app.route("/captcha_image")
def captcha_image():
    captcha_text = server.captcha_string
    image = ImageCaptcha(width=280, height=90)
    data = image.generate(captcha_text)

    # 轉成 BytesIO 並回傳
    img_io = BytesIO(data.read())
    img_io.seek(0)
    return send_file(img_io, mimetype='image/png')

@app.route("/new_page")
def new_page_route():
    # You can add any logic here if needed before rendering
    return render_template("new_page.html")

if __name__ == "__main__":
    app.run(debug=True)
