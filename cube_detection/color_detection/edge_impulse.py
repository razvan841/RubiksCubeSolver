import cv2
import numpy as np
import os
import json
import requests
from PIL import Image
import io
from dotenv import load_dotenv


load_dotenv()

MODEL_ID = int(os.getenv('MODEL_ID'))
API_KEY = os.getenv('API_KEY')

DEBUGGING = True

ENDPOINT = f'https://studio.edgeimpulse.com/v1/api/{MODEL_ID}/classify/image'


def get_prediction(image_bgr):
    """
    Send the raw BGR image (no preprocessing) to Edge Impulse and get the prediction.
    image_bgr: np.array, shape (H, W, 3) in BGR format from OpenCV
    """
    # Convert BGR to RGB
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

    # Convert the numpy array image to bytes (PNG format)
    img_byte_array = io.BytesIO()
    # Ensure image is uint8
    if image_rgb.dtype != np.uint8:
        image_rgb = image_rgb.astype(np.uint8)

    pil_img = Image.fromarray(image_rgb)
    pil_img.save(img_byte_array, format="PNG")
    img_byte_array = img_byte_array.getvalue()

    headers = {
        'x-api-key': API_KEY
    }
    files = {'image': ('image.png', img_byte_array, 'image/png')}
    response = requests.post(ENDPOINT, headers=headers, files=files)

    # Check for success
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            # 'result' typically is a dict of label -> probability
            predictions = result['result']
            if isinstance(predictions, dict):
                predicted_label = max(predictions, key=predictions.get)
                return predicted_label, predictions[predicted_label]
            else:
                print("Unexpected response structure from Edge Impulse:", predictions)
                return None
        else:
            print(f"Error from EI response: {result.get('error')}")
            return None
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None


def load_test_labels(label_file):
    with open(label_file, 'r') as f:
        labels = {}
        for line in f:
            image_name, label_str = line.strip().split(":")
            labels[image_name.strip()] = json.loads(label_str.strip())
    return labels


def extract_patches(image):

    height, width, _ = image.shape
    square_height = height // 3
    square_width = width // 3
    patches = []
    for row in range(3):
        for col in range(3):
            y_start = row * square_height
            y_end = (row + 1) * square_height
            x_start = col * square_width
            x_end = (col + 1) * square_width
            patch = image[y_start:y_end, x_start:x_end]
            patches.append(patch)
    return patches


def color_to_index(color):
    color_to_index = {
        'blue': 0,
        'orange': 1,
        'green': 2,
        'red': 3,
        'yellow': 4,
        'white': 5
    }
    return color_to_index.get(color, -1)  # Return -1 if unknown color


def process_test_data(test_data_dir, test_labels_file):
    print("Loading test labels...")
    test_labels = load_test_labels(test_labels_file)

    print("Processing test images...")
    correct = 0
    total = 0

    for file_name in os.listdir(test_data_dir):
        if file_name.endswith(".jpg"):
            file_path = os.path.join(test_data_dir, file_name)

            test_image = cv2.imread(file_path)

            test_patches = extract_patches(test_image)

            predicted_colors = []

            for i, patch in enumerate(test_patches):
                prediction = get_prediction(patch)
                if prediction:
                    predicted_color = prediction[0]
                    predicted_index = color_to_index(predicted_color)
                    predicted_colors.append(predicted_index)
                    print(f"Patch {i+1}: Predicted: {predicted_color}")
                else:
                    predicted_colors.append(-1)

            true_colors = test_labels.get(file_name)

            if true_colors:
                total += 9
                for i, (pred, true_label) in enumerate(zip(predicted_colors, true_colors)):
                    if pred == true_label:
                        correct += 1
                    else:
                        if DEBUGGING:
                            print(f"[DEBUG] Incorrect prediction in file: {file_name}, Patch: {i}")
                            print(f"   Predicted: {pred}, True: {true_label}")

    accuracy = (correct / total) * 100 if total > 0 else 0
    print(f"Accuracy: {accuracy:.2f}%")


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    test_images_dir = os.path.join(script_dir, "test_data")
    test_labels_file = os.path.join(test_images_dir, "test_labels.txt")
    process_test_data(test_images_dir, test_labels_file)


if __name__ == "__main__":
    main()