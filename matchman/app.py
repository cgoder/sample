import cv2
import numpy as np
import requests
import subprocess
import tempfile
import tensorflow as tf
from flask import Flask, request, Response,render_template

# Create Flask application object
# app = Flask(__name__)
app = Flask(__name__, template_folder='./')

# Load Movenet model
interpreter = tf.lite.Interpreter(model_path='movenet_thunder.tflite')
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
interpreter.allocate_tensors()

# Define generate endpoint

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/generate', methods=['POST'])
def generate():
    # Get video URL from request data
    video_url = request.form['video_url']

    # Download video using requests library
    r = requests.get(video_url)
    video_data = r.content

    # Use FFmpeg to extract frames from video
    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as f:
        f.write(video_data)
        input_filename = f.name
    with tempfile.TemporaryDirectory() as tmpdir:
        output_template = '{}/frame-%04d.jpg'.format(tmpdir)
        subprocess.check_call(
            ['ffmpeg', '-i', input_filename, '-qscale:v', '2', output_template])

    # Process frames using Movenet model
    output_frames = []
    with tf.device('/CPU:0'):
        for i in range(1, 10000):
            input_frame = cv2.imread('{}/frame-{:04d}.jpg'.format(tmpdir, i))
            if input_frame is None:
                break
            input_frame = cv2.resize(input_frame, (256, 256))
            input_data = np.expand_dims(input_frame, axis=0)
            input_data = (input_data / 255.0) * 2.0 - 1.0
            interpreter.set_tensor(input_details[0]['index'], input_data)
            interpreter.invoke()
            output_data = interpreter.get_tensor(output_details[0]['index'])
            output_data = np.squeeze(output_data, axis=0)
            output_frames.append(output_data)

    # Use OpenCV to draw skeleton on frames
    for i, output_frame in enumerate(output_frames):
        output_frame = cv2.resize(
            output_frame, (input_frame.shape[1], input_frame.shape[0]))
        for j in range(output_frame.shape[0]):
            x, y = output_frame[j]
            if x >= 0 and y >= 0:
                cv2.circle(input_frame, (int(x), int(y)), 4, (0, 255, 0), -1)
        output_frames[i] = input_frame

    # Use FFmpeg to encode frames into new video
    with tempfile.NamedTemporaryFile(suffix='.mp4', delete=False) as f:
        output_filename = f.name
    subprocess.check_call(['ffmpeg', '-y', '-i', '{}/frame-%04d.jpg'.format(
        tmpdir), '-vcodec', 'libx264', '-pix_fmt', 'yuv420p', output_filename])

    # Read new video into memory
    with open(output_filename, 'rb') as f:
        new_video_data = f.read()

    # Clean up temporary files
    subprocess.call(['rm', input_filename])
    subprocess.call(['rm', output_filename])
    subprocess.call(['rm', '{}/frame-*.jpg'.format(tmpdir)])

    # Return new video to user
    return Response(new_video_data, mimetype='video/mp4')

@app.route("/pose", methods=["POST"])
def pose_estimation():
    # Receive input video from request
    file = request.files["file"]
    video_bytes = file.read()

    # Process input video using MoveNet model
    cap = cv2.VideoCapture(video_bytes)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (256, 256))
        input_data = np.expand_dims(frame.astype(np.float32) / 255.0, axis=0)
        interpreter.set_tensor(interpreter.get_input_details()[0]['index'], input_data)
        interpreter.invoke()
        output_data = interpreter.get_tensor(
            interpreter.get_output_details()[0]['index'])
        frames.append(output_data[0])
    cap.release()

    # Convert MoveNet output to video
    height, width = frames[0].shape[0], frames[0].shape[1]
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter('output.mp4', fourcc, 30, (width, height))
    for frame in frames:
        frame = (frame * 255.0).astype(np.uint8)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        out.write(frame)
    out.release()

    # Return output video in response
    with open("output.mp4", "rb") as f:
        video_bytes = f.read()
    return jsonify({"result": video_bytes})



# Run Flask application
if __name__ == '__main__':
    app.run()
