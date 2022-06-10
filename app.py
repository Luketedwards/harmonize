import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, Response)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
import pathlib
import datetime
from datetime import datetime, timedelta, date
import boto3
import botocore
from filters import datetimeformat, datetimeformatBucket, file_type


from imagekitio import ImageKit
imagekit = ImageKit(
    private_key='private_qwuxSVAklF1V0cJcrBjfluCALVM=',
    public_key='public_pW2XXmuTn4jfQxJ4V1KESsANJYQ=',
    url_endpoint='https://ik.imagekit.io/harmonise'
)

if os.path.exists("env.py"):
    import env


app = Flask(__name__)
app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['datetimeformatBucket'] = datetimeformatBucket
app.jinja_env.filters['file_type'] = file_type


UPLOAD_FOLDER = 'static/images/user-images/'
UPLOAD_FOLDER_PROJECT = 'static/project-files/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_PROJECT'] = UPLOAD_FOLDER_PROJECT
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")
S3_BUCKET = os.environ.get("S3_BUCKET")
S3_KEY = os.environ.get("S3_KEY")
S3_SECRET = os.environ.get("S3_SECRET")

mongo = PyMongo(app)


global user

# creating global instance of amazon S3 bucket for file uploads


def _get_s3_resource():
    if S3_KEY and S3_SECRET:
        return boto3.resource(
            's3',
            aws_access_key_id=S3_KEY,
            aws_secret_access_key=S3_SECRET
        )
    else:
        return boto3.resource('s3')

# projects Amazon S3 bucket


def get_bucket():
    s3_resource = _get_s3_resource()
    return s3_resource.Bucket(S3_BUCKET)

# Login function


@app.route("/")
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(
                    request.form.get("username")))
                return redirect(url_for(
                    "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route('/files')
def files():
    s3_resource = boto3.resource('s3')
    my_bucket = s3_resource.Bucket(S3_BUCKET)
    summaries = my_bucket.objects.all()

    return render_template("files.html", my_bucket=my_bucket, files=summaries)

# registers user account, creates user object in database


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        takenUsername = mongo.db.takenUsernames.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user or takenUsername:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "fname": request.form.get("first_name"),
            "lname": request.form.get("last_name"),
            "password": generate_password_hash(
                request.form.get("password")),
            "city": request.form.get("city"),
            "email": request.form.get("email"),
            "instruments": request.form.getlist("instruments"),
            "genres": request.form.getlist("genres"),
            "bio": "Tell us a little about yourself! Click the edit profile \
                    button to write your bio",
            "profile_pic": "/static/images/default-pp-min.png",
            "profile_pic2":
            "https://ik.imagekit.io/harmonise/static/images/user-images/default-pp-min.png",
            "followers": [],
            "following": [],
            "notifications": []}

        takenUsernames = {
            "username": request.form.get("username").lower()
        }

        mongo.db.users.insert_one(register)
        mongo.db.takenUsernames.insert_one(takenUsernames)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")

# logs out user


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))

# users personal profile


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):

    listOfUsers = mongo.db.users.find()
    allCurrentUsernames = mongo.db.users.distinct("username")
    projects = mongo.db.projects.find({'username': username})
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    user = (session["user"])
    user_notifications = mongo.db.users.find_one({'username': user})
    listOfUsers = mongo.db.users.find()
    listOfProjectNames = mongo.db.projects.distinct('projectTitle')

    if session["user"]:
        user = (session["user"])
        current_user = mongo.db.users.find_one({'username': user})
        userProjects = mongo.db.projects.count_documents(
            {'username': username})
        return render_template(
            "profile.html",
            username=username,
            current_user=current_user,
            listOfUsers=listOfUsers,
            user_notifications=user_notifications,
            allCurrentUsernames=allCurrentUsernames,
            listOfProjectNames=listOfProjectNames,
            userProjects=userProjects,
            projects=projects)

    return redirect(url_for("login"))


# Renders users setting page
@app.route("/settings/<username>", methods=["GET", "POST"])
def settings(username):
    try:
        listOfUsers = mongo.db.users.find()
        allCurrentUsernames = mongo.db.users.distinct("username")
        listOfProjectNames = mongo.db.projects.distinct('projectTitle')

        # grab the session user's username from db
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        user = (session["user"])
        user_notifications = mongo.db.users.find_one({'username': user})

        if session["user"]:
            user = (session["user"])
            current_user = mongo.db.users.find_one({'username': user})

            return render_template("settings.html", username=username,
                                   current_user=current_user,
                                   user_notifications=user_notifications,
                                   allCurrentUsernames=allCurrentUsernames,
                                   listOfProjectNames=listOfProjectNames)

        return redirect(url_for("login"))
    except BaseException:
        return render_template("login.html")


# function to delete user account from database
@app.route("/delete_account", methods=["GET", "POST"])
def delete_account():

    listOfUsers = mongo.db.users.find()
    allCurrentUsernames = mongo.db.users.distinct("username")
    listOfProjectNames = mongo.db.projects.distinct('projectTitle')
    username = (session["user"])

    # Code to delete all of the files within users projects and then the
    # project itself

    projectsToDelete = mongo.db.projects.find({'username': username})

    for projectsD in projectsToDelete:
        thisProjectId = projectsD['_id']
        thisProjectTitle = projectsD['projectTitle']
        noOfFiles = mongo.db.projects.find_one(
            {'_id': ObjectId(thisProjectId)})
        noOfFiles = len(noOfFiles['projectFiles'])
        result1 = []
        result2 = []
        if noOfFiles > 0:
            for nameOfFiles in mongo.db.projects.find({'_id': ObjectId(thisProjectId)}, {
                                                      'projectFiles': {'file': True}}):
                result1.append(nameOfFiles['projectFiles'])
                for i in range(noOfFiles):
                    result2.append(nameOfFiles['projectFiles'][i]['file'])

            mongo.db.projects.delete_one({'_id': ObjectId(thisProjectId)})

            for filename in result2:
                key = str(filename)
                my_bucket = get_bucket()
                my_bucket.Object(key).delete()

        else:
            mongo.db.projects.delete_one({'_id': ObjectId(thisProjectId)})
    # Deletes users username from all following lists
    mongo.db.users.update_many(
        {"following": username},
        {'$pull': {"following": username}})
    mongo.db.users.update_many(
        {"followers": username},
        {'$pull': {"followers": username}})

    # deletes users profile photo from Amazon s3
    try:
        typeofFile = mongo.db.users.find_one(
            {'username': username})['profile_pic']
        typeofFile = typeofFile[-4:]
        key = 'static/images/user-images/profile-image-' + username + typeofFile
        my_bucket = get_bucket()
        my_bucket.Object(key).delete()

        # Deletes users account and data
        mongo.db.users.delete_one({"username": username})

        # logs out user for the last time and prompts them to register
        session.pop("user")
        flash("Account successfully deleted")
    except BaseException:
        # Deletes users account and data
        mongo.db.users.delete_one({"username": username})

        # logs out user for the last time and prompts them to register
        session.pop("user")
        flash("Account successfully deleted")

    return render_template("register.html")


