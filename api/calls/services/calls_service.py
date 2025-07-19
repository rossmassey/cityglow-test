import json
from api.database import get_calls_collection


def get_all_calls():
    """
    Fetch all calls from Firebase Firestore.
    Returns a list of call documents as dictionaries.
    """
    calls_collection = get_calls_collection()
    docs = calls_collection.stream()
    
    calls_list = []
    for doc in docs:
        call_data = doc.to_dict()
        call_data['id'] = doc.id  # Include document ID
        calls_list.append(call_data)
    
    return calls_list 