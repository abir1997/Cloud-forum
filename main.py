from flask import Flask, render_template, request, make_response, flash, jsonify, url_for
from datetime import datetime
from werkzeug.utils import redirect
import firebase_service as fbs
import gcs_service as gcs_s

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('home.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['userId'] and request.form['password']:
            user_id = request.form['userId']
            pwd = request.form['password']
            user = fbs.get_user(user_id)
            if is_valid_login(user_id, pwd):
                print("Authorization successful, routing to forum..")
                # cookie docs : https://pythonbasics.org/flask-cookies/
                resp = make_response(redirect("/forum"))
                resp.set_cookie('logged_in_user', user_id)
                resp.set_cookie('username', user['user_name'])
                img_link = gcs_s.get_img_link(user_id)
                resp.set_cookie('img_link', img_link)
                return resp
            else:
                print("Authorization unsuccessful.")
                error = "ID or password is invalid"

    return render_template('login.html', message=error)


def is_valid_login(user_id, password):
    users = fbs.get_all_users()
    # user = fbs.get_user(user_id)
    for user in users:
        if user['id'] == user_id and user['password'] == password:
            return True
    return False


@app.route("/register", methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        user_id = request.form['userId']
        pwd = request.form['password']
        username = request.form['userName']

        users = fbs.get_all_users()
        if id_exists(users, user_id):
            error = "The ID already exists."
        elif username_exists(users, username):
            error = "The username already exists"
        else:
            print("Registration successful. Creating record in firestore.")
            fbs.create_user(user_id, username, pwd)
            if request.files['img']:
                file = request.files['img']
                gcs_s.upload(file, user_id)
            return make_response(redirect("/login"))

    return render_template('register.html', message=error)


def is_valid_registration(user_id, username):
    users = fbs.get_all_users()
    for user in users:
        if user['id'] == user_id or user['user_name'] == username:
            return False
    return True


def id_exists(users, user_id):
    for user in users:
        if user['id'] == user_id:
            return True
    return False


def username_exists(users, username):
    for user in users:
        if user['user_name'] == username:
            return False


@app.route("/forum", methods=["GET", "POST"])
def forum():
    if request.method == 'POST':
        if request.form['subject'] is None:
            return render_template("forum.html", username=request.cookies.get("username"),
                                   img_link=request.cookies.get("img_link"), err="Subject is required")
        subject = request.form['subject']
        msg = request.form['message']
        msg_img = request.files['msg_img']
        dt = datetime.now()
        user_id = request.cookies.get("logged_in_user")
        img_link = ""
        if msg_img:
            img_file_name = user_id + dt.isoformat()
            gcs_s.upload(msg_img, img_file_name)
            img_link = gcs_s.get_img_link(img_file_name)

        fbs.create_post(user_id, subject, msg, dt, img_link)

    recent_posts = fbs.get_posts_by_date(10)
    return render_template("forum.html", username=request.cookies.get("username"),
                           img_link=request.cookies.get("img_link"), posts=recent_posts)


@app.route("/userpage", methods=["GET", "POST"])
def user_page():
    user_id = request.cookies.get("logged_in_user")
    user_posts = fbs.get_all_posts_by_user(user_id)

    if request.method == 'POST':
        old_pwd = request.form['old_password']
        new_pwd = request.form['new_password']

        if is_valid_password(old_pwd):
            fbs.update_user_password(user_id, new_pwd)
            resp = make_response(redirect("/login"))
            return resp
        else:
            return render_template("userpage.html", posts=user_posts, err="The old password is incorrect")

    return render_template("userpage.html", posts=user_posts)


def is_valid_password(pwd):
    user_id = request.cookies.get("logged_in_user")
    user = fbs.get_user(user_id)
    return pwd == user['password']


@app.route("/editpost", methods=["GET", "POST"])
def edit_post():
    user_id = request.cookies.get("username")
    subject = request.form['subject']
    message = request.form['message']
    img_link = request.form['img_link']
    dt_str = request.form['datetime']
    dt_obj = datetime.strptime(dt_str, "%d/%m/%Y %H:%M:%S")

    if "route_to_forum" in request.form:

        new_dt = datetime.now()
        msg_img = request.files['msg_img']
        if msg_img:
            file_name = user_id + new_dt.isoformat()
            gcs_s.upload(msg_img, file_name)
            img_link = gcs_s.get_img_link(file_name)

        # update post in firestore.
        post_id = user_id + dt_obj.isoformat("#", "seconds")
        print("updating post : " + post_id)
        fbs.update_post(post_id, subject, message, img_link, datetime.now())

        recent_posts = fbs.get_posts_by_date(10)
        return render_template("forum.html", username=request.cookies.get("username"),
                               img_link=request.cookies.get("img_link"), posts=recent_posts)

    return render_template("editpost.html", subject=subject, message=message,
                           img_link=img_link, datetime=dt_str)


@app.route("/logout")
def logout():
    resp = make_response(redirect("/login"))
    resp.set_cookie('logged_in_user', '', expires=0)
    resp.set_cookie('username', '', expires=0)
    resp.set_cookie('img_link', '', expires=0)
    return resp


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
