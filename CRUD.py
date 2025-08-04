from pymongo import MongoClient
from bson.objectid import ObjectId
from pymongo.errors import PyMongoError


class AnimalShelter:
    """
    CRUD operations for Animal collection in MongoDB.
    Designed to support reusability and modularity.
    """

    def __init__(self):
        """
        Initializes the MongoDB client connection and selects the specified
        database and collection.
        """
        USER = "aacuser"
        PASS = "Universe1"
        HOST = "nv-desktop-services.apporto.com"
        PORT = 31750
        DB = "AAC"
        COL = "animals"

        uri = f"mongodb://{USER}:{PASS}@{HOST}:{PORT}/?authSource=admin"
        self.client = MongoClient(uri)
        self.database = self.client[DB]
        self.collection = self.database[COL]

    def create(self, data):
        """
        Inserts a single document into the collection.

        Args:
            data (dict): The document to insert.

        Returns:
            bool: True if insert is successful, False otherwise.
        """
        if data:
            try:
                result = self.collection.insert_one(data)
                return result.acknowledged
            except PyMongoError as e:
                print(f"Create failed: {e}")
                return False
        else:
            print("Create failed: data is empty.")
            return False

    def read(self, query):
        """
        Queries the collection for matching documents.

        Args:
            query (dict): Filter to apply.

        Returns:
            list: A list of matching documents or an empty list on failure.
        """
        try:
            if query is None:
                raise ValueError("Query cannot be None")
            results = self.collection.find(query)
            return list(results)
        except PyMongoError as e:
            print(f"Read failed: {e}")
            return []
        except ValueError as e:
            print(e)
            return []

    def update(self, query, update_data):
        """
        Updates document(s) matching the query with new values.

        Args:
            query (dict): Filter to find documents to update.
            update_data (dict): Fields to update (must include MongoDB $ operators).

        Returns:
            int: Number of documents modified.
        """
        try:
            result = self.collection.update_many(query, update_data)
            return result.modified_count
        except PyMongoError as e:
            print(f"Update failed: {e}")
            return 0

    def delete(self, query):
        """
        Deletes document(s) matching the query.

        Args:
            query (dict): Filter to select documents to delete.

        Returns:
            int: Number of documents deleted.
        """
        try:
            result = self.collection.delete_many(query)
            return result.deleted_count
        except PyMongoError as e:
            print(f"Delete failed: {e}")
            return 0