from pymongo import MongoClient
# from django.conf import settings

# MongoDB Configuration
MONGODB_URI = 'mongodb://localhost:27017/'  # Replace with your MongoDB URI
MONGODB_NAME = 'your_database_name'         # Replace with your database name


# MongoDB connection setup
client = MongoClient(MONGODB_URI)
db = client[MONGODB_NAME]
