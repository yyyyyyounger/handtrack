# 機械臂端API代碼
機械臂端使用樹莓派連接某局域網，直接充當API服務器接收指令。

## 啟動前
1. 需安裝 `flask` 和 `flask_cors` 庫

    使用 `pip install flask`
    使用 `pip install flask_cors`

## 啟動
1. 使用 `python api.py` 啟動
2. 觀察控制台的輸出，會顯示當前機械臂在局域網內的IP，記錄這個IP填寫到前端服務器中。

## 其他
`./handTrackPython0412/` 為存檔文件夾
`./robotVersion/` 為真實機械臂端使用的穩定版代碼