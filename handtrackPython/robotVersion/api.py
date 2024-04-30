# API Server Function Import
from flask import Flask, request, make_response
from flask_cors import CORS
import time

# Robot Function Import
import Board
import cv2
import apriltag
import atexit

mode = "remote"  # local or remote
LAN_IP = "0.0.0.0"
app = Flask(__name__, static_folder="../", static_url_path="")
CORS(app, origins="*", resources={r"/*": {"origins": "*"}})

# 機械臂執行任務中標識
running = False
tag_id = None


# Robot Function
def f_exit():
    ini_pos()
    cap.release()
    cv2.destroyAllWindows()
    unload_all_servo()
    print("Exit!!!!!!", "\n")


atexit.register(f_exit)

detector = apriltag.Detector()


def apriltagDetect():
    global tag_id

    cap = cv2.VideoCapture(-1)
    ret, img = cap.read()

    # Breakpoint test
    # while(cap.isOpened()):
    # 	ret,frame = cap.read()
    # 	cv2.imshow('frame', frame)
    # 	key=cv2.waitKey(1)
    # 	if key & 0xFF == ord('q'):
    # 		cv2.destroyAllWindows()
    # 		break

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    detections = detector.detect(gray)

    print("len(detections)", len(detections))
    cv2.destroyAllWindows()
    if len(detections) != 0:
        for detection in detections:
            tag_family = str(detection.tag_family, encoding="utf-8")
            tag_id = int(detection.tag_id)
            return tag_family, tag_id
    else:
        tag_id = None
        return None, None


def ini_pos():
    # initial position
    Board.setBusServoPulse(1, 300, 700)
    Board.setBusServoPulse(2, 500, 700)
    Board.setBusServoPulse(3, 80, 700)
    Board.setBusServoPulse(4, 625, 700)
    Board.setBusServoPulse(5, 470, 700)
    Board.setBusServoPulse(6, 500, 700)
    time.sleep(1)


def unload_all_servo():
    time.sleep(2)
    #  Unload All Servo Motor
    for i in range(6):
        Board.unloadBusServo(i + 1)


def actR1():
    global tag_id
    # move to R1
    Board.setBusServoPulse(5, 660, 700)
    Board.setBusServoPulse(6, 130, 700)
    time.sleep(1)
    Board.setBusServoPulse(3, 130, 700)
    Board.setBusServoPulse(4, 680, 700)
    Board.setBusServoPulse(5, 500, 700)
    time.sleep(1)
    Board.setBusServoPulse(3, 300, 700)
    Board.setBusServoPulse(4, 740, 700)
    Board.setBusServoPulse(5, 400, 700)
    time.sleep(1)
    Board.setBusServoPulse(3, 370, 700)
    Board.setBusServoPulse(4, 760, 700)
    Board.setBusServoPulse(5, 360, 700)
    time.sleep(1)
    time.sleep(0.5)
    # grap from R1
    Board.setBusServoPulse(1, 550, 700)
    time.sleep(1)
    Board.setBusServoPulse(3, 320, 700)
    Board.setBusServoPulse(5, 385, 700)
    time.sleep(1)
    Board.setBusServoPulse(3, 260, 700)
    Board.setBusServoPulse(5, 415, 700)
    time.sleep(1)
    Board.setBusServoPulse(4, 800, 700)
    Board.setBusServoPulse(5, 450, 700)
    time.sleep(1)
    Board.setBusServoPulse(4, 850, 700)
    Board.setBusServoPulse(5, 500, 700)
    time.sleep(1)
    Board.setBusServoPulse(5, 650, 700)
    time.sleep(1)
    # detect if successfully grapped
    tag_family, tag_id = apriltagDetect()
    print("tag id", tag_id)
    if tag_id is not None:
        print("successfully grapped")
        # place to target point
        Board.setBusServoPulse(6, 500, 700)
        time.sleep(1)
        Board.setBusServoPulse(5, 600, 700)
        time.sleep(1)
        Board.setBusServoPulse(1, 300, 700)
        time.sleep(1)
    else:
        print("failed to grap")
    time.sleep(0.5)


