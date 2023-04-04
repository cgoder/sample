// 获取HTML元素
const urlInput = document.getElementById("url-input");
const generateBtn = document.getElementById("generate-btn");
const videoPreview = document.getElementById("video-preview");
const canvasPreview = document.getElementById("canvas-preview");
let downloadBtn;

// 定义变量
let net;
let video;
let ctx;
let intervalId;
let recorder;

// 加载模型
async function loadModel() {
  try {
    net = await poseDetection.createDetector(
      poseDetection.SupportedModels.MoveNet
    );
    console.log("MoveNet loaded", net);
  } catch (error) {
    console.error("Failed to load model:", error);
  }
}

// 绘制骨架
function drawSkeleton(keypoints) {
  const numKeypoints = keypoints.length;
  const colors = [
    "#FF0000", // 鼻子
    "#FF7F00", // 左眼
    "#FFFF00", // 右眼
    "#00FF00", // 左耳
    "#00FFFF", // 右耳
    "#0000FF", // 左肩
    "#8B00FF", // 右肩
    "#FF00FF", // 左肘
    "#FF1493", // 右肘
    "#FFA500", // 左手腕
    "#FFD700", // 右手腕
    "#008000", // 左臀
    "#808000", // 右臀
    "#000080", // 左膝
    "#4B0082", // 右膝
    "#800080", // 左脚踝
    "#8B4513", // 右脚踝
  ];
  const minDistance = Math.min(canvasPreview.width, canvasPreview.height) / 30;

  ctx.clearRect(0, 0, canvasPreview.width, canvasPreview.height);

  for (let i = 0; i < numKeypoints; i++) {
    const keypoint = keypoints[i];
    if (keypoint.score < 0.3) {
      continue;
    }
    const color = colors[i];
    // const radius = Math.max(
    //   minDistance * (1 - keypoint.y / canvasPreview.height),
    //   2
    // );
    const radius = 3;

    ctx.beginPath();
    ctx.fillStyle = color;
    ctx.strokeStyle = color;
    ctx.arc(keypoint.x, keypoint.y, radius, 0, 2 * Math.PI);
    ctx.fill();
    ctx.stroke();
    ctx.closePath();
  }
}

// 初始化录制器
function initRecorder() {
  downloadBtn = document.getElementById("download-btn");
  recorder = new MediaRecorder(canvasPreview.captureStream(), {
    mimeType: "video/webm;codecs=h264",
    videoBitsPerSecond: 100 * 1000,
    frameRate: 20,
  });
  recorder.ondataavailable = function (event) {
    downloadBtn.href = URL.createObjectURL(event.data);
    downloadBtn.download = "skeleton.mp4";
  };
}

// 开始录制
function startRecording() {
  recorder.start();
}

// 停止录制并下载视频
function stopRecording() {
  if (recorder && recorder.state === "recording") {
    recorder.stop();
  }
}

// 估计姿势并绘制骨架
async function estimatePose() {
  try {
    const poses = await net.estimatePoses(video,{ flipHorizontal: false });
    if (poses.length > 0) {
      drawSkeleton(poses[0].keypoints);
    }
  } catch (error) {
    console.error("Failed to estimate pose:", error);
  }
}

// 主函数
async function main() {
  video = videoPreview;
  ctx = canvasPreview.getContext("2d");

  // 添加事件监听器
  generateBtn.addEventListener("click", async () => {
    const videoUrl = urlInput.value;
    videoPreview.crossOrigin = "anonymous";
    videoPreview.src = videoUrl;
    await videoPreview.play();
  });
  videoPreview.addEventListener("loadedmetadata", function() {
    canvasPreview.width = videoPreview.videoWidth;
    canvasPreview.height = videoPreview.videoHeight;
  });
  videoPreview.addEventListener("play", async () => {
    await loadModel();
    intervalId = setInterval(() => {
      estimatePose();
    }, 1000 / 30);
    initRecorder();
    startRecording();
  });

  videoPreview.addEventListener("pause", () => {
    clearInterval(intervalId);
    stopRecording();
  });

  videoPreview.addEventListener("ended", () => {
    clearInterval(intervalId);
    stopRecording();
  });
}

// 在DOM加载完成后调用主函数
document.addEventListener("DOMContentLoaded", main);