# allows user to edit bio and account information
@app.route("/edit_profile/<username>", methods=["GET", "POST"])
def edit_profile(username):
    try:
        username = username
        user = (session["user"])
        current_user = mongo.db.users.find_one({'username': user})
        user_notifications = mongo.db.users.find_one({'username': user})
        listOfUsers = mongo.db.users.find()
        allCurrentUsernames = mongo.db.users.distinct("username")
        listOfProjectNames = mongo.db.projects.distinct('projectTitle')
        if request.method == "POST":
            edit = {'$set': {
                "fname": request.form.get("first_nameEdit"),
                    "lname": request.form.get("last_nameEdit"),
                    "city": request.form.get("cityEdit"),
                    "instruments": request.form.getlist("instrumentsEdit"),
                    "genres": request.form.getlist("genreEdit"),
                    "bio": request.form.get("bio")

                    }}
            user_id = mongo.db.users.find_one({'username': user})['_id']

            mongo.db.users.update_one({'_id': ObjectId(user_id)}, edit)
            flash("Profile Updated!")

            if session["user"]:
                user = (session["user"])
                current_user = mongo.db.users.find_one({'username': user})

            return redirect(url_for('profile', username=username))

        return render_template(
            "edit-profile.html",
            username=username,
            current_user=current_user,
            listOfUsers=listOfUsers,
            user_notifications=user_notifications,
            allCurrentUsernames=allCurrentUsernames,
            listOfProjectNames=listOfProjectNames)

    except BaseException:
        return render_template("login.html")


# allows user to upload and change their profile image
@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():

    listOfUsers = mongo.db.users.find()
    allCurrentUsernames = mongo.db.users.distinct("username")
    listOfProjectNames = mongo.db.projects.distinct('projectTitle')
    user = (session["user"])
    user_notifications = mongo.db.users.find_one({'username': user})
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    current_user = mongo.db.users.find_one({'username': user})
    user_id = mongo.db.users.find_one({'username': user})['_id']
    

    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file1 in form!'
        file1 = request.files['file1']

        newFileName = "profile-image" + "-" + user
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        ext = pathlib.Path(path).suffix
        newPath = os.path.join(
            app.config['UPLOAD_FOLDER'], newFileName + ext)
        newPathNoExt = os.path.join(
            app.config['UPLOAD_FOLDER'], newFileName )
    

        my_bucket = get_bucket()
        my_bucket.Object(newPath).put(Body=file1)
        
        #purges imagekit cache so new profile image is updated

        imagekit.purge_file_cache(
            'https://ik.imagekit.io/harmonise/' + newPathNoExt + '.jpg' + '*'
            )

        imagekit.purge_file_cache(
            'https://ik.imagekit.io/harmonise/' + newPathNoExt + '.png' + '*'
            )

        imagekit.purge_file_cache(
            'https://ik.imagekit.io/harmonise/' + newPathNoExt + '.jpeg' + '*'
            )

        profile_pic_update = {'$set': {
            'profile_pic':
            'https://harmonise.s3.eu-west-2.amazonaws.com/' + newPath
        }

        }

        profile_pic_update_optimsed = {'$set': {
            'profile_pic2':
            'https://ik.imagekit.io/harmonise/' + newPath
        }}
        mongo.db.users.update_one(
            {'_id': ObjectId(user_id)}, profile_pic_update)

        mongo.db.users.update_one(
            {'_id': ObjectId(user_id)}, profile_pic_update_optimsed)
        flash("Profile Picture Updated! Changes may take a minute to display")

        return redirect(url_for("profile", username=username))

    return render_template("upload_file.html", listOfUsers=listOfUsers,
                           user_notifications=user_notifications,
                           allCurrentUsernames=allCurrentUsernames,
                           listOfProjectNames=listOfProjectNames)


# renders all other users on the site
@app.route("/other_users")
def other_users():
    try:
        listOfUsers = mongo.db.users.find()
        allCurrentUsernames = mongo.db.users.distinct("username")
        listOfProjectNames = mongo.db.projects.distinct('projectTitle')
        users = mongo.db.users.find()
        user = (session["user"])
        user_notifications = mongo.db.users.find_one({'username': user})
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        current_user = mongo.db.users.find_one({'username': user})
        user_id = mongo.db.users.find_one({'username': user})['_id']

        return render_template(
            "other-users.html",
            user=user,
            username=username,
            current_user=current_user,
            user_id=user_id,
            users=users,
            listOfUsers=listOfUsers,
            user_notifications=user_notifications,
            allCurrentUsernames=allCurrentUsernames,
            listOfProjectNames=listOfProjectNames)
    except BaseException:
        return render_template("login.html")


# page to specify parameters to filter users by
@app.route("/filter_users", methods=['GET', 'POST'])
def filter_users():
    try:
        listOfUsers = mongo.db.users.find()
        allCurrentUsernames = mongo.db.users.distinct("username")
        listOfProjectNames = mongo.db.projects.distinct('projectTitle')
        user = (session["user"])
        users = mongo.db.users.find()
        user_notifications = mongo.db.users.find_one({'username': user})

        if request.method == "POST":
            cityQuery = request.form.get('city')
            if cityQuery == "":
                cityQuery = " "
            instrumentsQuery = request.form.getlist('instruments')
            genresQuery = request.form.getlist("genres")

            return render_template(
                "other-users-filter.html",
                listOfUsers=listOfUsers,
                allCurrentUsernames=allCurrentUsernames,
                listOfProjectNames=listOfProjectNames,
                user_notifications=user_notifications,
                cityQuery=cityQuery,
                instrumentsQuery=instrumentsQuery,
                genresQuery=genresQuery,
                users=users)

        return render_template('user-filter.html', listOfUsers=listOfUsers,
                               allCurrentUsernames=allCurrentUsernames,
                               listOfProjectNames=listOfProjectNames,
                               user_notifications=user_notifications)

    except BaseException:
        return render_template("login.html")


