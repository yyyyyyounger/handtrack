# 前端聯動機械臂
## 2024 UM ECEN3025 課程作業

### 啟動前
1. 命令行使用 `npm i` 安裝所需庫，如沒有npm命令，還需要安裝 `node.js` 。

2. 修改[`./src/App.js`](./src/App.js)中大概第 9 行的ip地址，**為當前WiFi/局域網內計劃運行前端服務器設備的LAN IP**。
`LOCAL_HOST` 為電腦端IP（前端服務器），`REMOTE_HOST` 為機械臂端IP（可在機械臂運行API服務器時查看）。

### 啟動
#### 1. 打開機械臂端服務器
1. 啟動Python API服務器，在實際環境中部署在機械臂上。具體參考 [`./handtrackPython/README.md`](./handtrackPython/README.md)。

#### 2. 打開前端服務器
1. 在電腦端運行本地服務器，供前端加載靜態Model。
```console
cd handtrackPython
python api.py
```
1. 使用`yarn start`開啟前端服務器，默認在3000端口，可在瀏覽器中通過 `localhost:3000` 打開。（檢查自己使用HTTPS還是HTTP啟動參數）

npm 啟動參數 `"start": "HTTPS=true SSL_CRT_FILE=cert.pem SSL_KEY_FILE=key.pem react-scripts start"`

2. 局域網內，還可以使用手機或其他PC連接到該前端服務器。

#### 3. 使用其他設備連接到機械臂和前端
1. 由於沒有申請可信證書，前端和機械臂服務器使用了移動設備上不可信的 `https` 協議（尤其iOS設備）。
2. 建議製作 `https://LOCAL_HOST:5001`, `https://REMOTE_HOST:5002` 的 QRcode，方便手機掃描，然後點擊**信任該服務器**，才會正確在服務器上加載資源。
3. 最後前往前端服務器 `https://LOCAL_HOST:3000` 即可開始前端的代碼邏輯。

---
API服務器和前端服務器啟動時有可能發生端口佔用報錯，如有發生，可按照控制台的說明更改網址端口！
---