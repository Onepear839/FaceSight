import * as THREE from 'three';

// 初始化 Three.js
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// 创建一个立方体（代表你的 3D 展示柜/牛角包）
const geometry = new THREE.BoxGeometry(1, 1, 1);
const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
const cube = new THREE.Mesh(geometry, material);
scene.add(cube);
camera.position.z = 5;

// 连接 SocketIO，接收人脸位置
const socket = io();
let targetX = 0, targetY = 0;

socket.on('face_pos', (pos) => {
    // 人脸位置（0~1）映射到相机偏移（-2~2）
    targetX = (pos.x - 0.5) * 4;
    targetY = (pos.y - 0.5) * 4;
});

// 动画循环：平滑跟随人脸
function animate() {
    requestAnimationFrame(animate);
    cube.position.x += (targetX - cube.position.x) * 0.1;
    cube.position.y += (targetY - cube.position.y) * 0.1;
    cube.rotation.x += 0.01;
    cube.rotation.y += 0.01;
    renderer.render(scene, camera);
}
animate();