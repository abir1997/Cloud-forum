from google.cloud import storage
from oauth2client.service_account import ServiceAccountCredentials


credentials = ServiceAccountCredentials.from_json_keyfile_name('service-key.json')
bucket_name = "flaskforum_bucket"


def upload(file, user_id):
    client = storage.Client.from_service_account_json("service-key.json")
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(user_id + ".png")
    blob.upload_from_file(file)
