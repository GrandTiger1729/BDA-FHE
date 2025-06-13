from flask import Flask, render_template, request, redirect, url_for
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
        return render_template(
            "result.html",
            is_verified=is_verified
        )

    # 預設顯示 captcha 頁面
    return render_template(
        "index.html",
        captcha_string=server.captcha_string
    )

if __name__ == "__main__":
    app.run(debug=True)

