import cv2
import os
import numpy as np

# Paths to model files and test image
model_prototxt = "media/age_model/age_deploy.prototxt"
model_caffemodel = "media/age_model/age_net.caffemodel"
test_image_path = "static/images/cardio.jpg"

# Validate file existence
if not all([os.path.exists(model_prototxt), os.path.exists(model_caffemodel), os.path.exists(test_image_path)]):
    raise FileNotFoundError("Error: One or more files do not exist. Check file paths.")

# Load the model
net = cv2.dnn.readNetFromCaffe(model_prototxt, model_caffemodel)
print("Model loaded successfully.")

# Load and preprocess image
image = cv2.imread(test_image_path)
if image is None:
    raise ValueError("Error: Failed to load the test image.")

print(f"Image shape: {image.shape}")
blob = cv2.dnn.blobFromImage(image, scalefactor=1.0, size=(224, 224), mean=(104, 117, 123), swapRB=False, crop=False)
net.setInput(blob)

# Inspect and debug specific layers
layer_names = net.getLayerNames()
for i, layer in enumerate(layer_names):
    try:
        print(f"Processing layer {i + 1}/{len(layer_names)}: {layer}")
        output = net.forward(layer)
        print(f"Layer {layer} output shape: {output.shape}")
    except cv2.error as e:
        print(f"OpenCV error in layer {layer}: {e}")
        print(f"Check the weights and input blob shape for the layer.")
        break
    except Exception as e:
        print(f"Unexpected error in layer {layer}: {e}")
        break