def actR2():
    global tag_id
    # move to R2
    Board.setBusServoPulse(5, 660, 700)
    time.sleep(1)
    Board.setBusServoPulse(4, 450, 700)
    Board.setBusServoPulse(5, 510, 700)
    Board.setBusServoPulse(6, 125, 700)
    time.sleep(1)
    Board.setBusServoPulse(4, 600, 700)
    Board.setBusServoPulse(5, 410, 700)
    time.sleep(1)
    Board.setBusServoPulse(3, 230, 700)
    Board.setBusServoPulse(4, 640, 700)
    time.sleep(1)
    Board.setBusServoPulse(3, 310, 700)
    Board.setBusServoPulse(4, 680, 700)
    time.sleep(1)
    time.sleep(0.5)
    # grap from R2
    Board.setBusServoPulse(1, 550, 700)
    time.sleep(1)
    Board.setBusServoPulse(3, 250, 700)
    Board.setBusServoPulse(4, 640, 700)
    time.sleep(1)
    Board.setBusServoPulse(3, 200, 700)
    Board.setBusServoPulse(4, 610, 700)
    time.sleep(1)
    Board.setBusServoPulse(3, 150, 700)
    Board.setBusServoPulse(4, 570, 700)
    time.sleep(1)
    Board.setBusServoPulse(3, 100, 700)
    Board.setBusServoPulse(4, 530, 700)
    time.sleep(1)
    Board.setBusServoPulse(3, 80, 700)
    Board.setBusServoPulse(4, 450, 700)
    Board.setBusServoPulse(5, 510, 700)
    time.sleep(1)
    # detect if successfully grapped
    tag_family, tag_id = apriltagDetect()
    print("id", tag_id)
    if tag_id is not None:
        print("successfully grapped")
        # place to target point
        Board.setBusServoPulse(6, 500, 700)
        time.sleep(1)
        Board.setBusServoPulse(4, 625, 700)
        Board.setBusServoPulse(5, 435, 700)
        time.sleep(1)
        Board.setBusServoPulse(1, 300, 700)
        time.sleep(1)
    else:
        print("failed to grap")
    time.sleep(0.5)


def actR3():
    global tag_id
    # Move to R3
    Board.setBusServoPulse(5, 660, 700)
    time.sleep(1)
    Board.setBusServoPulse(4, 450, 700)
    Board.setBusServoPulse(5, 510, 700)
    Board.setBusServoPulse(6, 120, 700)
    time.sleep(1)
    Board.setBusServoPulse(3, 300, 700)
    Board.setBusServoPulse(4, 560, 700)
    Board.setBusServoPulse(5, 380, 700)
    time.sleep(1)
    time.sleep(0.5)
    # Grap from R3 and place to target point
    Board.setBusServoPulse(1, 550, 700)
    time.sleep(1)
    Board.setBusServoPulse(4, 450, 700)
    time.sleep(1)
    Board.setBusServoPulse(6, 500, 700)
    time.sleep(1)
    Board.setBusServoPulse(3, 250, 700)
    Board.setBusServoPulse(4, 800, 700)
    Board.setBusServoPulse(5, 560, 700)
    time.sleep(1)
    Board.setBusServoPulse(1, 300, 700)
    time.sleep(1)
    # detect if successfully grapped
    Board.setBusServoPulse(4, 450, 700)
    Board.setBusServoPulse(5, 510, 700)
    time.sleep(1)
    Board.setBusServoPulse(6, 120, 700)
    time.sleep(1)
    Board.setBusServoPulse(3, 300, 700)
    Board.setBusServoPulse(4, 700, 700)
    time.sleep(1)
    time.sleep(0.5)
    tag_family, tag_id = apriltagDetect()
    print("id", tag_id)
    if tag_id is not None:
        print("failed to grap")
    else:
        print("successfully grapped")
    Board.setBusServoPulse(3, 250, 700)
    Board.setBusServoPulse(4, 450, 700)
    time.sleep(1)


