import cv2
import mediapipe as mp
from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import threading
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

lock = threading.Lock()
face_pos = [0.5, 0.5]   # 使用列表以便修改

mp_face_detection = mp.solutions.face_detection
face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)

def face_detection_loop():
    global face_pos
    print("🔥 摄像头线程启动成功")
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ 摄像头打不开！")
        return
    print("✅ 摄像头已打开")
    while True:
        success, frame = cap.read()
        if not success:
            print("❌ 读取帧失败")
            break
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(frame_rgb)
        if results.detections:
            print("✅ 检测到人脸！")
            detection = results.detections[0]
            bbox = detection.location_data.relative_bounding_box
            x = bbox.xmin + bbox.width/2
            y = bbox.ymin + bbox.height/2
            with lock:
                face_pos[0] = x
                face_pos[1] = y
            print(f"📤 已写入新坐标: x={x:.3f}, y={y:.3f}")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/face-data')
def get_face_data():
    with lock:
        print(f"📥 接口返回: x={face_pos[0]:.3f}, y={face_pos[1]:.3f}")
        return jsonify({"x": face_pos[0], "y": face_pos[1]})

if __name__ == '__main__':
    # 只在子进程中启动线程（当 debug=True 且使用 reloader 时）
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        threading.Thread(target=face_detection_loop, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)