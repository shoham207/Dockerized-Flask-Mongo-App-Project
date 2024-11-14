from flask import Flask, request, json, Response
from pymongo import MongoClient

from MongoAPI import MongoAPI

if __name__ == "__main__":
    app = Flask(__name__)
    app.run(debug=True, port=5001, host='0.0.0.0')
    data = {
        'database': 'posts',
        'collection': 'users'
    }

    mongo_api = MongoAPI(data)

    # Insert a test document
    test_data = {
        'Document': {
            'name': 'Test User',
            'email': 'test@example.com'
        }
    }
    print("\nInserting test document...")
    mongo_api.write(test_data)

    # Read and print all documents
    print("\nReading all documents...")
    result = mongo_api.read()
    print("Documents found:", json.dumps(result, indent=4))