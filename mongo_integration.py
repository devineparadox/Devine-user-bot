import pymongo

# MongoDB connection URL
mongo_url = "mongodb+srv://borobo1625:wxLvRG2iMty7l8wp@cluster0.41tusdj.mongodb.net/?retryWrites=true&w=majority"

# Connect to MongoDB
client = pymongo.MongoClient(mongo_url)
db = client.get_database()  # You can specify the database name if needed
collection = db["mycollection"]  # Replace "mycollection" with your collection name

# Example: Insert a document
data = {"username": "johndoe", "email": "johndoe@example.com"}
collection.insert_one(data)

# Example: Query documents
result = collection.find_one({"username": "johndoe"})
print(result)
