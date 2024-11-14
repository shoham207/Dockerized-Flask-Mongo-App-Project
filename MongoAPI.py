from pymongo import MongoClient
import logging as log

class MongoAPI:
    def __init__(self, data):
        log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s:\n%(message)s\n')
        self.client = MongoClient("mongodb://localhost:5000/")

        # Explicitly get database and collection names from data
        database_name = data.get('database')
        collection_name = data.get('collection')

        cursor = self.client[database_name]
        self.collection = cursor[collection_name]
        self.data = data

    def read(self):
        log.info('Reading All Data')
        try:
            documents = self.collection.find()
            return [{item: data[item] for item in data if item != '_id'}
                      for data in documents]

        except Exception as e:
            print(f"Error reading documents: {e}")
            return []

    def write(self, data):
        log.info('Writing Data')
        new_document = data.get('Document', data)
        response = self.collection.insert_one(new_document)
        return {'Status': 'Successfully Inserted',
                  'Document_ID': str(response.inserted_id)}

    def update(self):
        log.info('Updating Data')
        filt = self.data['Filter']
        updated_data = {"$set": self.data['DataToBeUpdated']}
        response = self.collection.update_one(filt, updated_data)
        output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
        return output

    def delete(self, data):
        log.info('Deleting Data')
        delete = data['Delete']
        response = self.collection.delete_one(delete)
        output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
        return output

