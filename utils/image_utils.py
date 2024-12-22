import easyocr
from PIL import Image
from io import BytesIO
from sentence_transformers import SentenceTransformer
import boto3
from urllib.parse import urlparse
import numpy as np


reader = easyocr.Reader(['en'], gpu=False)
model = SentenceTransformer('all-MiniLM-L6-v2')
s3_client = boto3.client('s3')



def load_image_from_s3(s3_path):
    """Loads an image from an S3 path or URL."""
    if s3_path.startswith("https://"):
        # Parse the S3 HTTP URL
        parsed_url = urlparse(s3_path)
        bucket = parsed_url.netloc.split(".")[0]  # Extract the bucket name
        key = parsed_url.path.lstrip("/")        # Extract the key
    elif s3_path.startswith("s3://"):
        # Handle the s3:// format
        s3_path = s3_path[len("s3://"):]
        bucket, key = s3_path.split("/", 1)
    else:
        raise ValueError(f"Invalid S3 path: {s3_path}")
    
    # Fetch the image from S3
    response = s3_client.get_object(Bucket=bucket, Key=key)
    return Image.open(BytesIO(response['Body'].read()))

def extract_text_from_image(image):
    """Extracts text from an image using EasyOCR."""
    # Convert the PIL Image object to a NumPy array
    image_np = np.array(image)
    # Use EasyOCR to extract text
    result = reader.readtext(image_np)
    return " ".join([text[1] for text in result])

def process_images(image_paths):
    """Processes a list of image paths, extracting text and generating embeddings."""
    processed_data = {}
    for path in image_paths:
        image = load_image_from_s3(path)
        text = extract_text_from_image(image)
        embedding = model.encode([text])[0]
        processed_data[path] = {"text": text, "embedding": embedding}
    return processed_data
