"""
Relevant docs:
https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
https://stackoverflow.com/questions/45645717/unable-to-authenticate-google-cloud-storage-client-in-python
https://stackoverflow.com/questions/37003862/how-to-upload-a-file-to-google-cloud-storage-on-python-3
"""

from google.cloud import storage
from oauth2client.service_account import ServiceAccountCredentials


credentials = ServiceAccountCredentials.from_json_keyfile_name('service-key.json')
bucket_name = "flaskforum_bucket"
client = storage.Client.from_service_account_json("service-key.json")
bucket = client.get_bucket(bucket_name)


def upload(file, user_id):
    blob = bucket.blob(user_id + ".png")
    blob.upload_from_file(file)
    blob.make_public()


def download(user_id):
    pass


def get_img_link(user_id):
    blob = bucket.get_blob(user_id + ".png")
    return blob.public_url
