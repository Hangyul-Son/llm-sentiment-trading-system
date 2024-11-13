from pymongo import MongoClient
from datetime import datetime
from typing import Dict, Any
import streamlit as st

class Database:
    def __init__(self):
        # Get MongoDB connection string from streamlit secrets
        self.connection_string = st.secrets["MONGODB_CONNECTION_STRING"]
        self.db_name = st.secrets["MONGODB_DATABASE_NAME"]
        
        if not self.connection_string:
            raise ValueError("MongoDB connection string not found in secrets")
        
        # Initialize MongoDB client with Azure connection
        self.client = MongoClient(self.connection_string)
        self.db = self.client[self.db_name]

    def insert_document(self, collection: str, document: Dict[str, Any]) -> str:
        """Insert a document into specified collection"""
        document['created_at'] = datetime.utcnow()
        result = self.db[collection].insert_one(document)
        return str(result.inserted_id)

    def find_documents(self, collection: str, query: Dict[str, Any]) -> list:
        """Find documents matching query in specified collection"""
        return list(self.db[collection].find(query))

    def update_document(self, collection: str, query: Dict[str, Any], update: Dict[str, Any]) -> int:
        """Update documents matching query in specified collection"""
        result = self.db[collection].update_many(query, {'$set': update})
        return result.modified_count

    def delete_documents(self, collection: str, query: Dict[str, Any]) -> int:
        """Delete documents matching query from specified collection"""
        result = self.db[collection].delete_many(query)
        return result.deleted_count

    def close_connection(self):
        """Close MongoDB connection"""
        self.client.close()
