import cv2
from ultralytics import solutions
import os

# Input YouTube URL
video_path = 'video.mp4' # path to your video

# Initialize Video Capture
#cap = cv2.VideoCapture(0) # for your webcam input
cap = cv2.VideoCapture(video_path) # for external videos
assert cap.isOpened(), "Error reading video file"
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
video_writer = cv2.VideoWriter("workouts.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

# Init AIGym
gym = solutions.AIGym(
    show=False,  # Set to False because we are using cv2.imshow for real-time display
    kpts=[6, 8, 10],  # Keypoints index of person for monitoring specific exercise
    model="yolo11n-pose.pt",  # Path to the YOLO11 pose estimation model file
)

# Process video and display in real-time
while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Video frame is empty or video processing has been successfully completed.")
        break
    im0 = gym.monitor(cv2.resize(frame, (600, 300)))
    video_writer.write(im0)
    cv2.imshow("Workout Monitoring", im0)

    # Display the processed frame in real-time
    #cv2.imshow("Workout Monitoring", processed_frame)

    # Break on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()


import os
import cv2
from flask import Flask, render_template, Response
import atexit

# This is a simplified version for debugging.
# It does NOT include the AI push-up counting.

app = Flask(__name__)
camera = None

def get_camera():
    global camera
    if camera is None:
        CAMERA_INDEX = 1  # Make sure this is still your correct camera index
        print(f"DEBUG: Attempting to open camera at index: {CAMERA_INDEX}")
        camera = cv2.VideoCapture(CAMERA_INDEX)
        if not camera.isOpened():
            print(f"!!! CRITICAL: Could not start camera at index {CAMERA_INDEX}. !!!")
            raise RuntimeError(f"Could not start camera at index {CAMERA_INDEX}.")
        print("DEBUG: Camera opened successfully.")
    return camera

def release_camera():
    global camera
    if camera and camera.isOpened():
        camera.release()
        print("DEBUG: Camera released.")

atexit.register(release_camera)

def generate_frames_simple():
    """
    This function now ONLY captures frames and streams them.
    All AI processing has been removed for this test.
    """
    try:
        cap = get_camera()
        while True:
            # Read a frame from the camera
            success, frame = cap.read()
            if not success:
                print("DEBUG: Failed to read frame from camera. Ending stream.")
                break

            # Encode the raw frame into JPEG format
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                print("DEBUG: Failed to encode frame.")
                continue
            
            frame_bytes = buffer.tobytes()

            # Yield the frame to the browser
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    except Exception as e:
        print(f"An error occurred in generate_frames_simple: {e}")

@app.route('/')
def index():
    return render_template('pala.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames_simple(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    if not os.path.exists('templates'):
        os.makedirs('templates')
    app.run(port=5000, debug=True, threaded=True, use_reloader=False)

