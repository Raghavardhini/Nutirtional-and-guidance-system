import os
import cv2
import numpy as np
from tempfile import NamedTemporaryFile

# Path to the pre-trained model files
AGE_MODEL_PATH = 'media/age_model/'
PROTOTXT = os.path.join(AGE_MODEL_PATH, 'age_deploy.prototxt')
MODEL = os.path.join(AGE_MODEL_PATH, 'age_net.caffemodel')

AGE_LIST = ['(0-2)', '(4-6)', '(8-13)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']

# Load Haar Cascade for face detection
FACE_CASCADE_PATH = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)

def detect_face(image_file):
    """
    Detect face in the image and crop it.
    Args:
        image_file (str): Path to the image file.
    Returns:
        numpy.ndarray: Cropped face region or the original image if no face is detected.
    """
    # Load the image
    image = cv2.imread(image_file)
    if image is None:
        raise ValueError("Error loading image. Check the file path.")

    # Convert to grayscale for face detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    if len(faces) == 0:
        print("No face detected. Using the original image.")
        return image  # Return original image if no face is detected

    # Crop the first detected face
    x, y, w, h = faces[0]
    cropped_face = image[y:y+h, x:x+w]
    return cropped_face

def predict_age(image_file):
    """
    Predict the age group based on the provided image.
    Args:
        image_file (str): Path to the image file for age prediction.
    Returns:
        str: Predicted age group.
    """
    # Load the model
    net = cv2.dnn.readNetFromCaffe(PROTOTXT, MODEL)

    # Detect and crop face
    face = detect_face(image_file)
    face_resized = cv2.resize(face, (227, 227))  # Resize face to (227x227) for the model

    # Normalize the image and prepare it as a blob
    blob = cv2.dnn.blobFromImage(face_resized, scalefactor=1.0, size=(227, 227),
                                 mean=(78, 87, 114), swapRB=False, crop=False)

    # Predict age group
    try:
        net.setInput(blob)
        age_preds = net.forward()  # Get predictions from the model
        predicted_age_group = AGE_LIST[np.argmax(age_preds)]  # Find the age group with the highest score
        return predicted_age_group
    except Exception as e:
        raise ValueError(f"Error during model inference: {e}")

def handle_uploaded_image(uploaded_file):
    """
    Save an uploaded file to a temporary location and return the file path.
    Args:
        uploaded_file (InMemoryUploadedFile): Uploaded file object.
    Returns:
        str: Path to the temporary saved file.
    """
    temp_file = NamedTemporaryFile(delete=False, suffix=".jpg")
    temp_file.write(uploaded_file.read())
    temp_file.close()
    return temp_file.name

def get_exercise_and_food_recommendations(age_group, height, weight):
    """
    Get exercise and food recommendations based on the predicted age group and BMI.
    Args:
        age_group (str): The predicted age group (e.g., '(25-32)', '(60-100)', etc.).
        height (float): Height in centimeters.
        weight (float): Weight in kilograms.
    Returns:
        dict: Recommendations for exercise, food, and associated images.
    """
    bmi = weight / ((height / 100) ** 2)  # Calculate BMI

    # Initialize recommendations
    recommendations = {
        'exercise_image': '',
        'food_image': '',
        'exercise': '',
        'food': ''
    }

    # Age-based exercise and food recommendations
    # Age-based exercise and food recommendations
    if age_group in ['(0-2)', '(4-6)']:
        recommendations['exercise'] = 'Play-based exercises'
        recommendations['food'] = 'Nutritious baby food'
        recommendations['exercise_images'] = ['/static/images/play_exercise1.avif', '/static/images/play_exercise2.avif']  # Multiple exercise images
        recommendations['food_images'] = ['/static/images/baby_food.jpg', '/static/images/baby_food2.avif']  # Multiple food images

    elif age_group in ['(15-20)', '(25-32)']:
        recommendations['exercise'] = 'Cardio and strength training'
        recommendations['food'] = 'High-protein diet'
        recommendations['exercise_images'] = ['/static/images/cardio.jpg', '/static/images/cardio2.jpg']  # Multiple exercise images
        recommendations['food_images'] = ['/static/images/high_protein.jpg', '/static/images/high_protein2.webp']  # Multiple food images

    elif age_group in ['(38-43)', '(48-53)']:
        recommendations['exercise'] = 'Low-impact exercises'
        recommendations['food'] = 'Fiber-rich foods'
        recommendations['exercise_images'] = ['/static/images/low_impact.webp', '/static/images/low_impact2.jpg']  # Multiple exercise images
        recommendations['food_images'] = ['/static/images/fiber_rich.jpg', '/static/images/fiber_rich2.webp']  # Multiple food images

    elif age_group in ['(60-100)']:
        recommendations['exercise'] = 'Low-impact exercises'
        recommendations['food'] = 'Fiber-rich foods'
        recommendations['exercise_images'] = ['/static/images/low_impact.webp', '/static/images/low_impact2.jpg']  # Multiple exercise images
        recommendations['food_images'] = ['/static/images/fiber_rich.jpg', '/static/images/fiber_rich2.webp']  # Multiple food images

    # BMI-based adjustments to exercise and food
    if bmi > 25:
        recommendations['exercise'] += ' (Focus on weight loss)'
        recommendations['food'] += ' (Low-calorie diet)'
    elif bmi < 18.5:
        recommendations['exercise'] += ' (Focus on muscle gain)'
        recommendations['food'] += ' (High-calorie diet)'

    return recommendations
