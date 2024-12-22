from datetime import datetime, timezone
from utils.mongo_utils import fetch_inputs_from_mongo
from utils.s3_utils import save_json_to_s3
from utils.image_utils import process_images
from utils.similarity_utils import compute_similarity_report

def main():
    # Ensure bucket name is correct
    bucket_name = "ai-inzint-tracker"
    print(f"Using bucket name: {bucket_name}")  # Debugging

    current_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    users_data = fetch_inputs_from_mongo(current_date)

    for user_data in users_data:
        user_id = user_data.get("userID", "unknown_user")
        date = user_data.get("date", "unknown_date")
        screenshot_array = user_data.get("s3Urls", [])

        if not screenshot_array:
            print(f"No screenshots for User ID: {user_id}, Date: {date}")
            continue

        # Directly use the list of URLs
        image_paths = screenshot_array

        # Process images and compute report
        processed_data = process_images(image_paths)
        print("data processing done")
        report = compute_similarity_report(processed_data)
        print("report computed")

        # Save the report to S3
        output_key = f"reports/{user_id}/{date}/report.json"
        save_json_to_s3(report, bucket_name, output_key)
        print(f"Report saved for User {user_id} at {output_key}")

if __name__ == "__main__":
    main()
