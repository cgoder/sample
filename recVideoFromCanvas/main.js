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
  ctx.clearRect(0, 0, canvasPreview.width, canvasPreview.height);
  ctx.fillStyle = "#FF0000";
  ctx.strokeStyle = "#FF0000";
  for (let i = 0; i < numKeypoints; i++) {
    const keypoint = keypoints[i];
    if (keypoint.score < 0.3) {
      continue;
    }
    ctx.beginPath();
    ctx.arc(keypoint.x, keypoint.y, 3, 0, 2 * Math.PI);
    ctx.fill();
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
    const poses = await net.estimatePoses(video);
    console.log("Got pose:", poses);
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
  // const willReadFromCanvas2d = tf
  //   .env()
  //   .getBool("CANVAS2D_WILL_READ_FREQUENTLY_FOR_GPU");
  // console.log("will", willReadFromCanvas2d);

  // 添加事件监听器
  generateBtn.addEventListener("click", async () => {
    const videoUrl = urlInput.value;
    videoPreview.crossOrigin = "anonymous";
    videoPreview.src = videoUrl;
    await videoPreview.play();
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
