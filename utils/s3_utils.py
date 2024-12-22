import json
import boto3
import numpy as np  # Import NumPy for type-checking

def convert_numpy_types(obj):
    """Recursively convert NumPy types to Python native types."""
    if isinstance(obj, np.ndarray):
        return obj.tolist()  # Convert NumPy array to list
    elif isinstance(obj, (np.float32, np.float64)):
        return float(obj)  # Convert NumPy float to Python float
    elif isinstance(obj, (np.int32, np.int64)):
        return int(obj)  # Convert NumPy int to Python int
    elif isinstance(obj, dict):
        return {k: convert_numpy_types(v) for k, v in obj.items()}  # Process dictionary
    elif isinstance(obj, list):
        return [convert_numpy_types(i) for i in obj]  # Process list
    else:
        return obj  # Return as-is for other types

def save_json_to_s3(json_data, bucket_name, output_key):
    """Save JSON data to an S3 bucket."""
    # Preprocess JSON data to ensure compatibility
    processed_data = convert_numpy_types(json_data)
    
    # Initialize S3 client
    s3 = boto3.client('s3')
    
    # Serialize the JSON data and save to S3
    s3.put_object(
        Bucket=bucket_name,
        Key=output_key,
        Body=json.dumps(processed_data, indent=4),
        ContentType='application/json'
    )
