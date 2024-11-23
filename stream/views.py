import sys
import logging
from django.shortcuts import render
from django.http import StreamingHttpResponse
import cv2
import numpy as np

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize global variables
camera = None
net = None

# Define the model paths
prototxt_path = r'C:\Users\Arisu\PycharmProjects\botStream\models\deploy.prototxt'
caffe_model_path = r'C:\Users\Arisu\PycharmProjects\botStream\models\mobilenet_iter_73000.caffemodel'

# Load the MobileNet SSD model
try:
    net = cv2.dnn.readNetFromCaffe(prototxt_path, caffe_model_path)
    logger.info("MobileNet SSD model loaded successfully.")
except Exception as e:
    logger.error(f"Error loading MobileNet SSD model: {e}")

# Initialize the local webcam
try:
    camera = cv2.VideoCapture(0)  # Use the local webcam (index 0)
    if not camera.isOpened():
        logger.error("Error: Could not open local webcam.")
except Exception as e:
    logger.error(f"Error initializing camera: {e}")


# Main index view
def index(request):
    return render(request, 'index.html')


# Function to generate frames from the local webcam with MobileNet SSD detection
def gen_frames():
    global net, camera
    if net is None:
        logger.error("MobileNet SSD model is not loaded. Unable to process frames.")
        return
    if camera is None or not camera.isOpened():
        logger.info("Reinitializing local webcam...")
        camera = cv2.VideoCapture(0)  # Reinitialize with the local webcam
        if not camera.isOpened():
            logger.error("Local webcam is not initialized. Unable to capture frames.")
            return

    try:
        while True:
            # Capture frame-by-frame
            success, frame = camera.read()
            if not success:
                logger.warning("Failed to capture frame from camera.")
                break
            else:
                # Prepare the frame for MobileNet SSD model
                h, w = frame.shape[:2]
                blob = cv2.dnn.blobFromImage(frame, 0.007843, (300, 300), (127.5, 127.5, 127.5), swapRB=True,
                                             crop=False)

                # Set the input to the network and run forward pass
                net.setInput(blob)
                detections = net.forward()

                # Loop through detections
                for i in range(detections.shape[2]):
                    confidence = detections[0, 0, i, 2]  # Confidence score

                    if confidence > 0.2:  # Filter by confidence threshold
                        # Get object class ID and bounding box coordinates
                        class_id = int(detections[0, 0, i, 1])
                        x1 = int(detections[0, 0, i, 3] * w)
                        y1 = int(detections[0, 0, i, 4] * h)
                        x2 = int(detections[0, 0, i, 5] * w)
                        y2 = int(detections[0, 0, i, 6] * h)

                        # Draw bounding box and label
                        if class_id == 15:  # Class ID 15 corresponds to 'person' in MobileNet SSD
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                            label = f'Person {confidence:.2f}'
                            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Encode the frame with bounding boxes
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()

                # Yield the frame as part of a multipart response
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    finally:
        # Release the camera after streaming is complete
        if camera is not None:
            camera.release()
            logger.info("Camera released.")


# Django view to handle the video stream
def video_feed(request):
    return StreamingHttpResponse(gen_frames(), content_type='multipart/x-mixed-replace; boundary=frame')
