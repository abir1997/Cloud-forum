from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app

'''
Relevant doc : https://cloud.google.com/community/tutorials/building-flask-api-with-cloud-firestore-and-deploying-to-cloud-run
'''

# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
user_ref = db.collection('users')


def get_user(user_id):
    if user_id:
        user = user_ref.document(user_id).get()
        return user.to_dict()


def get_all_users():
    all_users = [doc.to_dict() for doc in user_ref.stream()]
    return all_users