def actL1():
    global tag_id
    # Move to L1
    Board.setBusServoPulse(5, 660, 700)
    time.sleep(1)
    Board.setBusServoPulse(6, 880, 700)
    time.sleep(1)
    Board.setBusServoPulse(3, 130, 700)
    Board.setBusServoPulse(4, 680, 700)
    Board.setBusServoPulse(5, 500, 700)
    time.sleep(1)
    Board.setBusServoPulse(4, 740, 700)
    time.sleep(1)
    Board.setBusServoPulse(3, 300, 700)
    Board.setBusServoPulse(5, 400, 700)
    time.sleep(1)
    Board.setBusServoPulse(3, 370, 700)
    Board.setBusServoPulse(4, 760, 700)
    Board.setBusServoPulse(5, 360, 700)
    time.sleep(1)
    time.sleep(0.5)
    # Grap from L1
    Board.setBusServoPulse(1, 550, 700)
    time.sleep(1)
    Board.setBusServoPulse(3, 320, 700)
    Board.setBusServoPulse(5, 385, 700)
    time.sleep(1)
    Board.setBusServoPulse(3, 260, 700)
    Board.setBusServoPulse(5, 415, 700)
    time.sleep(1)
    Board.setBusServoPulse(4, 800, 700)
    Board.setBusServoPulse(5, 450, 700)
    time.sleep(1)
    Board.setBusServoPulse(4, 850, 700)
    Board.setBusServoPulse(5, 500, 700)
    time.sleep(1)
    Board.setBusServoPulse(5, 680, 700)
    time.sleep(1)
    # detect if successfully grapped
    tag_family, tag_id = apriltagDetect()
    if tag_id is not None:
        print("successfully grapped")
        # place to target point
        Board.setBusServoPulse(6, 500, 700)
        time.sleep(1)
        Board.setBusServoPulse(5, 600, 700)
        time.sleep(1)
        Board.setBusServoPulse(1, 300, 700)
        time.sleep(1)
    else:
        print("failed to grap")
    time.sleep(0.5)


def actL2():
    global tag_id
    # Move to L2
    Board.setBusServoPulse(5, 660, 700)
    time.sleep(1)
    Board.setBusServoPulse(4, 450, 700)
    Board.setBusServoPulse(5, 510, 700)
    Board.setBusServoPulse(6, 870, 700)
    time.sleep(1)
    Board.setBusServoPulse(4, 600, 700)
    Board.setBusServoPulse(5, 410, 700)
    time.sleep(1)
    Board.setBusServoPulse(3, 230, 700)
    Board.setBusServoPulse(4, 640, 700)
    time.sleep(1)
    Board.setBusServoPulse(3, 310, 700)
    Board.setBusServoPulse(4, 680, 700)
    time.sleep(1)
    time.sleep(0.5)
    # Grap from L2
    Board.setBusServoPulse(1, 550, 700)
    time.sleep(1)
    Board.setBusServoPulse(3, 250, 700)
    Board.setBusServoPulse(4, 640, 700)
    time.sleep(1)
    Board.setBusServoPulse(3, 200, 700)
    Board.setBusServoPulse(4, 610, 700)
    time.sleep(1)
    Board.setBusServoPulse(3, 150, 700)
    Board.setBusServoPulse(4, 570, 700)
    time.sleep(1)
    Board.setBusServoPulse(3, 100, 700)
    Board.setBusServoPulse(4, 530, 700)
    time.sleep(1)
    Board.setBusServoPulse(3, 80, 700)
    Board.setBusServoPulse(4, 450, 700)
    Board.setBusServoPulse(5, 510, 700)
    time.sleep(1)
    # detect if successfully grapped
    tag_family, tag_id = apriltagDetect()
    if tag_id is not None:
        print("successfully grapped")
        Board.setBusServoPulse(6, 500, 700)
        time.sleep(1)
        Board.setBusServoPulse(4, 625, 700)
        Board.setBusServoPulse(5, 435, 700)
        time.sleep(1)
        Board.setBusServoPulse(1, 300, 700)
        time.sleep(1)
    else:
        print("failed to grap")
    time.sleep(0.5)


