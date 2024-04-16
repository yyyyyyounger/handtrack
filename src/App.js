import { useCallback, useEffect, useRef, useState, } from "react";

import Webcam from "react-webcam";
import { Holistic, FACEMESH_TESSELATION, HAND_CONNECTIONS, POSE_CONNECTIONS, } from '@mediapipe/holistic';
import { Camera } from "@mediapipe/camera_utils";
import { drawConnectors, drawLandmarks, } from "@mediapipe/drawing_utils";
import axios from "axios";

// 定义一个函数来模拟 math.degrees()
function degrees(radians) {
  return radians * (180 / Math.PI);
}

let leftCount = 0;
let leftPos = '';
let rightCount = 0;
let rightPos = '';

let humanCommand = null;

const commandMap = {
  1: '一號',
  2: '二號',
  3: '三號',
  4: '四號',
  5: '五號',
  6: '六號',
}

function App() {
  const webcamRef = useRef(null);
  const canvasRef = useRef(null);

  const [renderCommand, setCommand] = useState(null);
  const [callState, setDo] = useState(null);

  // 根據兩點的座標，計算角度
  const vector_2d_angle = (v1, v2) => {
    let v1_x = v1[0]
    let v1_y = v1[1]
    let v2_x = v2[0]
    let v2_y = v2[1]
    let angle_ = degrees(Math.acos((v1_x * v2_x + v1_y * v2_y) / (((v1_x ** 2 + v1_y ** 2) ** 0.5) * ((v2_x ** 2 + v2_y ** 2) ** 0.5))));
    // angle_ = 180
    return angle_
  }

  // 根據傳入的 21 個節點座標，得到該手指的角度
  const hand_angle = (hand_) => {
    let angle_list = [];
    // # thumb 大拇指角度
    let angle_ = vector_2d_angle(
      [(Number(hand_[0].x) - Number(hand_[2].x)), (Number(hand_[0].y) - Number(hand_[2].y))],
      [(Number(hand_[3].x) - Number(hand_[4].x)), (Number(hand_[3].y) - Number(hand_[4].y))]
    );
    angle_list.push(angle_);
    // # index 食指角度
    angle_ = vector_2d_angle(
      [(Number(hand_[0].x) - Number(hand_[6].x)), (Number(hand_[0].y) - Number(hand_[6].y))],
      [(Number(hand_[7].x) - Number(hand_[8].x)), (Number(hand_[7].y) - Number(hand_[8].y))]
    )
    angle_list.push(angle_)
    // # middle 中指角度
    angle_ = vector_2d_angle(
      [(Number(hand_[0].x) - Number(hand_[10].x)), (Number(hand_[0].y) - Number(hand_[10].y))],
      [(Number(hand_[11].x) - Number(hand_[12].x)), (Number(hand_[11].y) - Number(hand_[12].y))]
    )
    angle_list.push(angle_)
    // # ring 無名指角度
    angle_ = vector_2d_angle(
      [(Number(hand_[0].x) - Number(hand_[14].x)), (Number(hand_[0].y) - Number(hand_[14].y))],
      [(Number(hand_[15].x) - Number(hand_[16].x)), (Number(hand_[15].y) - Number(hand_[16].y))]
    )
    angle_list.push(angle_)
    // # pink 小拇指角度
    angle_ = vector_2d_angle(
      [(Number(hand_[0].x) - Number(hand_[18].x)), (Number(hand_[0].y) - Number(hand_[18].y))],
      [(Number(hand_[19].x) - Number(hand_[20].x)), (Number(hand_[19].y) - Number(hand_[20].y))]
    )
    angle_list.push(angle_)
    // console.log('angle_list', angle_list);
    return angle_list
  }

  // # 根據手指角度的串列內容，返回對應的手勢名稱
  const hand_pos = (finger_angle) => {
    let f1 = finger_angle[0]   // 大拇指角度
    let f2 = finger_angle[1]   // 食指角度
    let f3 = finger_angle[2]   // 中指角度
    let f4 = finger_angle[3]   // 無名指角度
    let f5 = finger_angle[4]   // 小拇指角度

    // 小於 50 表示手指伸直，大於等於 50 表示手指捲縮
    if (f1 < 50 && f2 >= 50 && f3 >= 50 && f4 >= 50 && f5 >= 50) {
      return 'good'
    }
    else if (f1 >= 50 && f2 >= 50 && f3 < 50 && f4 >= 50 && f5 >= 50) {
      return 'no!!!'
    }
    else if (f1 < 50 && f2 < 50 && f3 >= 50 && f4 >= 50 && f5 < 50) {
      return 'ROCK!'
    }
    else if (f1 >= 50 && f2 >= 50 && f3 >= 50 && f4 >= 50 && f5 >= 50) {
      return '0'
    }
    else if (f1 >= 50 && f2 >= 50 && f3 >= 50 && f4 >= 50 && f5 < 50) {
      return 'pink'
    }
    else if (f1 >= 50 && f2 < 50 && f3 >= 50 && f4 >= 50 && f5 >= 50) {
      return '1'
    }
    else if (f1 >= 50 && f2 < 50 && f3 < 50 && f4 >= 50 && f5 >= 50) {
      return '2'
    }
    else if (f1 >= 50 && f2 >= 50 && f3 < 50 && f4 < 50 && f5 < 50) {
      return 'ok'
    }
    else if (f1 < 50 && f2 >= 50 && f3 < 50 && f4 < 50 && f5 < 50) {
      return 'ok'
    }
    else if (f1 >= 50 && f2 < 50 && f3 < 50 && f4 < 50 && f5 > 50) {
      return '3'
    }
    else if (f1 >= 50 && f2 < 50 && f3 < 50 && f4 < 50 && f5 < 50) {
      return '4'
    }
    else if (f1 < 50 && f2 < 50 && f3 < 50 && f4 < 50 && f5 < 50) {
      return '5'
    }
    else if (f1 < 50 && f2 >= 50 && f3 >= 50 && f4 >= 50 && f5 < 50) {
      return '6'
    }
    else if (f1 < 50 && f2 < 50 && f3 >= 50 && f4 >= 50 && f5 >= 50) {
      return '7'
    }
    else if (f1 < 50 && f2 < 50 && f3 < 50 && f4 >= 50 && f5 >= 50) {
      return '8'
    }
    else if (f1 < 50 && f2 < 50 && f3 < 50 && f4 < 50 && f5 >= 50) {
      return '9'
    }
    else return ''
  }

  useEffect(() => {
    const holistic = new Holistic({
      locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/holistic/${file}`
    });
    const onResults = (res) => {
      if (!webcamRef.current?.video || !canvasRef.current) return
      const videoWidth = webcamRef.current.video.videoWidth;
      const videoHeight = webcamRef.current.video.videoHeight;
      canvasRef.current.width = videoWidth;
      canvasRef.current.height = videoHeight;

      const canvasElement = canvasRef.current;
      const canvasCtx = canvasElement.getContext("2d");
      if (canvasCtx == null) throw new Error('Could not get context');
      canvasCtx.save();
      canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);

      // Only overwrite existing pixels.
      canvasCtx.globalCompositeOperation = 'source-in';
      canvasCtx.fillRect(0, 0, canvasElement.width, canvasElement.height);

      // Only overwrite missing pixels.
      canvasCtx.globalCompositeOperation = 'destination-atop';
      canvasCtx.drawImage(res.image, 0, 0, canvasElement.width, canvasElement.height);

      canvasCtx.globalCompositeOperation = 'source-over';

      // 分解手勢
      // 1. 識別到對應手勢指令
      // 2. 等待 5s 確認指令
      // 無確認
      //    重新回1. 
      // 有確認
      //    傳送該指令，重新回1.

      let right_hand_res = res.rightHandLandmarks;
      if (!!right_hand_res) {
        let nowPos = hand_pos(hand_angle(right_hand_res)); // 此刻識別的手勢
        // 當前手勢與上次記錄的手勢不同
        if (rightPos != nowPos) {
          // 記錄的手勢是所需指令之一，當前是確認指令
          if ((humanCommand == '1' || humanCommand == '2' || humanCommand == '3' || humanCommand == '4' || humanCommand == '5' || humanCommand == '6')
            && nowPos == 'good') {
            rightCount = rightCount + 1;
            if (rightCount >= 20) {
              setDo(true);
              console.log('檢測到確認指令!!!!!!');
              // 本地開發
              // let URL = `http://127.0.0.1:5001/do?pw=abcd1234&command=${humanCommand}`;
              // 遠端測試
              let URL = `https://192.168.236.22:5001/do?pw=abcd1234&command=${humanCommand}`;

              // 通知機械臂執行
              // axios({ method: 'get', url: URL, })
              //   .then(res => {
              //     setCommand(humanCommand);
              //     console.log('res', res);
              //   }).catch(err => {
              //     setCommand('error');
              //     console.log('err', err);
              //   })
              fetch(URL, { rejectUnauthorized: false })
                .then(res => {
                  setCommand(humanCommand);
                  console.log('res', res);
                })
                .catch(err => {
                  setCommand('error');
                  console.log('err', err);
                });
              rightCount = 0;
              humanCommand = null;
              rightPos = null;
            }
          }
          // 更新記錄的手勢，用於啟動計數器
          else {
            rightPos = nowPos;
            rightCount = 0;
          }
        }
        // 當前手勢與記錄手勢相同
        else {
          // 啟動手勢計數器
          rightCount = rightCount + 1;
          if (rightCount >= 20) {
            rightCount = 0;
            humanCommand = rightPos;
            setCommand(humanCommand);
            setDo(false);
            console.log('當前 Right 指令:', humanCommand, '\n');
          }
        }
      }

      // 姿勢
      // drawConnectors(canvasCtx, res.poseLandmarks, POSE_CONNECTIONS,
      //   {color: '#00FF00', lineWidth: 4});
      // drawLandmarks(canvasCtx, res.poseLandmarks,
      //   {color: '#FF0000', lineWidth: 2});

      // 臉部
      // drawConnectors(canvasCtx, res.faceLandmarks, FACEMESH_TESSELATION,
      //   { color: '#C0C0C070', lineWidth: 1 });

      // 手
      drawConnectors(canvasCtx, res.leftHandLandmarks, HAND_CONNECTIONS, { color: '#1565c0', lineWidth: 5 });
      drawLandmarks(canvasCtx, res.leftHandLandmarks, { color: '#00FF00', lineWidth: 2 });
      drawConnectors(canvasCtx, res.rightHandLandmarks, HAND_CONNECTIONS, { color: '#00CC00', lineWidth: 5 });
      drawLandmarks(canvasCtx, res.rightHandLandmarks, { color: '#FF0000', lineWidth: 2 });

      canvasCtx.restore();
    }

    holistic.setOptions({
      // selfieMode: true,
      modelComplexity: 1,
      smoothLandmarks: true,
      enableSegmentation: true,
      smoothSegmentation: true,
      // refineFaceLandmarks: true,
      minDetectionConfidence: 0.6,
      minTrackingConfidence: 0.9
    });
    holistic.onResults(onResults);


    if (typeof webcamRef.current !== "undefined" && webcamRef.current !== null) {
      if (!webcamRef.current.video) return
      const camera = new Camera(webcamRef.current.video, {
        onFrame: async () => {
          if (!webcamRef.current.video) return
          await holistic.send({ image: webcamRef.current.video });
        },
        width: 640, height: 480,
      });

      camera.start();
    }

    return () => { }
  }, []);

  return (
    <div style={{}}>

      <meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests" />

      <Webcam ref={webcamRef} style={{ width: '800px', }} hidden mirrored={true} />

      <h1>手勢識別炒菜助手</h1>

      <div style={{ display: 'flex' }}>
        {renderCommand == 'error' ? (<p>{'出現錯誤!!!'}</p>) : (
          <>
            <p>{renderCommand ? commandMap[renderCommand] : '等候指令...'}</p>
            {callState ? (<p>{'執行!'}</p>) : null}
          </>)
        }
      </div >

      <div>
        <canvas
          ref={canvasRef}
          style={{
            // position: "absolute",
            // marginLeft: "auto",
            // marginRight: "auto",
            // left: 0,
            // right: 0,
            // textAlign: "center",
            zIndex: 9,
            // width: 1200,
            // height: 800,
            width: 800,
            // height: 800,
            transform: `scaleX(-1)`,
          }}
        />
      </div>

    </div >
  );
}

export default App;
