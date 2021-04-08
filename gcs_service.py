"""
Relevant docs:
https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
https://stackoverflow.com/questions/45645717/unable-to-authenticate-google-cloud-storage-client-in-python
https://stackoverflow.com/questions/37003862/how-to-upload-a-file-to-google-cloud-storage-on-python-3
"""

from google.cloud import storage

bucket_name = "flaskforum_bucket"
client = storage.Client.from_service_account_json("service-key.json")
bucket = client.get_bucket(bucket_name)


def upload(file, file_name):
    blob = bucket.blob(file_name + ".png")
    blob.upload_from_file(file)
    blob.make_public()


def get_img_link(file_name):
    """
    Gets the public url for file.
    Returns a default user image if user does not upload an image
    :param file_name: Name of the file
    :return: url string
    """
    blob = bucket.get_blob(file_name + ".png")
    if blob is None:
        default_img_url = "https://storage.googleapis.com/flaskforum_bucket/default.png"
        return default_img_url
    return blob.public_url
