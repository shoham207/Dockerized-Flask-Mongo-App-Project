from pymongo import MongoClient
import logging as log

class MongoAPI:
    def __init__(self, data):
        log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s:\n%(message)s\n')
        try:
            self.client = MongoClient("mongodb://localhost:5000/")

            database = data['database']
            collection = data['collection']
            cursor = self.client[database]
            self.collection = cursor[collection]
            self.data = data

        except Exception as e:
            print(f"Error connecting to MongoDB: {e}")

    def read(self):
        log.info('Reading All Data')
        try:
            documents = self.collection.find()
            # Print raw documents for debugging
            print("Raw documents:", list(documents))

            output = [{item: data[item] for item in data if item != '_id'}
                      for data in self.collection.find()]
            return output
        except Exception as e:
            print(f"Error reading documents: {e}")
            return []

    def write(self, data):
        log.info('Writing Data')
        new_document = data['Document']
        response = self.collection.insert_one(new_document)
        output = {'Status': 'Successfully Inserted',
                  'Document_ID': str(response.inserted_id)}
        return output

    def update(self):
        log.info('Updating Data')
        filt = self.data['Filter']
        updated_data = {"$set": self.data['DataToBeUpdated']}
        response = self.collection.update_one(filt, updated_data)
        output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
        return output

    def delete(self, data):
        log.info('Deleting Data')
        filt = data['Document']
        response = self.collection.delete_one(filt)
        output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
        return output

