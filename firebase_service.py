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


def get_all_posts():
    return [doc.to_dict() for doc in post_ref.stream()]


def get_post(post_id):
    post = post_ref.document(post_id).get()
    return post.to_dict()


def get_post_by_date(dt):
    dt_str = dt.strftime("%d/%m/%Y %H:%M:%S")
    posts = get_all_posts()
    for post in posts:
        if post['datetime'] == dt_str:
            return post


def update_post(post_id, subject, message, img_link, dt):
    post_doc = post_ref.document(post_id)
    dt_str = dt.strftime("%d/%m/%Y %H:%M:%S")

    post_doc.update({
        'subject': subject,
        'message': message,
        'datetime': dt_str,
        'img_link': img_link
    })


def update_user_password(user_id, pwd):
    user_doc = user_ref.document(user_id)

    user_doc.update({
        'password': pwd
    })


def get_all_posts_by_user(user_id):
    query = post_ref.where('user_id', '==', user_id)
    return [doc.to_dict() for doc in query.stream()]


def get_posts_by_date(limit):
    """
    Sort posts in descending order of date to get posts.
    https://firebase.google.com/docs/firestore/query-data/order-limit-data
    :param limit: number of posts
    :return: list of posts
    """
    query = post_ref.order_by('datetime', direction=firestore.Query.DESCENDING).limit(limit)
    return [doc.to_dict() for doc in query.stream()]


def create_user(user_id, username, password):
    user = {
        'id': user_id,
        'password': password,
        'user_name': username
    }
    user_ref.document(user_id).set(user)


def create_post(user_id, subject, message, dt, post_img_link, user_img_link):
    # https://www.programiz.com/python-programming/datetime/current-datetime
    dt_str = dt.strftime("%d/%m/%Y %H:%M:%S")
    user = get_user(user_id)
    username = user['user_name']
    post_id = user_id + dt.isoformat("#", "seconds")
    post = {
        'post_id': post_id,
        'user_id': user_id,
        'subject': subject,
        'message': message,
        'datetime': dt_str,
        'user_name': username,
        'img_link': post_img_link,
        'user_img_link': user_img_link
    }

    # one user can only submit one post at a given time
    # using isoformat as firestore keys cannot contain '/' : https://firebase.google.com/docs/firestore/quotas#collections_documents_and_fields
    print("Creating post : "+ post_id)
    post_ref.document(post_id).set(post)
