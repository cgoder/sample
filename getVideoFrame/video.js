// // 获取网页元素
// const videoUrlInput = document.getElementById('video-url');
// const videoElement = document.getElementById('video');
// const canvasElement = document.getElementById('canvas');

// // 处理表单提交事件
// document.querySelector('form').addEventListener('submit', function(event) {
// 	event.preventDefault(); // 阻止表单默认行为

// 	const videoUrl = videoUrlInput.value;

// 	// 创建视频元素
// 	videoElement.src = videoUrl;

// 	// 监听视频元素加载事件
// 	videoElement.addEventListener('loadedmetadata', function() {
// 		// 设置画布尺寸
// 		canvasElement.width = videoElement.videoWidth;
// 		canvasElement.height = videoElement.videoHeight;

// 		// 每隔100毫秒获取一次图像帧
// 		setInterval(function() {
// 			// 将视频当前时间设置为下一帧
// 			videoElement.currentTime += 0.1;

// 			// 在画布上绘制当前帧
// 			canvasElement.getContext('2d').drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);
// 		}, 100);
// 	});
// });

const videoUrlInput = document.getElementById("video-url");
const videoElement = document.getElementById("video");
const canvasElement = document.getElementById("canvas");

let lastFrameTime = 0;

document.querySelector("form").addEventListener("submit", function (event) {
  event.preventDefault();

  const videoUrl = videoUrlInput.value;

  videoElement.src = videoUrl;

  videoElement.addEventListener("loadedmetadata", function () {
    canvasElement.width = videoElement.videoWidth;
    canvasElement.height = videoElement.videoHeight;

    // 请求第一帧图像
    videoElement.requestVideoFrameCallback(drawFrame);
  });
});

function drawFrame(now, metadata) {
  // 如果当前时间与上一帧时间相同，则跳过该帧
  if (now === lastFrameTime) {
    metadata.currentTime += 0.1;
    videoElement.requestVideoFrameCallback(drawFrame);
    return;
  }

  // 在画布上绘制当前帧
  canvasElement
    .getContext("2d")
    .drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);

  // 记录上一帧时间
  lastFrameTime = now;

  // 请求下一帧图像
  metadata.currentTime += 0.1;
  videoElement.requestVideoFrameCallback(drawFrame);
}
