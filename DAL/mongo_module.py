from typing import Dict, List, Optional, Any
from pymongo import MongoClient
from datetime import datetime
import logging as log
from bson.objectid import ObjectId
from PIL import Image


class MongoModule:
    def __init__(self, data: Dict[str, str], connection_string: str) -> None:
        """
        Initialize MongoDB service for meme management.

        Args:
            data: Dictionary containing database and collection names
            connection_string: MongoDB connection string
        """
        log.basicConfig(level=log.DEBUG, format='%(asctime)s %(levelname)s:\n%(message)s\n')
        self.client = MongoClient(connection_string)

        database_name = data.get('database')
        self.db = self.client[database_name]

        # Create separate collections for memes and images
        self.memes_collection = self.db['memes']
        self.images_collection = self.db['images']

    def save_meme(self, image_binary: bytes) -> dict:
        """
        Save meme binary data with creation timestamp.

        Args:
            image_binary: Binary data of the generated meme

        Returns:
            dict: Contains status and meme_id
        """
        log.info('Saving new meme')
        try:
            meme_document = {
                'binary_data': image_binary,
                'created_at': datetime.now()
            }

            meme_result = self.memes_collection.insert_one(meme_document)
            meme_id = str(meme_result.inserted_id)

            return {
                'status': 'Successfully Inserted',
                'meme_id': meme_id
            }

        except Exception as e:
            log.error(f"Error saving meme: {e}")
            raise

    def get_all_memes(self, include_images: bool = False) -> List[Dict[str, Any]]:
        """
        Retrieve all memes with optional image data.

        Args:
            include_images: Whether to include image binary data
        """
        log.info('Retrieving all memes')
        try:
            memes = list(self.memes_collection.find())

            for meme in memes:
                meme['_id'] = str(meme['_id'])

                if include_images:
                    image = self.images_collection.find_one({'meme_id': meme['_id']})
                    if image:
                        meme['image_data'] = image['binary_data']

            return memes

        except Exception as e:
            log.error(f"Error retrieving memes: {e}")
            return []

    def get_meme(self, meme_id: str, include_image: bool = False) -> Optional[Dict[str, Any]]:
        """
        Retrieve a specific meme by ID.

        Args:
            meme_id: ID of the meme to retrieve
            include_image: Whether to include image binary data
        """
        log.info(f'Retrieving meme {meme_id}')
        try:
            meme = self.memes_collection.find_one({'_id': ObjectId(meme_id)})

            if meme:
                meme['_id'] = str(meme['_id'])

                if include_image:
                    image = self.images_collection.find_one({'meme_id': meme_id})
                    if image:
                        meme['image_data'] = image['binary_data']

                return meme

            return None

        except Exception as e:
            log.error(f"Error retrieving meme: {e}")
            return None

    def delete_meme(self, meme_id: str) -> Dict[str, str]:
        """
        Delete a meme and its associated image.

        Args:
            meme_id: ID of the meme to delete
        """
        log.info(f'Deleting meme {meme_id}')
        try:
            # Delete meme data
            meme_result = self.memes_collection.delete_one({'_id': ObjectId(meme_id)})

            # Delete associated image if it exists
            image_result = self.images_collection.delete_one({'meme_id': meme_id})

            return {
                'status': 'Successfully Deleted' if meme_result.deleted_count > 0 else 'Meme not found',
                'deleted_image': bool(image_result.deleted_count)
            }

        except Exception as e:
            log.error(f"Error deleting meme: {e}")
            raise

    def update_meme(self, meme_id: str, update_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Update meme information.

        Args:
            meme_id: ID of the meme to update
            update_data: New data to apply to the meme
        """
        log.info(f'Updating meme {meme_id}')
        try:
            update_result = self.memes_collection.update_one(
                {'_id': ObjectId(meme_id)},
                {'$set': update_data}
            )

            return {
                'status': 'Successfully Updated' if update_result.modified_count > 0 else 'No changes made'
            }

        except Exception as e:
            log.error(f"Error updating meme: {e}")
            raise