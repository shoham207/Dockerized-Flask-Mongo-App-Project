from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import logging as log

class MongoService:
    def __init__(self, data, connection_string):
        log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s:\n%(message)s\n')
        self.client = MongoClient(connection_string)

        # Explicitly get database and collection names from data
        database_name = data.get('database')
        collection_name = data.get('collection')

        cursor = self.client[database_name]
        self.collection = cursor[collection_name]
        self.data = data

    def get_all_quotes(self):
        log.info('Reading all quotes')
        try:
            quotes = self.collection.find()
            return [{item: data[item] for item in data if item != '_id'}
                      for data in quotes]

        except Exception as e:
            print(f"Error reading documents: {e}")
            return []

    def get_quote(self, quote_id):
        log.info(f'Reading {quote_id} quote')
        try:
            quote = self.collection.find_one({'_id': ObjectId(quote_id)})
            if quote:
                quote['_id'] = str(quote['_id'])
            return quote
        except Exception as e:
            print(f"Error getting quote: {e}")
            return None

    def save_quote(self, quote_data):
        log.info('Writing quote_data')
        # Add timestamp
        quote_data['created_at'] = datetime.now()
        response = self.collection.insert_one(quote_data)
        return {'Status': 'Successfully Inserted',
                  'Quote_ID': str(response.inserted_id)}

    #def update(self):
        #log.info('Updating Data')
        #filt = self.data['Filter']
        #updated_data = {"$set": self.data['DataToBeUpdated']}
        #response = self.collection.update_one(filt, updated_data)
        #output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
        #return output

    def delete_quote(self, quote_id):
        log.info('Deleting Data')
        try:
            response = self.collection.delete_one({'_id': ObjectId(quote_id)})
            output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
            return output
        except Exception as e:
            print(f"Error deleting quote: {e}")

