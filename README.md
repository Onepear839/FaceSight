# FaceSight - 人脸驱动 3D 场景交互

**FaceSight** 是一个基于计算机视觉的人脸追踪交互项目。通过摄像头实时捕捉人脸位置，驱动 Three.js 3D 场景中的摄像机视角，让用户用面部动作即可控制 3D 世界的观察角度。

## 功能特点

- **实时人脸检测** — 使用 MediaPipe 实现高性能面部检测
- **3D 场景交互** — 人脸位置映射为摄像机视角，实现沉浸式控制
- **平滑追踪** — 采用 Lerp（线性插值）算法，视角切换自然流畅
- **双通信方式** — 同时支持 REST API 轮询与 WebSocket 实时推送
- **视觉增强** — Three.js 构建的 3D 场景包含粒子系统、光照、网格地面等效果

## 项目结构

```
pythonProject2/
├── main.py                  # Flask 后端，摄像头线程与 API 接口
├── requirements.txt         # Python 依赖
├── templates/
│   ├── index.html           # 主页面：3D 场景 + 人脸控制摄像机视角
│   └── test.html            # 测试页面：显示原始人脸坐标
├── static/
│   ├── three.module.min.js  # Three.js 库
│   └── socket.io.min.js     # Socket.IO 客户端库
└── threejs/
    ├── index.html           # 备选 Three.js 页面（WebSocket 版）
    ├── main.js              # 备选前端逻辑
    └── style.css            # 样式文件
```

## 快速开始

### 环境要求

- Python 3.8 - 3.11
- 摄像头（内置或外接 USB 摄像头）

### 安装与运行

```bash
# 1. 克隆仓库
git clone https://github.com/your-username/FaceSight.git
cd FaceSight

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动服务
python main.py
```

### 访问

- 主页面（3D 场景）：[http://localhost:5000](http://localhost:5000)
- 测试页面（坐标数据）：[http://localhost:5000/test](http://localhost:5000/test)（需自行在 `main.py` 中注册路由）
- 人脸数据 API：[http://localhost:5000/face-data](http://localhost:5000/face-data)

## 技术栈

| 技术 | 用途 |
|------|------|
| **Python / Flask** | Web 服务后端 |
| **Flask-SocketIO** | WebSocket 实时通信 |
| **OpenCV** | 摄像头视频流采集 |
| **MediaPipe** | 人脸检测与坐标定位 |
| **Three.js** | 3D 场景渲染 |
| **HTML / CSS / JavaScript** | 前端界面与交互逻辑 |

## 原理说明

1. **人脸检测** — Python 后端启动独立线程调用摄像头，通过 MediaPipe 的 FaceDetection 模型检测人脸并计算面部中心坐标 `(x, y)`，坐标范围归一化为 `[0, 1]`
2. **数据传递** — 坐标数据通过 `/face-data` REST 接口或 WebSocket 实时推送给前端
3. **视角映射** — 前端接收坐标后映射为摄像机的偏航角（Yaw）和俯仰角（Pitch），并采用反转控制（面部向左移动，视角向右旋转），带来更自然的交互体验
4. **平滑动画** — 使用 Lerp 函数对目标角度进行插值，避免视角突变

## 自定义

- **控制灵敏度**：调整 `maxYaw` 和 `maxPitch` 变量控制最大视角范围
- **平滑系数**：修改 `lerpSpeed` 值控制视角跟随速度
- **检测精度**：修改 `min_detection_confidence` 参数调整人脸检测置信度阈值

## 许可证

[MIT](LICENSE)