# other users profiles
@app.route('/other_profile/<usernameOther>', methods=["GET", "POST"])
def other_profile(usernameOther):
    try:
        listOfUsers = mongo.db.users.find()
        allCurrentUsernames = mongo.db.users.distinct("username")
        listOfProjectNames = mongo.db.projects.distinct('projectTitle')
        listOfProjects = mongo.db.projects.distinct("projectTitle")
        selectedUser = mongo.db.users.find_one({'username': usernameOther})
        projects = mongo.db.projects.find({'username': usernameOther})
        project_number = mongo.db.projects.count_documents(
            {'username': usernameOther})
        user = (session["user"])
        myUsername = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        projectsImIn = mongo.db.projects.find(
            {'projectMembers.memberUsername': username})
        user_notifications = mongo.db.users.find_one({'username': user})
        current_user = mongo.db.users.find_one({'username': user})
        following = mongo.db.users.find_one({'username': user}, {"following"})
        username = user
        current_user = mongo.db.users.find_one({'username': user})

        if usernameOther != user and usernameOther in allCurrentUsernames:
            return render_template(
                'other-profile.html',
                selectedUser=selectedUser,
                following=following,
                listOfUsers=listOfUsers,
                user=user,
                current_user=current_user,
                projects=projects,
                user_notifications=user_notifications,
                project_number=project_number,
                allCurrentUsernames=allCurrentUsernames,
                listOfProjectNames=listOfProjectNames,
                projectsImIn=projectsImIn,
                myUsername=myUsername)

        elif usernameOther not in allCurrentUsernames:
            flash('This profile no longer exists')
            return redirect(url_for("profile", username=username))

        return redirect(url_for("profile", username=username))
    except BaseException:
        return render_template("login.html")


# search function to find other users by username
@app.route('/other_profile_search/', methods=["GET", "POST"])
def other_profile_search():
    try:
        user = (session["user"])

        usernameOther = request.form.get("user-search-input").lower().strip()

        projects = mongo.db.projects.find({'username': usernameOther})
        project_number = mongo.db.projects.count_documents(
            {'username': usernameOther})
        listOfUsers = mongo.db.users.find()
        allCurrentUsernames = mongo.db.users.distinct("username")
        listOfProjectNames = mongo.db.projects.distinct('projectTitle')
        myUsername = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        projectsImIn = mongo.db.projects.find(
            {'projectMembers.memberUsername': username})

        selectedUser = mongo.db.users.find_one({'username': usernameOther})

        user_notifications = mongo.db.users.find_one({'username': user})

        current_user = mongo.db.users.find_one({'username': user})
        following = mongo.db.users.find_one({'username': user}, {"following"})

        if usernameOther not in allCurrentUsernames:
            flash("That user doesn't exist")
            username = username
            return render_template(
                "profile.html",
                username=username,
                current_user=current_user,
                listOfUsers=listOfUsers,
                user_notifications=user_notifications,
                allCurrentUsernames=allCurrentUsernames,
                listOfProjectNames=listOfProjectNames)

        if usernameOther != username:
            return render_template(
                'other-profile.html',
                selectedUser=selectedUser,
                following=following,
                listOfUsers=listOfUsers,
                usernameOther=usernameOther,
                user=user,
                current_user=current_user,
                projects=projects,
                user_notifications=user_notifications,
                project_number=project_number,
                allCurrentUsernames=allCurrentUsernames,
                listOfProjectNames=listOfProjectNames,
                projectsImIn=projectsImIn,
                myUsername=myUsername)

        if usernameOther == username:
            username = username
            return redirect(url_for("profile", username=username))
    except BaseException:
        return render_template("login.html")


# function to follow other users accounts and notfiy them
@app.route('/follow-user/<usernameOther>', methods=["GET", "POST"])
def follow_user(usernameOther):
    try:
        listOfUsers = mongo.db.users.distinct('username')
        allCurrentUsernames = mongo.db.users.distinct("username")
        listOfProjectNames = mongo.db.projects.distinct('projectTitle')
        selectedUser = mongo.db.users.find_one({'username': usernameOther})
        user = (session["user"])
        user_notifications = mongo.db.users.find_one({'username': user})
        current_user = mongo.db.users.find_one({'username': user})
        current_username = mongo.db.users.find_one(
            {'username': user})["username"]
        user_id = mongo.db.users.find_one({'username': user})['_id']
        following = mongo.db.users.find_one({'username': user}, {"following"})
        usernameOther = (selectedUser['username'])

        mongo.db.users.update_one({"username": usernameOther}, {
                                  '$push': {"notifications": current_username}})
        mongo.db.users.update_one(
            {"username": user}, {'$push': {"following": usernameOther}})
        mongo.db.users.update_one({"username": usernameOther}, {
                                  '$push': {"followers": user}})
        flash("You are now following " + selectedUser['username'])

        return redirect(url_for('other_profile', usernameOther=usernameOther))
    except BaseException:
        return render_template("login.html")


# if user is already followed, allows you to unfollow user
@app.route('/unfollow-user/<usernameOther>', methods=["GET", "POST"])
def unfollow_user(usernameOther):

    selectedUser = mongo.db.users.find_one({'username': usernameOther})
    user = (session["user"])
    usernameOther = (selectedUser['username'])

    mongo.db.users.update_one(
        {"username": user}, {'$pull': {"following": usernameOther}})
    mongo.db.users.update_one({"username": usernameOther}, {
                              '$pull': {"followers": user}})
    flash("You are no longer following " + selectedUser['username'])

    return redirect(url_for('other_profile', usernameOther=usernameOther))


# renders list of users the user follows
@app.route("/following/")
def following():
    try:
        listOfUsers = mongo.db.users.find()
        allCurrentUsernames = mongo.db.users.distinct("username")
        listOfProjectNames = mongo.db.projects.distinct('projectTitle')
        users = mongo.db.users.find()
        user = (session["user"])
        user_notifications = mongo.db.users.find_one({'username': user})
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        current_user = mongo.db.users.find_one({'username': user})
        user_id = mongo.db.users.find_one({'username': user})['_id']

        return render_template(
            "following.html",
            user=user,
            username=username,
            current_user=current_user,
            user_id=user_id,
            users=users,
            listOfUsers=listOfUsers,
            user_notifications=user_notifications,
            allCurrentUsernames=allCurrentUsernames,
            listOfProjectNames=listOfProjectNames)
    except BaseException:
        return render_template("login.html")


