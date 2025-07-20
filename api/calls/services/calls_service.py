import logging

from api.database import get_calls_collection

logger = logging.getLogger(__name__)


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
    logger.info(f"Marking {call_id} with did_respond: {did_respond}")

    calls_collection = get_calls_collection()
    doc_ref = calls_collection.document(call_id)

    # First check if the document exists
    doc = doc_ref.get()
    if not doc.exists:
        logger.error(f"Document with ID {call_id} does not exist")
        raise ValueError(f"Call with ID {call_id} not found")

    try:
        doc_ref.update({'did_respond': did_respond})
        return {'id': call_id, 'did_respond': did_respond}

    except Exception as e:
        logger.error(f"Error updating call {call_id}: {str(e)}")
        raise
