import datetime
from google.cloud import storage
from oauth2client.service_account import ServiceAccountCredentials


credentials = ServiceAccountCredentials.from_json_keyfile_name('service-key.json')
bucket_name = 
def upload(file):
    client = storage.Client(credentials=credentials, project='flask-forum')
    bucket = client.get_bucket('')
