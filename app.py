import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo  
from bson.objectid import ObjectId  
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image
import pathlib

if os.path.exists("env.py"):
    import env


app = Flask(__name__)


UPLOAD_FOLDER = 'static/images/user-images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)

global user




@app.route("/")
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))
        
        register = {
            "username": request.form.get("username").lower(),
            "fname": request.form.get("first_name"),
            "lname": request.form.get("last_name"),
            "password": generate_password_hash(request.form.get("password")),
            "city": request.form.get("city"),
            "email": request.form.get("email"),
            "instruments": request.form.getlist("instruments"),
            "genres": request.form.getlist("genres"),
            "bio": "Tell us a little about yourself! Click the edit profile button to write your bio",
            "profile_pic": "/static/images/default-pp-min.png",
            "followers": [],
            "following": []
        }

        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")
    


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



@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))    


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"] 
    user = (session["user"])      
    
         
    if session["user"]:
        user = (session["user"])
        current_user = mongo.db.users.find_one({'username':user})

        return render_template("profile.html", username=username, current_user=current_user)

    return redirect(url_for("login"))



@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    if request.method == "POST":
        edit = { '$set': {
                "fname": request.form.get("first_nameEdit"),
                "lname": request.form.get("last_nameEdit"),
                "city": request.form.get("cityEdit"),
                "instruments": request.form.getlist("instrumentsEdit"),
                "genres": request.form.getlist("genreEdit"),
                "bio": request.form.get("bio")
                
            }}
        user = (session["user"])    
        current_user = mongo.db.users.find_one({'username':user})
        user_id = mongo.db.users.find_one({'username':user})['_id']
        
        mongo.db.users.update_one({'_id':ObjectId(user_id)},edit)  
        flash("success")
    
    if session["user"]:
        user = (session["user"])
        current_user = mongo.db.users.find_one({'username':user})
        

    return render_template("edit-profile.html", current_user=current_user)




@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    user = (session["user"])
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    current_user = mongo.db.users.find_one({'username':user})    
    user_id = mongo.db.users.find_one({'username':user})['_id']
    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file1 in form!'   
        file1 = request.files['file1']
        
        newFileName = "profile-image" + "-" + user 
        path = os.path.join(app.config['UPLOAD_FOLDER'], file1.filename)
        ext = pathlib.Path(path).suffix
        newPath = os.path.join(app.config['UPLOAD_FOLDER'], newFileName + ext)
        file1.save(newPath)
        profile_pic_update = {'$set':{
                'profile_pic': '/' + newPath
            }
        }
        mongo.db.users.update_one({'_id':ObjectId(user_id)},profile_pic_update) 
        flash("Profile Picture Updated!")

        return redirect(url_for("profile", username=username, current_user=current_user))
        
    return render_template("upload_file.html")


@app.route("/other_users")    
def other_users():
    users = mongo.db.users.find()
    user = (session["user"])
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    current_user = mongo.db.users.find_one({'username':user})    
    user_id = mongo.db.users.find_one({'username':user})['_id']
    

    return render_template("other-users.html", user=user, username=username, current_user=current_user, user_id=user_id, users=users)


@app.route('/other_profile/<username>', methods=["GET", "POST"])
def other_profile(username):
    selectedUser= mongo.db.users.find_one({'username':username})
    user = (session["user"])
    current_user = mongo.db.users.find_one({'username':user}) 
    following = mongo.db.users.find_one({'username':user},{"following"})
    
    if username != user:
        return render_template('other-profile.html', username=username, selectedUser=selectedUser,following=following)    
    return redirect(url_for("profile", username=username, current_user=current_user))  


@app.route('/follow-user/<username>', methods=["GET", "POST"])    
def follow_user(username):
    selectedUser = mongo.db.users.find_one({'username':username})
    user = (session["user"])
    current_user = mongo.db.users.find_one({'username':user})
    user_id = mongo.db.users.find_one({'username':user})['_id']
    following = mongo.db.users.find_one({'username':user},{"following"})

    mongo.db.users.update_one( { "username" : user },{ '$push': { "following": username } })
    mongo.db.users.update_one( { "username" : username },{ '$push': { "followers": user } })
    flash("You are now following " + username)

    return redirect(url_for("other_profile", user=user, username=username, current_user=current_user, user_id=user_id, selectedUser=selectedUser, following=following))



@app.route('/unfollow-user/<username>', methods=["GET", "POST"])    
def unfollow_user(username):
    selectedUser = mongo.db.users.find_one({'username':username})
    user = (session["user"])
    current_user = mongo.db.users.find_one({'username':user})
    user_id = mongo.db.users.find_one({'username':user})['_id']
    following = mongo.db.users.find_one({'username':user},{"following"})

    mongo.db.users.update_one( { "username" : user },{ '$pull': { "following": username } })
    mongo.db.users.update_one( { "username" : username },{ '$pull': { "followers": user } })
    flash("You are no longer following " + username)

        
    return redirect(url_for("other_profile", user=user, username=username, current_user=current_user, user_id=user_id, selectedUser=selectedUser, following=following))


@app.route("/my_connections")    
def my_connections():
    
    user = (session["user"])
    users = mongo.db.users.find({"username" : user},{'followers'})
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    current_user = mongo.db.users.find_one({'username':user})    
    user_id = mongo.db.users.find_one({'username':user})['_id']
    
    

    return render_template("my-connections.html", user=user, username=username, current_user=current_user, user_id=user_id, users=users)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)