# renders list of users followers
@app.route("/followers/")
def followers():
    try:
        listOfUsers = mongo.db.users.find()
        allCurrentUsernames = mongo.db.users.distinct("username")
        listOfProjectNames = mongo.db.projects.distinct('projectTitle')
        users = mongo.db.users.find()
        user = (session["user"])
        user_notifications = mongo.db.users.find_one({'username': user})
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        current_user = mongo.db.users.find_one({'username': user})
        user_id = mongo.db.users.find_one({'username': user})['_id']

        return render_template(
            "followers.html",
            user=user,
            username=username,
            current_user=current_user,
            user_id=user_id,
            users=users,
            listOfUsers=listOfUsers,
            user_notifications=user_notifications,
            allCurrentUsernames=allCurrentUsernames,
            listOfProjectNames=listOfProjectNames)

    except BaseException:
        return render_template("login.html")


# creates a new musical project
@app.route("/create_a_project/", methods=["GET", "POST"])
def create_a_project():
    try:
        user = (session['user'])
        listOfUsers = mongo.db.users.find()
        allCurrentUsernames = mongo.db.users.distinct("username")
        listOfProjectNames = mongo.db.projects.distinct('projectTitle')

        user_notifications = mongo.db.users.find_one({'username': user})
        projects = mongo.db.projects.find({'username': user})

        if request.method == "POST":
            # check if project name already exists for user
            existing_project = mongo.db.projects.find_one(
                {"project-title": request.form.get("project-title").lower()})

            if existing_project in projects:
                flash("You already have a project by this name")
                return redirect(url_for("create_a_project"))

            new_project = {
                "username": request.form.get("project-username"),
                "projectTitle": request.form.get("project-title").lower(),
                "projectDescription": request.form.get("project-description"),
                "city": request.form.get("city"),
                "email": request.form.get("email"),
                "instruments": request.form.getlist("instruments"),
                "genres": request.form.getlist("genres"),
                "completed": False,
                "projectFiles": [],
                "projectMembers": [],
                "applications": []
            }

            mongo.db.projects.insert_one(new_project)

            flash("Project successfully created!")
            return redirect(url_for('my_projects'))

        return render_template('create-a-project.html', user=user,
                               user_notifications=user_notifications,
                               allCurrentUsernames=allCurrentUsernames,
                               listOfProjectNames=listOfProjectNames)

    except BaseException:
        return render_template("login.html")


# deletes users project and all related files and info
@app.route('/delete_project/<thisProjectId>/<thisProjectTitle>/<noOfFiles>')
def delete_project(thisProjectId, thisProjectTitle, noOfFiles):
    user = (session['user'])
    listOfUsers = mongo.db.users.find()
    allCurrentUsernames = mongo.db.users.distinct("username")
    listOfProjectNames = mongo.db.projects.distinct('projectTitle')
    user_notifications = mongo.db.users.find_one({'username': user})
    projects = mongo.db.projects.find({'username': user})
    project_number = mongo.db.projects.count_documents({'username': user})
    username = mongo.db.users.find_one({'username': user})

    thisProjectId = thisProjectId
    thisProjectTitle = thisProjectTitle
    noOfFiles = int(noOfFiles)

    result1 = []
    result2 = []

    for nameOfFiles in mongo.db.projects.find({'_id': ObjectId(thisProjectId)}, {
                                              'projectFiles': {'file': True}}):

        result1.append(nameOfFiles['projectFiles'])
        for i in range(noOfFiles):
            result2.append(nameOfFiles['projectFiles'][i]['file'])

    mongo.db.projects.delete_one({'_id': ObjectId(thisProjectId)})

    for filename in result2:
        key = str(filename)
        my_bucket = get_bucket()
        my_bucket.Object(key).delete()

    flash('Project Deleted.')

    return redirect(url_for('my_projects'))


# renders page of users projects
@app.route('/my_projects/')
def my_projects():
    try:
        user = (session['user'])
        listOfUsers = mongo.db.users.find()
        allCurrentUsernames = mongo.db.users.distinct("username")
        listOfProjectNames = mongo.db.projects.distinct('projectTitle')

        user_notifications = mongo.db.users.find_one({'username': user})
        projects = mongo.db.projects.find({'username': user})
        project_number = mongo.db.projects.count_documents({'username': user})
        username = mongo.db.users.find_one({'username': user})

        return render_template('my-projects.html', user=user,
                               projects=projects, username=username,
                               user_notifications=user_notifications,
                               project_number=project_number,
                               allCurrentUsernames=allCurrentUsernames,
                               listOfProjectNames=listOfProjectNames)
    except BaseException:
        return render_template("login.html")


# application to join another users project
@app.route('/apply_to_project/<thisProject>/<usernameOther>',
           methods=["GET", "POST"])
def apply_to_project(thisProject, usernameOther):
    try:
        listOfUsers = mongo.db.users.find()
        allCurrentUsernames = mongo.db.users.distinct("username")
        listOfProjectNames = mongo.db.projects.distinct('projectTitle')
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        user = (session["user"])
        user_notifications = mongo.db.users.find_one({'username': user})
        current_user = mongo.db.users.find_one({'username': user})

        thisProjectId = mongo.db.projects.find_one(
            {'projectTitle': thisProject})['_id']
        user_notifications = mongo.db.users.find_one({'username': user})
        thisProject = mongo.db.projects.find_one({'projectTitle': thisProject})

        thisProjectTitle = thisProject['projectTitle']

        if request.method == "POST":
            thisProjectId = request.form.get('project-id')
            new_project_apply = {
                "projectMessage": request.form.get("project-message"),
                "city": request.form.get('city'),
                "email": request.form.get('email'),
                "instruments": request.form.getlist("instruments"),
                "genres": request.form.getlist("genres"),
                "applicantUsername": mongo.db.users.find_one({"username": session["user"]})["username"],
                "isApproved": False
            }
            usernameOther = request.form.get('project-username')
            mongo.db.users.update_one({"username": usernameOther}, {
                                      '$push': {"notifications": thisProjectTitle}})
            mongo.db.projects.update_one({'_id': ObjectId(thisProjectId)}, {
                                         '$push': {"applications": new_project_apply}})
            flash("Your application to " +
                  thisProject['projectTitle'] + " has been submitted.")

            return redirect(url_for("profile", username=username))

        return render_template(
            'apply-to-project.html',
            user=user,
            user_notifications=user_notifications,
            thisProject=thisProject,
            usernameOther=usernameOther,
            listOfUsers=listOfUsers,
            allCurrentUsernames=allCurrentUsernames,
            listOfProjectNames=listOfProjectNames)

    except BaseException:
        return render_template("login.html")


