import pymongo

# Replace with your MongoDB connection string
mongo_url = "mongodb://borobo1625:wxLvRG2iMty7l8wp@cluster0.41tusdj.mongodb.net:27017/?retryWrites=true&w=majority"

# Connect to MongoDB
try:
    client = pymongo.MongoClient(mongo_url)
    db = client.get_database("borobo1625")  # Replace with your database name
    collection = db.get_collection("borobo1625")  # Replace with your collection name

    # Test connection
    print("Connected to MongoDB")
except pymongo.errors.ConnectionFailure as e:
    print(f"Error connecting to MongoDB: {e}")
