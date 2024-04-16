from flask import Flask, request, make_response
from flask_cors import CORS
import time

mode = "remote"  # local or remote
LAN_IP = "0.0.0.0"

app = Flask(__name__, static_folder="../", static_url_path="")
# CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])
CORS(app, origins="*", resources={r"/*": {"origins": "*"}})

# 機械臂執行任務中標識
running = False


# 訪問的URL路徑
@app.route("/do")
def do():
    global running
    pw = request.args.get("pw")
    command = request.args.get("command")
    # 密碼正確
    if pw == "abcd1234":
        if command and (not running):
            # 收到指令，設定running為True，在此過程中不接受其他指令
            print("機械臂執行指令", command, "\n\n\n\n")
            running = True

            # TODO: ************************* 判斷接收的指令，進行機械臂的對應任務 *************************
            time.sleep(5)

            # TODO: 動作做完後設定running為False !!!
            # 任務執行完畢
            running = False
            return make_response("<h1>Success</h1>", 200)
        elif running:
            print("正在執行，請稍後", "\n\n\n\n")
            return make_response("<h1>Running</h1>", 201)
    else:
        return make_response("<h1>Failed</h1>", 400)


# TODO: ************************* 機械臂子函數 *************************


if __name__ == "__main__":
    if mode == "local":
        # localhost運行模式
        app.run(debug=True, port=5001)
    else:
        # 使用LAN_IP打開服務器模式
        print(mode, "mode\n\n\n\n")
        # 臨時SSL證書
        # app.run(host=LAN_IP, debug=True, port=5001, ssl_context="adhoc")
        # 本地自部署SSL證書
        app.run(
            host=LAN_IP,
            debug=True,
            port=5001,
            ssl_context=("../cert.pem", "../key.pem"),
        )
        # 無證書運行模式
        # app.run(host=LAN_IP, debug=True, port=5001)