def actL3():
    global tag_id
    # Move to L3
    Board.setBusServoPulse(5, 660, 700)
    time.sleep(1)
    Board.setBusServoPulse(4, 450, 700)
    Board.setBusServoPulse(5, 510, 700)
    Board.setBusServoPulse(6, 870, 700)
    time.sleep(1)
    Board.setBusServoPulse(3, 300, 700)
    Board.setBusServoPulse(4, 560, 700)
    Board.setBusServoPulse(5, 380, 700)
    time.sleep(1)
    time.sleep(0.5)
    # Grap from L3 and place to target point
    Board.setBusServoPulse(1, 550, 700)
    time.sleep(1)
    Board.setBusServoPulse(4, 450, 700)
    time.sleep(1)
    Board.setBusServoPulse(6, 500, 700)
    time.sleep(1)
    Board.setBusServoPulse(3, 250, 700)
    Board.setBusServoPulse(4, 800, 700)
    Board.setBusServoPulse(5, 560, 700)
    time.sleep(1)
    Board.setBusServoPulse(1, 300, 700)
    time.sleep(1)
    time.sleep(0.5)
    # detect if successfully grapped
    Board.setBusServoPulse(4, 450, 700)
    Board.setBusServoPulse(5, 510, 700)
    time.sleep(1)
    Board.setBusServoPulse(6, 870, 700)
    time.sleep(1)
    Board.setBusServoPulse(3, 300, 700)
    Board.setBusServoPulse(4, 700, 700)
    time.sleep(1)
    time.sleep(0.5)
    tag_family, tag_id = apriltagDetect()
    if tag_id is not None:
        print("failed to grap")
    else:
        print("successfully grapped")
    Board.setBusServoPulse(3, 250, 700)
    Board.setBusServoPulse(4, 450, 700)
    time.sleep(1)


def mix():
    global tag_id
    ini_pos()
    Board.setBusServoPulse(4, 550, 700)
    Board.setBusServoPulse(5, 320, 700)
    time.sleep(1)
    Board.setBusServoPulse(2, 1000, 700)
    time.sleep(1)
    Board.setBusServoPulse(2, 0, 700)
    time.sleep(1)
    Board.setBusServoPulse(2, 1000, 700)
    time.sleep(1)
    Board.setBusServoPulse(2, 0, 700)
    time.sleep(1)
    Board.setBusServoPulse(2, 1000, 700)
    time.sleep(1)
    Board.setBusServoPulse(2, 0, 700)
    time.sleep(1)
    Board.setBusServoPulse(2, 1000, 700)
    time.sleep(1)
    Board.setBusServoPulse(2, 0, 700)
    time.sleep(1)


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
            if command == "1":
                actR1()
                mix()
            elif command == "2":
                actR2()
                mix()
            elif command == "3":
                actR3()
                mix()
            elif command == "4":
                actL1()
                mix()
            elif command == "5":
                actL2()
                mix()
            elif command == "6":
                actL3()
                mix()
            elif command == "7":
                mix()
            # TODO: 動作做完後設定running為False !!!
            # 任務執行完畢
            ini_pos()
            running = False
            return make_response("<h1>Success</h1>", 200)
        elif running:
            print("正在執行，請稍後", "\n\n\n\n")
            return make_response("<h1>Running</h1>", 201)
    else:
        return make_response("<h1>Failed</h1>", 400)


if __name__ == "__main__":
    ini_pos()
    cap = cv2.VideoCapture(-1)
    cap.release()
    cv2.destroyAllWindows()

    if mode == "local":
        # localhost運行模式
        app.run(debug=True, port=5001)
    else:
        # 使用LAN_IP打開服務器模式
        print("Server is running", mode, "mode\n\n\n\n")
        # Board.setBusServoPulse(5, 0, 700)
        # 臨時SSL證書
        # app.run(host=LAN_IP, debug=True, port=5001, ssl_context="adhoc")
        # 本地自部署SSL證書
        app.run(
            host=LAN_IP,
            debug=False,
            port=5002,
            ssl_context=("cert.pem", "key.pem"),
        )
        # 無證書運行模式
        # app.run(host=LAN_IP, debug=True, port=5001)
