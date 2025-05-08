import cv2
import os

proto_file = r"C:\Users\HP\health_project\models\pose\pose_deploy_linevec.prototxt"
weights_file = r"C:\Users\HP\health_project\models\pose\pose_iter_440000.caffemodel"

# Check if files exist
if not os.path.exists(proto_file):
    print(f"Proto file not found: {proto_file}")
if not os.path.exists(weights_file):
    print(f"Weights file not found: {weights_file}")

# Attempt to load the network
net = cv2.dnn.readNetFromCaffe(proto_file, weights_file)
print("Model loaded successfully")
