async function generateVideo() {
    // Get video URL from input field
    const videoUrl = document.getElementById('video-url').value;
  
    // Send POST request to Flask server
    const response = await fetch('/generate', {
      method: 'POST',
      body: new FormData(document.getElementById('form')),
    });
    // const response = await fetch('/pose', {
    //     method: 'POST',
    //     body: new FormData(document.getElementById('form')),
    //   });
    // Read response data as a blob
    const videoData = await response.blob();
  
    // Create video element and set source to response data
    const videoElement = document.createElement('video');
    videoElement.src = URL.createObjectURL(videoData);
    videoElement.controls = true;
  
    // Add video element to page
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = '';
    resultDiv.appendChild(videoElement);
  }