# accept users application to your project and inform them of outcome
@app.route(
    '/accept_application/<applicant>/<applicantInstrument>/<thisProject>/<thisProjectTitle>/',
    methods=[
        "GET",
        "POST"])
def accept_application(
        applicant,
        applicantInstrument,
        thisProject,
        thisProjectTitle):
    try:
        listOfUsers = mongo.db.users.find()
        allCurrentUsernames = mongo.db.users.distinct("username")
        listOfProjectNames = mongo.db.projects.distinct('projectTitle')
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        user = (session["user"])
        user_notifications = mongo.db.users.find_one({'username': user})
        current_user = mongo.db.users.find_one({'username': user})
        thisProject = thisProject
        applicantInstrument = applicantInstrument
        thisProjectTitle = thisProjectTitle

        user_notifications = mongo.db.users.find_one({'username': user})

        approvedApplication = {
            'memberUsername': applicant,
            'memberInstrument': applicantInstrument
        }

        mongo.db.projects.update_one({'_id': ObjectId(thisProject)}, {
                                     '$push': {"projectMembers": approvedApplication}})
        mongo.db.projects.update_one(
            {'_id': ObjectId(thisProject)},
            {'$pull': {'applications': {'applicantUsername': applicant}}},

        )
        mongo.db.users.update_one({"username": applicant}, {'$push': {
                                  "notifications": "Application to "
                                  + thisProjectTitle + " approved."}})

        flash("Application Approved")

        return redirect(request.referrer)
    except BaseException:
        return render_template("login.html")


# remove project member, barring them access to the project
@app.route('/remove_member/<thisProject>/<member>/<thisProjectTitle>')
def remove_member(thisProject, member, thisProjectTitle):
    try:
        thisProject = thisProject
        member = member
        thisProjectTitle = thisProjectTitle

        mongo.db.projects.update_one({'_id': ObjectId(thisProject)}, {'$pull': {
                                     'projectMembers': {'memberUsername': member}}})
        mongo.db.users.update_one({'username': member}, {
                                  '$push': {'notifications': 'You were \
                                      removed from ' + thisProjectTitle}})

        flash(member + ' removed from project.')

        return redirect(request.referrer)
    except BaseException:
        return render_template("login.html")


# deny users project application and inform them of outcome
@app.route('/deny_application/<applicant>/<thisProject>/<thisProjectTitle>',
           methods=["GET", "POST"])
def deny_application(applicant, thisProject, thisProjectTitle):
    try:
        listOfUsers = mongo.db.users.find()
        allCurrentUsernames = mongo.db.users.distinct("username")
        listOfProjectNames = mongo.db.projects.distinct('projectTitle')
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        user = (session["user"])
        user_notifications = mongo.db.users.find_one({'username': user})
        current_user = mongo.db.users.find_one({'username': user})
        thisProject = thisProject
        thisProjectTitle = thisProjectTitle

        user_notifications = mongo.db.users.find_one({'username': user})

        mongo.db.projects.update_one(
            {'_id': ObjectId(thisProject)},
            {'$pull': {'applications': {'applicantUsername': applicant}}},
        )

        mongo.db.users.update_one({"username": applicant}, {'$push': {
                                  "notifications": "Application to "
                                  + thisProjectTitle + " was denied."}})
        flash("Application Denied")
        return redirect(request.referrer)
    except BaseException:
        return render_template("login.html")


# renders page of all relevant projects to user
@app.route('/browse_projects/')
def browse_projects():

    listOfUsers = mongo.db.users.find()
    allCurrentUsernames = mongo.db.users.distinct("username")
    listOfProjectNames = mongo.db.projects.distinct('projectTitle')
    user = (session["user"])
    user_notifications = mongo.db.users.find_one({'username': user})
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    projects = mongo.db.projects.find()
    myProfile = mongo.db.users.find_one({'username': username})

    return render_template(
        'browse-projects.html',
        listOfUsers=listOfUsers,
        allCurrentUsernames=allCurrentUsernames,
        listOfProjectNames=listOfProjectNames,
        user_notifications=user_notifications,
        username=username,
        projects=projects,
        myProfile=myProfile)


# renders all other user projects
@app.route('/browse_all_projects/')
def browse_all_projects():
    try:
        listOfUsers = mongo.db.users.find()
        allCurrentUsernames = mongo.db.users.distinct("username")
        listOfProjectNames = mongo.db.projects.distinct('projectTitle')
        user = (session["user"])
        user_notifications = mongo.db.users.find_one({'username': user})
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        projects = mongo.db.projects.find()
        myProfile = mongo.db.users.find_one({'username': username})

        return render_template(
            'browse-all-projects.html',
            listOfUsers=listOfUsers,
            allCurrentUsernames=allCurrentUsernames,
            listOfProjectNames=listOfProjectNames,
            user_notifications=user_notifications,
            username=username,
            projects=projects,
            myProfile=myProfile)

    except BaseException:
        return render_template("login.html")


# allows user to update details about the project from "my-projects" page
@app.route('/manage_project/<thisProject>/', methods=["GET", "POST"])
def manage_project(thisProject):

    listOfUsers = mongo.db.users.find()
    allCurrentUsernames = mongo.db.users.distinct("username")
    listOfProjectNames = mongo.db.projects.distinct('projectTitle')
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    user = (session["user"])
    user_notifications = mongo.db.users.find_one({'username': user})
    current_user = mongo.db.users.find_one({'username': user})

    user_notifications = mongo.db.users.find_one({'username': user})
    thisProject = mongo.db.projects.find_one(
        {'_id': ObjectId(thisProject)})
    thisProjectTitle = thisProject['projectTitle']
    thisProjectId = thisProject['_id']
    applications = mongo.db.projects.find_one(
        {'_id': thisProjectId})['applications']
    members = mongo.db.projects.find_one({'_id': ObjectId(thisProjectId)})[
        'projectMembers']

    if request.method == "POST":

        mongo.db.projects.update_one(
            {"_id": ObjectId(thisProjectId)},
            {
                '$set': {
                    "username": request.form.get("project-username"),
                    "projectTitle": request.form.get("project-title").lower(),
                    "projectDescription": request.form.get("project-description"),
                    "city": request.form.get("city"),
                    "email": request.form.get("email"),
                    "instruments": request.form.getlist("instruments"),
                    "genres": request.form.getlist("genres")
                }
            })

        return redirect(request.referrer)

    return render_template(
        'manage-projects.html',
        user=user,
        user_notifications=user_notifications,
        thisProject=thisProject,
        listOfUsers=listOfUsers,
        applications=applications,
        members=members,
        allCurrentUsernames=allCurrentUsernames,
        listOfProjectNames=listOfProjectNames,
        username=username)


