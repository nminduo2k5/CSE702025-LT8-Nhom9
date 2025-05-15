import cv2
import sys
import os
from datetime import datetime

# Load the image from file
image_path = r'C:\Users\duong\OneDrive_duong\Desktop\Thi_giac_mt\Thi_giac_mt\trai\DSCPDC_0001_BURST20250227135749337_COVER.JPG'  # Replace with your image path

# Create a new output directory with a timestamp
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
image_output = f"./output1_{timestamp}"

if not os.path.exists(image_output):
    os.makedirs(image_output)

image = cv2.imread(image_path)

# Load the pre-trained Haar Cascade model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Convert image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detect faces with optimized parameters
faces = face_cascade.detectMultiScale(
    gray_image,
    scaleFactor=1.05,  # Scale factor
    minNeighbors=3,    # Minimum number of neighbors
    minSize=(20, 20)   # Minimum size of faces
)

# Iterate over detected faces and crop them
for i, (x, y, w, h) in enumerate(faces):
    # Crop the face
    face_image = image[y:y+h, x:x+w]
    # Save or process the cropped face
    cv2.imwrite(os.path.join(image_output, f'face_{i}.jpg'), face_image)

# Display the cropped faces
import matplotlib.pyplot as plt

for i, (x, y, w, h) in enumerate(faces):
    # Crop the face
    face_image = image[y:y+h, x:x+w]
    # Convert from BGR to RGB
    face_image_rgb = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
    # Display the cropped face
    plt.figure(figsize=(6, 6))
    plt.imshow(face_image_rgb)
    plt.title(f'Face {i}')
    plt.axis('off')  # Hide the axis
    plt.show()
