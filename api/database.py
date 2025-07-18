"""
Firebase Firestore database initialization and client setup for Django.
"""

import os

import firebase_admin
from django.conf import settings
from firebase_admin import credentials, firestore

# Global Firestore client
db = None


def initialize_firebase():
    """
    Initialize Firebase Admin SDK and Firestore client.
    This should be called once during Django application startup.
    """
    global db

    if firebase_admin._apps:
        # Firebase already initialized
        db = firestore.client()
        return db

    # Get Firebase configuration from Django settings
    cred_path = settings.FIREBASE_CRED_PATH
    project_id = settings.FIREBASE_PROJECT_ID

    if not cred_path or not project_id:
        raise ValueError("Firebase credentials not properly configured in Django settings")

    # Initialize Firebase with service account credentials
    if os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
    else:
        raise FileNotFoundError(f"Firebase service account file not found: {cred_path}")

    firebase_admin.initialize_app(cred, {
        'projectId': project_id
    })

    # Initialize Firestore client
    db = firestore.client()
    return db


def get_firestore_client():
    """
    Get the Firestore client instance.
    Returns the global db client, initializing if necessary.
    """
    global db
    if db is None:
        db = initialize_firebase()
    return db


# Collection references
def get_calls_collection():
    """Get reference to calls collection."""
    return get_firestore_client().collection('calls')


def get_users_collection():
    """Get reference to users collection."""
    return get_firestore_client().collection('users')


def get_messages_collection():
    """Get reference to messages collection."""
    return get_firestore_client().collection('messages')


def get_logs_collection():
    """Get reference to logs collection."""
    return get_firestore_client().collection('logs')