# allows user to update details about the project from notification link
@app.route('/manage_project_link/<thisProject>/', methods=["GET", "POST"])
def manage_project_link(thisProject):
    try:
        listOfUsers = mongo.db.users.find()
        allCurrentUsernames = mongo.db.users.distinct("username")
        listOfProjectNames = mongo.db.projects.distinct('projectTitle')
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        user = (session["user"])
        user_notifications = mongo.db.users.find_one({'username': user})
        current_user = mongo.db.users.find_one({'username': user})
        thisProject = mongo.db.projects.find_one(
            {'projectTitle': thisProject})['_id']
        user_notifications = mongo.db.users.find_one({'username': user})
        thisProject = mongo.db.projects.find_one(
            {'_id': ObjectId(thisProject)})
        thisProjectTitle = thisProject['projectTitle']
        thisProjectId = thisProject['_id']
        applications = mongo.db.projects.find_one(
            {'_id': thisProjectId})['applications']
        members = mongo.db.projects.find_one({'_id': ObjectId(thisProjectId)})[
            'projectMembers']

        if request.method == "POST":

            mongo.db.projects.update_one(
                {"_id": ObjectId(thisProjectId)},
                {
                    '$set': {
                        "username": request.form.get("project-username"),
                        "projectTitle": request.form.get("project-title").lower(),
                        "projectDescription": request.form.get("project-description"),
                        "city": request.form.get("city"),
                        "email": request.form.get("email"),
                        "instruments": request.form.getlist("instruments"),
                        "genres": request.form.getlist("genres")
                    }
                })

            return redirect(request.referrer)

        return render_template(
            'manage-projects.html',
            user=user,
            user_notifications=user_notifications,
            thisProject=thisProject,
            listOfUsers=listOfUsers,
            applications=applications,
            members=members,
            allCurrentUsernames=allCurrentUsernames,
            listOfProjectNames=listOfProjectNames,
            username=username)
    except BaseException:
        return render_template("login.html")


# renders list of projects the user is in
@app.route('/projects_im_in/')
def projects_im_in():
    try:
        listOfUsers = mongo.db.users.find()
        allCurrentUsernames = mongo.db.users.distinct("username")
        listOfProjectNames = mongo.db.projects.distinct('projectTitle')
        user = (session["user"])
        user_notifications = mongo.db.users.find_one({'username': user})
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        projectsImIn = mongo.db.projects.find(
            {'projectMembers.memberUsername': username})
        projectsImInNumber = mongo.db.projects.count_documents(
            {'projectMembers.memberUsername': username})

        return render_template(
            'projects-im-in.html',
            listOfUsers=listOfUsers,
            allCurrentUsernames=allCurrentUsernames,
            user=user,
            user_notifications=user_notifications,
            projectsImIn=projectsImIn,
            projectsImInNumber=projectsImInNumber,
            listOfProjectNames=listOfProjectNames)

    except BaseException:
        return render_template("login.html")


"""displays hub page to selected project, allowing access to comment
chat, and project files"""


@app.route('/project_hub/<thisProject>/')
def project_hub(thisProject):
    try:
        listOfUsers = mongo.db.users.find()
        allCurrentUsernames = mongo.db.users.distinct("username")
        listOfProjectNames = mongo.db.projects.distinct('projectTitle')
        user = (session["user"])
        user_notifications = mongo.db.users.find_one({'username': user})
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]

        thisProjectId = thisProject
        thisProject = mongo.db.projects.find_one(
            {'_id': ObjectId(thisProject)})

        thisProjectTitle = thisProject['projectTitle']
        members = mongo.db.projects.find_one({'_id': ObjectId(thisProjectId)})[
            'projectMembers']
        projectFiles = mongo.db.projects.find_one(
            {'projectTitle': thisProjectTitle})['projectFiles']
        projectFilesNumber = thisProject['projectFiles']

        return render_template(
            'project-hub.html',
            listOfUsers=listOfUsers,
            allCurrentUsernames=allCurrentUsernames,
            user=user,
            user_notifications=user_notifications,
            username=username,
            thisProject=thisProject,
            thisProjectTitle=thisProjectTitle,
            members=members,
            projectFiles=projectFiles,
            projectFilesNumber=projectFilesNumber,
            listOfProjectNames=listOfProjectNames)

    except BaseException:
        return render_template("login.html")


# allows user to add comment visible by other project members
@app.route('/add_comment/<thisProject>', methods=["GET", "POST"])
def add_comment(thisProject):
    try:
        user = (session["user"])
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        thisProject = thisProject
        thisProjectTitle = mongo.db.projects.find_one(
            {'_id': ObjectId(thisProject)})['projectTitle']

        projectHost = mongo.db.projects.find_one(
            {'_id': ObjectId(thisProject)})['username']
        newComment = {
            'userComment': request.form.get('addComment'),
            'date': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            'username': username
        }

        mongo.db.projects.update_one({'_id': ObjectId(thisProject)}, {
                                     '$push': {"comments": newComment}})
        mongo.db.users.update_one({"username": projectHost}, {
                                  '$push': {"notifications": "New comment \
                                  on project: " + thisProjectTitle}})

        flash("Comment Added")
        return redirect(request.referrer)
    except BaseException:
        return render_template("login.html")


# clears the users notifications list
@app.route('/clear_notifications/')
def clear_notifications():
    try:
        user = (session['user'])
        listOfUsers = mongo.db.users.find()

        user_notifications = mongo.db.users.find_one({'username': user})

        mongo.db.users.update_one(
            {"username": user}, {'$set': {'notifications': []}})

        return redirect(request.referrer)
    except BaseException:
        return render_template("login.html")


