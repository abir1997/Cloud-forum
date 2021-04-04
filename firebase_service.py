from flask import Flask, request, jsonify
from firebase_admin import credentials, firestore, initialize_app

'''
Relevant docs : 
https://cloud.google.com/community/tutorials/building-flask-api-with-cloud-firestore-and-deploying-to-cloud-run
https://firebase.google.com/docs/firestore/manage-data/add-data#python
'''

# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
user_ref = db.collection('users')
post_ref = db.collection('posts')


def get_user(user_id):
    if user_id:
        user = user_ref.document(user_id).get()
        return user.to_dict()


def get_all_users():
    all_users = [doc.to_dict() for doc in user_ref.stream()]
    return all_users


def create_user(user_id, username, password):
    user = {
        'id': user_id,
        'password': password,
        'user_name': username
    }
    user_ref.document(user_id).set(user)


def create_post(user_id, subject, message, dt):
    # https://www.programiz.com/python-programming/datetime/current-datetime
    dt_str = dt.strftime("%d/%m/%Y %H:%M:%S")
    print(dt_str)
    post = {
        'subject': subject,
        'message': message,
        'datetime': dt_str
    }

    # one user can only submit one post at a given time
    # using isoformat as firestore keys cannot contain '/'
    post_id = user_id + dt.isoformat()
    print(post_id)
    post_ref.document(post_id).set(post)
