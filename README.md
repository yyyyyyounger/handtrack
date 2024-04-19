# 前端聯動機械臂
## 2024 UM ECEN3025 課程作業

### 運行前
1. 命令行使用 `npm i` 安裝所需庫，如沒有npm命令，還需要安裝 `node.js` 。

2. 修改[`./src/App.js`](./src/App.js)中大概第 9 行的ip地址，查看連接WiFi時自己的LAN IP。
`LOCAL_HOST` 為電腦端IP，`REMOTE_HOST` 為機械臂端IP（可在機械臂運行API服務器時查看）。

### 運行
#### 打開前端服務器
1. 在電腦端運行本地服務器，供前端加載靜態Model。
```console
cd handtrackPython
python api.py
```
2. 使用`yarn start`開啟前端服務器，默認在3000端口，可在瀏覽器中通過 `localhost:3000` 打開。（檢查自己使用HTTPS還是HTTP啟動參數）

npm 啟動參數 `"start": "HTTPS=true SSL_CRT_FILE=cert.pem SSL_KEY_FILE=key.pem react-scripts start"`

#### 打開機械臂端服務器
1. 啟動Python API服務器，在實際環境中部署在機械臂上。具體參考 [`./handtrackPython/README.md`](./handtrackPython/README.md)。

2. 局域網內，還可以使用手機或其他PC連接到該前端服務器。