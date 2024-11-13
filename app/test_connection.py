from pymongo import MongoClient
import os
from dotenv import load_dotenv

def test_mongodb_connection():
    load_dotenv()
    
    # Get connection string from .env
    connection_string = os.getenv('MONGODB_CONNECTION_STRING')
    
    try:
        # Try to connect
        client = MongoClient(connection_string)
        
        # Ping the server
        client.admin.command('ping')
        
        print("✅ Successfully connected to MongoDB!")
        
        # Optional: List all databases
        print("\nAvailable databases:")
        for db in client.list_database_names():
            print(f"- {db}")
            
    except Exception as e:
        print("❌ Connection failed!")
        print(f"Error: {str(e)}")
    finally:
        # Close the connection
        if 'client' in locals():
            client.close()

if __name__ == "__main__":
    test_mongodb_connection() 