# uploads users files to project hub file system
@app.route('/upload_project_files/<thisProject>/', methods=['GET', 'POST'])
def upload_project_files(thisProject):
    try:
        listOfUsers = mongo.db.users.find()
        allCurrentUsernames = mongo.db.users.distinct("username")
        listOfProjectNames = mongo.db.projects.distinct('projectTitle')
        user = (session["user"])
        user_notifications = mongo.db.users.find_one({'username': user})
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]

        thisProject = mongo.db.projects.find_one(
            {'_id': ObjectId(thisProject)})["_id"]
        thisProjectTitle = mongo.db.projects.find_one(
            {'_id': ObjectId(thisProject)})["projectTitle"]
        members = mongo.db.projects.find_one({'projectTitle': thisProjectTitle})[
            'projectMembers']
        projectFiles = mongo.db.projects.find_one(
            {'projectTitle': thisProjectTitle})['projectFiles']
        projectFilesNumber = mongo.db.projects.count_documents(
            {'projectFiles': projectFiles})

        if request.method == 'POST':
            if 'file1' not in request.files:
                return 'there is no file1 in form!'
            file1 = request.files['file1']
            userChosenName = request.form.get('file-name')
            newFileName = userChosenName + "-" + user
            path = os.path.join(
                app.config['UPLOAD_FOLDER_PROJECT'], file1.filename)
            ext = pathlib.Path(path).suffix
            newPath = os.path.join(
                app.config['UPLOAD_FOLDER_PROJECT'], newFileName + ext)

            my_bucket = get_bucket()
            my_bucket.Object(newPath).put(Body=file1)

            project_file_update = {
                'file': newPath,
                'displayName': request.form.get('file-name') + ext,
                'fileDescription': request.form.get('file-description'),
                'folder': request.form.get('file-folder'),
                'uploader': username,
                'date': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            }
            mongo.db.projects.update_one({'_id': ObjectId(thisProject)}, {
                                         '$push': {"projectFiles": project_file_update}})
            flash("Project file uploaded")

            return redirect(url_for('project_hub', thisProject=thisProject))

            return str(output)

        return render_template(
            'project-file-upload.html',
            listOfUsers=listOfUsers,
            user_notifications=user_notifications,
            thisProject=thisProject,
            thisProjectTitle=thisProjectTitle,
            allCurrentUsernames=allCurrentUsernames,
            listOfProjectNames=listOfProjectNames)

    except BaseException:
        return render_template("login.html")


# function to allow direct messaging between users
@app.route('/messages/<usernameToContact>', methods=['GET', 'POST'])
def messages(usernameToContact):
    try:
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]

        usernameToContact = usernameToContact
        listOfUsers = mongo.db.users.find()
        allCurrentUsernames = mongo.db.users.distinct("username")
        listOfProjectNames = mongo.db.projects.distinct('projectTitle')
        user = (session["user"])
        user_notifications = mongo.db.users.find_one({'username': user})
        messages = mongo.db.messages.find(
            {'members': [username, usernameToContact], 'members':
             [usernameToContact, username]})

        if request.method == 'POST':

            conversation = {
                'username': username,
                'message': request.form.get('message'),
                'date': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            }

            convoExists1 = mongo.db.messages.count_documents(
                {'members': [username, usernameToContact]})
            convoExists2 = mongo.db.messages.count_documents(
                {'members': [usernameToContact, username]})

            if convoExists1 == 0 and convoExists2 == 0:
                mongo.db.messages.insert_one(
                    {'members': [username, usernameToContact]})
                mongo.db.messages.insert_one(
                    {'members': [usernameToContact, username]})
                mongo.db.messages.update_one({'members': [username, usernameToContact]}, {
                                             '$push': {'messages': conversation}})
                mongo.db.messages.update_one({'members': [usernameToContact, username]}, {
                                             '$push': {'messages': conversation}})
                messages = mongo.db.messages.find(
                    {'members': [username, usernameToContact], 'members': [usernameToContact, username]})
                notification = 'You have a new message from ' + username
                mongo.db.users.update_one({"username": usernameToContact}, {
                                          '$push': {'notifications': notification}})

            else:
                mongo.db.messages.update_one({'members': [username, usernameToContact]}, {
                                             '$push': {'messages': conversation}})
                mongo.db.messages.update_one({'members': [usernameToContact, username]}, {
                                             '$push': {'messages': conversation}})

                messages = mongo.db.messages.find(
                    {'members': [username, usernameToContact], 'members': [usernameToContact, username]})
                notification = 'You have a new message from ' + username
                mongo.db.users.update_one({"username": usernameToContact}, {
                                          '$push': {'notifications': notification}})

            return render_template(
                'messages.html',
                listOfUsers=listOfUsers,
                allCurrentUsernames=allCurrentUsernames,
                listOfProjectNames=listOfProjectNames,
                user_notifications=user_notifications,
                messages=messages,
                username=username,
                usernameToContact=usernameToContact)

        return render_template(
            'messages.html',
            listOfUsers=listOfUsers,
            allCurrentUsernames=allCurrentUsernames,
            listOfProjectNames=listOfProjectNames,
            user_notifications=user_notifications,
            messages=messages,
            username=username,
            usernameToContact=usernameToContact)

    except BaseException:
        return render_template("login.html")


# renders list of users conversations with others
@app.route('/convo_list/')
def convo_list():
    try:
        listOfUsers = mongo.db.users.find()
        allCurrentUsernames = mongo.db.users.distinct("username")
        listOfProjectNames = mongo.db.projects.distinct('projectTitle')
        user = (session["user"])
        users = mongo.db.users.find()
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        user_notifications = mongo.db.users.find_one({'username': user})
        myConversations = mongo.db.messages.find({'members': username})

        return render_template(
            'convo-list.html',
            listOfUsers=listOfUsers,
            allCurrentUsernames=allCurrentUsernames,
            listOfProjectNames=listOfProjectNames,
            user_notifications=user_notifications,
            myConversations=myConversations,
            username=username,
            users=users)

    except BaseException:
        return render_template("login.html")


""" creates new message to other user if no messages exist
otherwise redirects to existing messages """


