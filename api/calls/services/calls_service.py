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


def update_call_response_status(call_id: str, did_respond: bool):
    """
    Update the did_respond field for a specific call by ID.
    """
    calls_collection = get_calls_collection()
    doc_ref = calls_collection.document(call_id)
    doc_ref.update({'did_respond': did_respond})
    return {'id': call_id, 'did_respond': did_respond} 