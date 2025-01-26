from google.cloud import firestore
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID
from uuid import uuid4

# TODO: wishlist can be part of the user table that I haven't created
class WishlistModel(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    timestamp: datetime = Field(default_factory=datetime.now)
    username: str
    search_term: str
    
    @classmethod
    def bq_schema(cls):
        bq_schema = [
            {"name": "id", "type": "STRING", "mode": "REQUIRED"},
            {"name": "timestamp", "type": "TIMESTAMP", "mode": "REQUIRED"},
            {"name": "username", "type": "STRING", "mode": "REQUIRED"},
            {"name": "search_term", "type": "STRING", "mode": "REQUIRED"},
        ]
        return bq_schema

    @classmethod
    def get_item(cls, username: str, search_term: str):
        return cls(
            username=username,
            search_term=search_term
        )
    
    def to_dict(self):
        data_dict = self.dict()  # Get the model's dictionary representation
        # Convert UUID fields to strings and datetime to ISO format
        data_dict['id'] = str(self.id)
        data_dict['timestamp'] = self.timestamp.isoformat()
        return data_dict

class WishList:
    def __init__(self):
        # self.db = firestore.Client()
        self.db = firestore.Client.from_service_account_json("firestore-key.json")
        self.collection = 'wishlist'

    def get_wishlist(self, username: str):
        collection_ref = self.db.collection(self.collection)
        query = collection_ref.where('username', '==', username)
        # Execute the query and fetch results
        results = query.stream()
        # Process the documents
        wishlist = []
        for doc in results:
            item = {
                'doc_id': doc.id,
                'search_term': doc.to_dict()["search_term"]
            }
            wishlist.append(item)
        return wishlist

    def insert_item(self, username: str, search_term: str):
        instance = WishlistModel.get_item(username=username, search_term=search_term)
        item_dict = instance.to_dict()

        doc_ref = self.db.collection(self.collection).document(item_dict['id'])
        doc_ref.set(item_dict)
        print(f"Document {item_dict} in collection '{self.collection}' created.")
    
    def remove_item(self, doc_id):
        doc_ref = self.db.collection(self.collection).document(doc_id)
        doc_ref.delete()