@app.route('/contact/<usernameToContact>', methods=['GET', 'POST'])
def contact(usernameToContact):
    try:
        listOfUsers = mongo.db.users.find()
        allCurrentUsernames = mongo.db.users.distinct("username")
        listOfProjectNames = mongo.db.projects.distinct('projectTitle')
        user = (session["user"])
        user_notifications = mongo.db.users.find_one({'username': user})
        usernameToContact = usernameToContact
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        selectedUser = mongo.db.users.find_one({'username': usernameToContact})
        conversationExists = mongo.db.messages.find(
            {'members': [username, usernameToContact], 'members': [usernameToContact, username]})

        if conversationExists:
            messages = mongo.db.messages.find(
                {'members': [username, usernameToContact], 'members': [usernameToContact, username]})

            return redirect(
                url_for(
                    'messages',
                    usernameToContact=usernameToContact))

        else:
            if request.method == 'POST':

                conversation = {
                    'username': username,
                    'message': request.form.get('message'),
                    'date': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                }

                convoExists1 = mongo.db.messages.count_documents(
                    {'members': [username, usernameToContact]})
                convoExists2 = mongo.db.messages.count_documents(
                    {'members': [usernameToContact, username]})

                if convoExists1 == 0 and convoExists2 == 0:
                    mongo.db.messages.insert_one(
                        {'members': [username, usernameToContact]})
                    mongo.db.messages.insert_one(
                        {'members': [usernameToContact, username]})
                    mongo.db.messages.update_one({'members': [username, usernameToContact]}, {
                                                 '$push': {'messages': conversation}})
                    mongo.db.messages.update_one({'members': [usernameToContact, username]}, {
                                                 '$push': {'messages': conversation}})
                    messages = mongo.db.messages.find(
                        {'members': [username, usernameToContact], 'members': [usernameToContact, username]})

                    notification = 'You have a new message from ' + username
                    mongo.db.users.update_one({"username": usernameToContact}, {
                                              '$push': {'notifications': notification}})

                else:
                    mongo.db.messages.update_one({'members': [username, usernameToContact]}, {
                                                 '$push': {'messages': conversation}})
                    mongo.db.messages.update_one({'members': [usernameToContact, username]}, {
                                                 '$push': {'messages': conversation}})

                    messages = mongo.db.messages.find(
                        {'members': [username, usernameToContact], 'members': [usernameToContact, username]})

                    notification = 'You have a new message from ' + username
                    mongo.db.users.update_one({"username": usernameToContact}, {
                                              '$push': {'notifications': notification}})

                flash('Message Sent')

                return redirect(
                    url_for(
                        'messages',
                        usernameToContact=usernameToContact))

        return render_template('contact.html', listOfUsers=listOfUsers,
                               allCurrentUsernames=allCurrentUsernames,
                               listOfProjectNames=listOfProjectNames,
                               user_notifications=user_notifications,
                               usernameToContact=usernameToContact)

    except BaseException:
        return render_template("login.html")


# generic function for file upload to amazon S3
def upload_file_to_s3(file1, bucket_name, acl="public-read"):
    try:
        s3.Bucket('harmonise').upload_fileobj(
            file1,
            bucket_name,
            file1.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type  # Set appropriate content type as per the file
            }
        )

    except Exception as e:
        print("Something Happened: ", e)
        return e
    return "{}{}".format(app.config["S3_LOCATION"], file1.filename)


# uploads user project files to amazon s3
@app.route('/upload_s3', methods=['POST'])
def upload_s3():
    try:
        file = request.files['file-s3']

        my_bucket = get_bucket()
        my_bucket.Object(file.filename).put(Body=file)

        return redirect(url_for('files'))
    except BaseException:
        return render_template("login.html")


# uploads user profile image to folder in amazon s3
@app.route('/upload_s3_profile_pic', methods=['POST'])
def upload_s3_profile_pic():
    try:
        file = request.files['file-s3']

        my_bucket = get_bucket()
        my_bucket.Object(file.filename).put(Body=file)

        return redirect(url_for('files'))
    except BaseException:
        return render_template("login.html")


# deletes user files from amazon s3 bucket
@app.route('/delete_s3/<thisProject>', methods=['post'])
def delete_s3(thisProject):
    try:
        thisProject = thisProject
        key = request.form['key']

        mongo.db.projects.update_one(
            {'_id': ObjectId(thisProject)},
            {'$pull': {'projectFiles': {'file': key}}}
        )
        my_bucket = get_bucket()
        my_bucket.Object(key).delete()

        flash("File deleted.")

        listOfUsers = mongo.db.users.find()
        allCurrentUsernames = mongo.db.users.distinct("username")
        listOfProjectNames = mongo.db.projects.distinct('projectTitle')
        user = (session["user"])
        user_notifications = mongo.db.users.find_one({'username': user})
        username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]

        thisProject = mongo.db.projects.find_one(
            {'_id': ObjectId(thisProject)})
        thisProjectTitle = thisProject['projectTitle']
        members = mongo.db.projects.find_one({'projectTitle': thisProjectTitle})[
            'projectMembers']
        projectFiles = mongo.db.projects.find_one(
            {'projectTitle': thisProjectTitle})['projectFiles']
        projectFilesNumber = thisProject['projectFiles']

        return render_template(
            'project-hub.html',
            listOfUsers=listOfUsers,
            allCurrentUsernames=allCurrentUsernames,
            user=user,
            user_notifications=user_notifications,
            username=username,
            thisProject=thisProject,
            thisProjectTitle=thisProjectTitle,
            members=members,
            projectFiles=projectFiles,
            projectFilesNumber=projectFilesNumber,
            listOfProjectNames=listOfProjectNames)

    except BaseException:
        return render_template("login.html")


# downloads files from amazon s3 bucket
@app.route('/download_s3', methods=['post'])
def download_s3():
    try:
        key = request.form.get('key')

        my_bucket = get_bucket()

        file_obj = my_bucket.Object(key).get()

        if '.pdf' in key:
            typeOfFile = 'application/pdf'
        elif '.jpg' in key or '.jpeg' in key:
            typeOfFile = 'image/jpeg'
        elif '.mp3' in key:
            typeOfFile = 'audio/mpeg'
        elif '.mp4' in key:
            typeOfFile = 'video/mp4'
        elif '.png' in key:
            typeOfFile = 'image/png'

        return Response(
            file_obj['Body'].read(),
            mimetype=typeOfFile,
            headers={
                "Content-Disposition": 'attachment;filename={}'.format(key)}
        )
    except BaseException:
        return render_template("login.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
