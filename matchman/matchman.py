from flask import Flask, request, jsonify
import tensorflow as tf
import cv2
import numpy as np

app = Flask(__name__)

# Load MoveNet model
interpreter = tf.lite.Interpreter(model_path="movenet_thunder.tflite")
interpreter.allocate_tensors()

# Define endpoints for API


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


if __name__ == "__main__":
    app.run(debug=True)
