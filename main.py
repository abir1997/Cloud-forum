from flask import Flask
from firebase_admin import credentials, firestore, initialize_app

app = Flask(__name__)

# Initialize Firestore DB
cred = credentials.Certificate('key.json')
default_app = initialize_app(cred)
db = firestore.client()
user_ref = db.collection('users')

# firebaseConfig = {
#     'apiKey': "AIzaSyD_ZP5IGwlVqYNwHPfsLNfA4TEO6Y9-71w",
#     'authDomain': "flask-forum.firebaseapp.com",
#     'projectId': "flask-forum",
#     'storageBucket': "flask-forum.appspot.com",
#     'messagingSenderId': "552857994123",
#     'appId': "1:552857994123:web:e2878e400a5dd9b451e58e",
#     'measurementId': "G-12BLGVRGQ7"
# }


@app.route("/", methods=['GET'])
def welcome():
    users = [doc.to_dict() for doc in user_ref.stream()]
    for user in users:
        return user


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)