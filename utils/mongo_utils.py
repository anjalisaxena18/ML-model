from pymongo import MongoClient

def fetch_inputs_from_mongo(date):
    """Fetches user data for the specified date."""
    mongo_client = MongoClient("mongodb+srv://anjali:tzfE7LYesmNXRKyf@ai-inzint-tracker.v9ifm.mongodb.net/?retryWrites=true&w=majority&appName=ai-inzint-tracker")
    db = mongo_client["screenshot_metadata"]
    collection = db["screenshots"]

    query = {"date": date}
    data = list(collection.find(query))
    print("Fetched Data:", data)  # Debugging
    return data
