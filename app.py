import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo  
from bson.objectid import ObjectId  
from werkzeug.security import generate_password_hash, check_password_hash
from PIL import Image
import pathlib
import datetime
from datetime import datetime, timedelta, date

if os.path.exists("env.py"):
    import env


app = Flask(__name__)


UPLOAD_FOLDER = 'static/images/user-images/'
UPLOAD_FOLDER_PROJECT = 'static/project-files/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER_PROJECT'] = UPLOAD_FOLDER_PROJECT
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")



mongo = PyMongo(app)

global user





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
            "following": [],
            "notifications": []
        }

        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")
    


@app.route("/logout")
def logout():
    listOfUsers = mongo.db.users.find()

    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))    


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    listOfUsers = mongo.db.users.find()
    allCurrentUsernames = mongo.db.users.distinct("username")

    
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"] 
    user = (session["user"])   
    user_notifications = mongo.db.users.find_one({'username':user}) 
    listOfUsers = mongo.db.users.find()
    listOfProjectNames = mongo.db.projects.distinct('projectTitle')
    
         
    if session["user"]:
        user = (session["user"])
        current_user = mongo.db.users.find_one({'username':user})

        return render_template("profile.html", username=username, current_user=current_user, listOfUsers=listOfUsers, user_notifications=user_notifications,allCurrentUsernames=allCurrentUsernames,listOfProjectNames=listOfProjectNames)

    return redirect(url_for("login"))


@app.route("/settings/<username>", methods=["GET", "POST"])
def settings(username):
    listOfUsers = mongo.db.users.find()
    allCurrentUsernames = mongo.db.users.distinct("username")
    listOfProjectNames = mongo.db.projects.distinct('projectTitle')

    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"] 
    user = (session["user"])      
    user_notifications = mongo.db.users.find_one({'username':user}) 
         
    if session["user"]:
        user = (session["user"])
        current_user = mongo.db.users.find_one({'username':user})

        return render_template("settings.html", username=username, current_user=current_user, user_notifications=user_notifications,allCurrentUsernames=allCurrentUsernames,listOfProjectNames=listOfProjectNames)

    return redirect(url_for("login"))    



@app.route("/delete_account", methods=["GET", "POST"])
def delete_account():
    listOfUsers = mongo.db.users.find()
    allCurrentUsernames = mongo.db.users.distinct("username")
    listOfProjectNames = mongo.db.projects.distinct('projectTitle')
    username = (session["user"]) 
    mongo.db.users.delete_one({"username": username})
    mongo.db.users.update_many(
    {"following": username},    
    { '$pull': { "following": username}})
    mongo.db.users.update_many(
    {"followers": username},     
    { '$pull': { "followers": username } })
    session.pop("user")
    flash("Account successfully deleted")

    return render_template("register.html")
    



@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    user = (session["user"])    
    user_notifications = mongo.db.users.find_one({'username':user}) 
    listOfUsers = mongo.db.users.find()
    allCurrentUsernames = mongo.db.users.distinct("username")
    listOfProjectNames = mongo.db.projects.distinct('projectTitle')
    if request.method == "POST":
        edit = { '$set': {
                "fname": request.form.get("first_nameEdit"),
                "lname": request.form.get("last_nameEdit"),
                "city": request.form.get("cityEdit"),
                "instruments": request.form.getlist("instrumentsEdit"),
                "genres": request.form.getlist("genreEdit"),
                "bio": request.form.get("bio")
                
            }}
        
        current_user = mongo.db.users.find_one({'username':user})
        user_id = mongo.db.users.find_one({'username':user})['_id']
        
        mongo.db.users.update_one({'_id':ObjectId(user_id)},edit)  
        flash("success")
    
    if session["user"]:
        user = (session["user"])
        current_user = mongo.db.users.find_one({'username':user})
        

    return render_template("edit-profile.html", current_user=current_user, listOfUsers=listOfUsers, user_notifications=user_notifications,allCurrentUsernames=allCurrentUsernames,listOfProjectNames=listOfProjectNames)




@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    listOfUsers = mongo.db.users.find()
    allCurrentUsernames = mongo.db.users.distinct("username")
    listOfProjectNames = mongo.db.projects.distinct('projectTitle')
    user = (session["user"])
    user_notifications = mongo.db.users.find_one({'username':user}) 
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

        return redirect(url_for("profile", username=username, current_user=current_user, listOfUsers=listOfUsers, user_notifications=user_notifications,allCurrentUsernames=allCurrentUsernames,listOfProjectNames=listOfProjectNames))
        
    return render_template("upload_file.html", listOfUsers=listOfUsers, user_notifications=user_notifications,allCurrentUsernames=allCurrentUsernames,listOfProjectNames=listOfProjectNames)


@app.route("/other_users")    
def other_users():
    listOfUsers = mongo.db.users.find()
    allCurrentUsernames = mongo.db.users.distinct("username")
    listOfProjectNames = mongo.db.projects.distinct('projectTitle')
    users = mongo.db.users.find()
    user = (session["user"])
    user_notifications = mongo.db.users.find_one({'username':user}) 
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    current_user = mongo.db.users.find_one({'username':user})    
    user_id = mongo.db.users.find_one({'username':user})['_id']
    

    return render_template("other-users.html", user=user, username=username, current_user=current_user, user_id=user_id, users=users, listOfUsers=listOfUsers, user_notifications=user_notifications,allCurrentUsernames=allCurrentUsernames,listOfProjectNames=listOfProjectNames)



@app.route("/filter_users", methods=['GET', 'POST'])
def filter_users():
    listOfUsers = mongo.db.users.find()
    allCurrentUsernames = mongo.db.users.distinct("username")
    listOfProjectNames = mongo.db.projects.distinct('projectTitle')
    user = (session["user"])
    users = mongo.db.users.find()
    user_notifications = mongo.db.users.find_one({'username':user}) 

    if request.method == "POST":
        cityQuery = request.form.get('city')
        instrumentsQuery = request.form.getlist('instruments')
        genresQuery = request.form.getlist("genres")

        return render_template("other-users-filter.html", listOfUsers=listOfUsers, allCurrentUsernames=allCurrentUsernames, listOfProjectNames=listOfProjectNames,user_notifications=user_notifications, cityQuery=cityQuery, instrumentsQuery=instrumentsQuery, genresQuery=genresQuery,users=users)


    return render_template('user-filter.html', listOfUsers=listOfUsers, allCurrentUsernames=allCurrentUsernames, listOfProjectNames=listOfProjectNames,user_notifications=user_notifications )


@app.route('/other_profile/<usernameOther>', methods=["GET", "POST"])
def other_profile(usernameOther):
    listOfUsers = mongo.db.users.find()
    allCurrentUsernames = mongo.db.users.distinct("username")
    listOfProjectNames = mongo.db.projects.distinct('projectTitle')
    listOfProjects = mongo.db.projects.distinct("projectTitle")
    selectedUser= mongo.db.users.find_one({'username':usernameOther})
    projects = mongo.db.projects.find({'username':usernameOther})
    project_number = mongo.db.projects.count_documents({'username':usernameOther})
    user = (session["user"])
    myUsername = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    projectsImIn = mongo.db.projects.find({'projectMembers.memberUsername':username})
    user_notifications = mongo.db.users.find_one({'username':user}) 
    current_user = mongo.db.users.find_one({'username':user}) 
    following = mongo.db.users.find_one({'username':user},{"following"})
    username = user
    current_user = mongo.db.users.find_one({'username':user}) 
    
    if usernameOther != user:
        return render_template('other-profile.html', selectedUser=selectedUser,following=following, listOfUsers=listOfUsers, user=user, current_user=current_user, projects=projects, user_notifications=user_notifications,project_number=project_number,allCurrentUsernames=allCurrentUsernames,listOfProjectNames=listOfProjectNames,projectsImIn=projectsImIn,myUsername=myUsername)    
    return redirect(url_for("profile", username=username, current_user=current_user, listOfUsers=listOfUsers, user=user,following=following, user_notifications=user_notifications,allCurrentUsernames=allCurrentUsernames,listOfProjectNames=listOfProjectNames))  


@app.route('/other_profile_search/', methods=["GET", "POST"])
def other_profile_search():
    user = (session["user"])
    usernameOther = request.form.get("user-search-input")
    projects = mongo.db.projects.find({'username':usernameOther})  
    project_number = mongo.db.projects.count_documents({'username':usernameOther})  
    listOfUsers = mongo.db.users.find()
    allCurrentUsernames = mongo.db.users.distinct("username")
    listOfProjectNames = mongo.db.projects.distinct('projectTitle')
    myUsername = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    projectsImIn = mongo.db.projects.find({'projectMembers.memberUsername':username})
    
    selectedUser= mongo.db.users.find_one({'username':usernameOther})
    
    
    user_notifications = mongo.db.users.find_one({'username':user}) 
    
    current_user = mongo.db.users.find_one({'username':user}) 
    following = mongo.db.users.find_one({'username':user},{"following"})

    if usernameOther not in allCurrentUsernames:
        flash("That user doesn't exist")
        username=user
        return redirect(url_for("profile", username=username, current_user=current_user, listOfUsers=listOfUsers, user=user, following=following, user_notifications=user_notifications,allCurrentUsernames=allCurrentUsernames,listOfProjectNames=listOfProjectNames))  

    
    if usernameOther != user:
        return render_template('other-profile.html', selectedUser=selectedUser,following=following, listOfUsers=listOfUsers, usernameOther=usernameOther, user=user, current_user=current_user,projects=projects, user_notifications=user_notifications,project_number=project_number,allCurrentUsernames=allCurrentUsernames,listOfProjectNames=listOfProjectNames,projectsImIn=projectsImIn,myUsername=myUsername)  
    username = user      
    return redirect(url_for("profile", username=username, current_user=current_user, listOfUsers=listOfUsers, user=user, following=following, user_notifications=user_notifications,allCurrentUsernames=allCurrentUsernames,listOfProjectNames=listOfProjectNames))  

@app.route('/follow-user/<usernameOther>', methods=["GET", "POST"])    
def follow_user(usernameOther):
    listOfUsers = mongo.db.users.distinct('username')
    allCurrentUsernames = mongo.db.users.distinct("username")
    listOfProjectNames = mongo.db.projects.distinct('projectTitle')
    selectedUser = mongo.db.users.find_one({'username': usernameOther})
    user = (session["user"])
    user_notifications = mongo.db.users.find_one({'username':user}) 
    current_user = mongo.db.users.find_one({'username':user})
    current_username = mongo.db.users.find_one({'username':user})["username"]
    user_id = mongo.db.users.find_one({'username':user})['_id']
    following = mongo.db.users.find_one({'username':user},{"following"})
    usernameOther= (selectedUser['username'])

    mongo.db.users.update_one({ "username" : usernameOther },{ '$push': { "notifications": current_username } })
    mongo.db.users.update_one( { "username" : user },{ '$push': { "following": usernameOther } })
    mongo.db.users.update_one( { "username" : usernameOther },{ '$push': { "followers": user } })
    flash("You are now following " + selectedUser['username'])

    return redirect(url_for("other_profile", user=user, current_user=current_user, user_id=user_id, selectedUser=selectedUser, following=following, listOfUsers=listOfUsers, usernameOther=usernameOther, user_notifications=user_notifications,allCurrentUsernames=allCurrentUsernames,listOfProjectNames=listOfProjectNames))



@app.route('/unfollow-user/<usernameOther>', methods=["GET", "POST"])    
def unfollow_user(usernameOther):
    listOfUsers = mongo.db.users.find()
    allCurrentUsernames = mongo.db.users.distinct("username")
    listOfProjectNames = mongo.db.projects.distinct('projectTitle')
    mongo.db.users.find_one({'username': usernameOther})
    selectedUser = mongo.db.users.find_one({'username': usernameOther})
    user = (session["user"])
    user_notifications = mongo.db.users.find_one({'username':user}) 
    current_user = mongo.db.users.find_one({'username':user})
    user_id = mongo.db.users.find_one({'username':user})['_id']
    following = mongo.db.users.find_one({'username':user},{"following"})
    usernameOther= (selectedUser['username'])


    mongo.db.users.update_one( { "username" : user },{ '$pull': { "following": usernameOther } })
    mongo.db.users.update_one( { "username" : usernameOther },{ '$pull': { "followers": user } })
    flash("You are no longer following " + selectedUser['username'])

        
    return redirect(url_for("other_profile", user=user, current_user=current_user, user_id=user_id, selectedUser=selectedUser, following=following, listOfUsers=listOfUsers, usernameOther=usernameOther, user_notifications=user_notifications,allCurrentUsernames=allCurrentUsernames,listOfProjectNames=listOfProjectNames))


@app.route("/following/")   
def following():
    listOfUsers = mongo.db.users.find()
    allCurrentUsernames = mongo.db.users.distinct("username")
    listOfProjectNames = mongo.db.projects.distinct('projectTitle')
    users = mongo.db.users.find()
    user = (session["user"])
    user_notifications = mongo.db.users.find_one({'username':user}) 
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    current_user = mongo.db.users.find_one({'username':user})    
    user_id = mongo.db.users.find_one({'username':user})['_id']
    

    return render_template("following.html", user=user, username=username, current_user=current_user, user_id=user_id, users=users, listOfUsers=listOfUsers, user_notifications=user_notifications,allCurrentUsernames=allCurrentUsernames,listOfProjectNames=listOfProjectNames)


@app.route("/followers/")   
def followers():
    listOfUsers = mongo.db.users.find()
    allCurrentUsernames = mongo.db.users.distinct("username")
    listOfProjectNames = mongo.db.projects.distinct('projectTitle')
    users = mongo.db.users.find()
    user = (session["user"])
    user_notifications = mongo.db.users.find_one({'username':user}) 
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    current_user = mongo.db.users.find_one({'username':user})    
    user_id = mongo.db.users.find_one({'username':user})['_id']
    

    return render_template("followers.html", user=user, username=username, current_user=current_user, user_id=user_id, users=users, listOfUsers=listOfUsers, user_notifications=user_notifications,allCurrentUsernames=allCurrentUsernames,listOfProjectNames=listOfProjectNames)   



@app.route("/create_a_project/", methods=["GET", "POST"])   
def create_a_project():
    user = (session['user'])
    listOfUsers = mongo.db.users.find()
    allCurrentUsernames = mongo.db.users.distinct("username")
    listOfProjectNames = mongo.db.projects.distinct('projectTitle')

    user_notifications = mongo.db.users.find_one({'username':user}) 
    projects = mongo.db.projects.find({'username':user})
    

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
            "projectMembers": []


        }

        mongo.db.projects.insert_one(new_project)
        
    
        flash("Project successfully created!")
        return redirect(url_for('my_projects', user = user, projects=projects, user_notifications=user_notifications,allCurrentUsernames=allCurrentUsernames,listOfProjectNames=listOfProjectNames))
    return render_template('create-a-project.html', user=user, user_notifications=user_notifications,allCurrentUsernames=allCurrentUsernames,listOfProjectNames=listOfProjectNames)  



@app.route('/my_projects/')
def my_projects():
    user = (session['user'])
    listOfUsers = mongo.db.users.find()
    allCurrentUsernames = mongo.db.users.distinct("username")
    listOfProjectNames = mongo.db.projects.distinct('projectTitle')

    user_notifications = mongo.db.users.find_one({'username':user}) 
    projects = mongo.db.projects.find({'username':user})
    project_number = mongo.db.projects.count_documents({'username':user})
    username = mongo.db.users.find_one({'username': user})

    return render_template('my-projects.html', user = user, projects=projects, username=username, user_notifications=user_notifications,project_number=project_number,allCurrentUsernames=allCurrentUsernames,listOfProjectNames=listOfProjectNames)



@app.route('/apply_to_project/<thisProject>/<usernameOther>', methods=["GET", "POST"])
def apply_to_project(thisProject, usernameOther):
    listOfUsers = mongo.db.users.find()
    allCurrentUsernames = mongo.db.users.distinct("username")
    listOfProjectNames = mongo.db.projects.distinct('projectTitle')
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"] 
    user = (session["user"])   
    user_notifications = mongo.db.users.find_one({'username':user}) 
    current_user = mongo.db.users.find_one({'username':user})

    user_notifications = mongo.db.users.find_one({'username':user}) 
    thisProject= mongo.db.projects.find_one({'projectTitle':thisProject})
    thisProjectId = thisProject['_id']
    thisProjectTitle = thisProject['projectTitle']

    if request.method == "POST":
        
        new_project_apply = {
            "projectMessage": request.form.get("project-message"),
            "city": request.form.get('city'),
            "email": request.form.get('email'),
            "instruments": request.form.getlist("instruments"),
            "genres": request.form.getlist("genres"),
            "applicantUsername": mongo.db.users.find_one({"username": session["user"]})["username"],
            "isApproved": False 
        }
        mongo.db.users.update_one({ "username" : usernameOther },{ '$push': { "notifications": thisProjectTitle } })
        mongo.db.projects.update_one({ '_id': thisProjectId },{ '$push': { "applications": new_project_apply } })
        flash("Your application to " + thisProject['projectTitle'] + " has been submitted.")
        
        return redirect(url_for("profile", username=username, current_user=current_user, listOfUsers=listOfUsers, user=user, following=following, user_notifications=user_notifications,usernameOther=usernameOther,allCurrentUsernames=allCurrentUsernames,listOfProjectNames=listOfProjectNames))  
    return render_template('apply-to-project.html', user=user, user_notifications=user_notifications,thisProject=thisProject, usernameOther=usernameOther, listOfUsers=listOfUsers,allCurrentUsernames=allCurrentUsernames,listOfProjectNames=listOfProjectNames)


@app.route('/accept_application/<applicant>/<applicantInstrument>/<thisProject>/<thisProjectTitle>/', methods=["GET", "POST"])
def accept_application(applicant,applicantInstrument,thisProject,thisProjectTitle):
    listOfUsers = mongo.db.users.find()
    allCurrentUsernames = mongo.db.users.distinct("username")
    listOfProjectNames = mongo.db.projects.distinct('projectTitle')
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"] 
    user = (session["user"])   
    user_notifications = mongo.db.users.find_one({'username':user}) 
    current_user = mongo.db.users.find_one({'username':user})
    thisProject= thisProject
    applicantInstrument=applicantInstrument
    thisProjectTitle=thisProjectTitle
    
    user_notifications = mongo.db.users.find_one({'username':user}) 
    
    
    
    approvedApplication = {
        'memberUsername': applicant,
        'memberInstrument': applicantInstrument
    }
    
        
    mongo.db.projects.update_one({ '_id': ObjectId(thisProject)},{ '$push': { "projectMembers": approvedApplication }})
    mongo.db.projects.update_one(
    { '_id': ObjectId(thisProject) }, 
    { '$pull': { 'applications': { 'applicantUsername': applicant } } },

    );   
    mongo.db.users.update_one({ "username" : applicant },{ '$push': { "notifications": "your application to " + thisProjectTitle + " was approved."} })
    flash("Application Approved")
        
    return redirect(request.referrer)
    



@app.route('/deny_application/<applicant>/<thisProject>/', methods=["GET", "POST"])
def deny_application(applicant,thisProject):
    listOfUsers = mongo.db.users.find()
    allCurrentUsernames = mongo.db.users.distinct("username")
    listOfProjectNames = mongo.db.projects.distinct('projectTitle')
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"] 
    user = (session["user"])   
    user_notifications = mongo.db.users.find_one({'username':user}) 
    current_user = mongo.db.users.find_one({'username':user})
    thisProject= thisProject
    
    user_notifications = mongo.db.users.find_one({'username':user}) 
    
    


    mongo.db.projects.update_one(
    { '_id': ObjectId(thisProject) }, 
    { '$pull': { 'applications': { 'applicantUsername': applicant } } },

    );    
      
    mongo.db.users.update_one({ "username" : applicant },{ '$push': { "notifications": "your application to " + thisProjectTitle + " was denied."} })
    flash("Application Denied") 
    return redirect(request.referrer)
     



@app.route('/manage_project/<thisProject>/', methods=["GET", "POST"])
def manage_project(thisProject):
    listOfUsers = mongo.db.users.find()
    allCurrentUsernames = mongo.db.users.distinct("username")
    listOfProjectNames = mongo.db.projects.distinct('projectTitle')
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"] 
    user = (session["user"])   
    user_notifications = mongo.db.users.find_one({'username':user}) 
    current_user = mongo.db.users.find_one({'username':user})
    

    user_notifications = mongo.db.users.find_one({'username':user}) 
    thisProject= mongo.db.projects.find_one({'projectTitle':thisProject})
    thisProjectId = thisProject['_id']
    thisProjectTitle = thisProject['projectTitle']
    applications = mongo.db.projects.find_one({'projectTitle':thisProjectTitle})['applications']
    members = mongo.db.projects.find_one({'projectTitle':thisProjectTitle})['projectMembers']

    if request.method == "POST":
        
       
        
        return redirect(url_for("profile", username=username, current_user=current_user, listOfUsers=listOfUsers, user=user, following=following, user_notifications=user_notifications,allCurrentUsernames=allCurrentUsernames,listOfProjectNames=listOfProjectNames))  
    return render_template('manage-projects.html', user=user, user_notifications=user_notifications,thisProject=thisProject, listOfUsers=listOfUsers, applications=applications, members=members,allCurrentUsernames=allCurrentUsernames,listOfProjectNames=listOfProjectNames) 



@app.route('/projects_im_in/')       
def projects_im_in():
    listOfUsers = mongo.db.users.find()
    allCurrentUsernames = mongo.db.users.distinct("username")
    listOfProjectNames = mongo.db.projects.distinct('projectTitle')
    user = (session["user"])   
    user_notifications = mongo.db.users.find_one({'username':user}) 
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"] 
    projectsImIn = mongo.db.projects.find({'projectMembers.memberUsername':username})
    projectsImInNumber = mongo.db.projects.count_documents({'projectMembers.memberUsername':username})
    

    return render_template('projects-im-in.html', listOfUsers=listOfUsers,allCurrentUsernames=allCurrentUsernames,user=user,user_notifications=user_notifications,projectsImIn=projectsImIn,projectsImInNumber=projectsImInNumber,listOfProjectNames=listOfProjectNames)



@app.route('/project_hub/<thisProject>/')    
def project_hub(thisProject):
    listOfUsers = mongo.db.users.find()
    allCurrentUsernames = mongo.db.users.distinct("username")
    listOfProjectNames = mongo.db.projects.distinct('projectTitle')
    user = (session["user"])   
    user_notifications = mongo.db.users.find_one({'username':user}) 
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"] 

    thisProject = mongo.db.projects.find_one({'_id': ObjectId(thisProject)})   
    thisProjectTitle = thisProject['projectTitle']
    members = mongo.db.projects.find_one({'projectTitle':thisProjectTitle})['projectMembers']
    projectFiles = mongo.db.projects.find_one({'projectTitle':thisProjectTitle})['projectFiles']
    projectFilesNumber = thisProject['projectFiles']

    return render_template('project-hub.html',listOfUsers=listOfUsers, allCurrentUsernames=allCurrentUsernames, user=user, user_notifications=user_notifications, username=username, thisProject=thisProject, thisProjectTitle=thisProjectTitle, members=members,projectFiles=projectFiles,projectFilesNumber=projectFilesNumber,listOfProjectNames=listOfProjectNames ) 


@app.route('/add_comment/<thisProject>', methods=["GET", "POST"])
def add_comment(thisProject):
    user = (session["user"])   
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"] 
    thisProject = thisProject
    thisProjectTitle = mongo.db.projects.find_one({'_id':ObjectId(thisProject)})['projectTitle']
    
    projectHost = mongo.db.projects.find_one({'_id': ObjectId(thisProject)})['username']
    newComment = {
        'userComment': request.form.get('addComment'),
        'date': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
        'username': username
    }    

    mongo.db.projects.update_one({ '_id': ObjectId(thisProject)},{ '$push': { "comments": newComment }})
    mongo.db.users.update_one({ "username" : projectHost },{ '$push': {"notifications": "New comment on project: " + thisProjectTitle} })
    
    flash("Comment Added")
    return redirect(request.referrer)

@app.route('/new_notification/')
def new_notification():
    user = (session['user'])
    listOfUsers = mongo.db.users.find()

    user_notifications = mongo.db.users.find_one({'username':user}) 
    notification = "test new new 2 "

    mongo.db.users.update_one( { "username" : user },{ '$push':{'notifications' : {'$each':[notification], '$position':0}}})

    return redirect(request.referrer)



@app.route('/clear_notifications/')
def clear_notifications():
    user = (session['user'])
    listOfUsers = mongo.db.users.find()

    user_notifications = mongo.db.users.find_one({'username':user}) 

    mongo.db.users.update_one( { "username" : user },{ '$set':{'notifications' : []}})

    return redirect(request.referrer)


@app.route('/upload_project_files/<thisProject>/', methods=['GET', 'POST'])
def upload_project_files(thisProject):
    listOfUsers = mongo.db.users.find()
    allCurrentUsernames = mongo.db.users.distinct("username")
    listOfProjectNames = mongo.db.projects.distinct('projectTitle')
    user = (session["user"])   
    user_notifications = mongo.db.users.find_one({'username':user}) 
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"] 

    thisProject= mongo.db.projects.find_one({'_id': ObjectId(thisProject)})["_id"]
    thisProjectTitle = mongo.db.projects.find_one({'_id': ObjectId(thisProject)})["projectTitle"]
    members = mongo.db.projects.find_one({'projectTitle':thisProjectTitle})['projectMembers']
    projectFiles = mongo.db.projects.find_one({'projectTitle':thisProjectTitle})['projectFiles']
    projectFilesNumber = mongo.db.projects.count_documents({'projectFiles': projectFiles})
    
    if request.method == 'POST':
        if 'file1' not in request.files:
            return 'there is no file1 in form!'   
        file1 = request.files['file1']
        userChosenName = request.form.get('file-name')
        newFileName = userChosenName + "-" + user 
        path = os.path.join(app.config['UPLOAD_FOLDER_PROJECT'], file1.filename)
        ext = pathlib.Path(path).suffix
        newPath = os.path.join(app.config['UPLOAD_FOLDER_PROJECT'], newFileName + ext)
        file1.save(newPath)
        project_file_update = {
                'file': '/' + newPath,
                'displayName': request.form.get('file-name') + ext,
                'fileDescription': request.form.get('file-description'),
                'folder': request.form.get('file-folder'),
                'uploader': username,
                'date': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            }
        
        mongo.db.projects.update_one({'_id': ObjectId(thisProject)},{ '$push': { "projectFiles": project_file_update }}) 
        flash("Project file uploaded")

        return redirect(url_for('project_hub',listOfUsers=listOfUsers, allCurrentUsernames=allCurrentUsernames, user=user, user_notifications=user_notifications, username=username, thisProject=thisProject, thisProjectTitle=thisProjectTitle, members=members,projectFiles=projectFiles, projectFilesNumber=projectFilesNumber,listOfProjectNames=listOfProjectNames ) )
        
    return render_template('project-file-upload.html',listOfUsers=listOfUsers,user_notifications=user_notifications,thisProject=thisProject,thisProjectTitle=thisProjectTitle,allCurrentUsernames=allCurrentUsernames,listOfProjectNames=listOfProjectNames)   


@app.route('/messages/<usernameToContact>', methods=['GET', 'POST'])
def messages(usernameToContact):
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    usernameToContact=usernameToContact
    listOfUsers = mongo.db.users.find()
    allCurrentUsernames = mongo.db.users.distinct("username")
    listOfProjectNames = mongo.db.projects.distinct('projectTitle')
    user = (session["user"])
    user_notifications = mongo.db.users.find_one({'username':user})
    messages= mongo.db.messages.find({'members':[username,usernameToContact],'members':[usernameToContact,username] })


    if request.method == 'POST':
        
        
        conversation = {
            'username': username,
            'message': request.form.get('message'),
            'date': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        }
        
        convoExists1 = mongo.db.messages.count_documents({'members':[username,usernameToContact]})
        convoExists2 = mongo.db.messages.count_documents({'members':[usernameToContact,username]})

        if convoExists1 == 0 and convoExists2 == 0 :
            mongo.db.messages.insert_one({ 'members':[username,usernameToContact]})
            mongo.db.messages.insert_one({ 'members':[usernameToContact,username]})
            mongo.db.messages.update_one({'members':[username,usernameToContact]},{'$push':{'messages': conversation}})
            mongo.db.messages.update_one({ 'members':[usernameToContact,username]},{'$push':{'messages': conversation}})
            messages= mongo.db.messages.find({'members':[username,usernameToContact],'members':[usernameToContact,username] })
            notification = 'You have a new message from ' + username
            mongo.db.users.update_one( { "username" : usernameToContact },{ '$push':{'notifications' : {'$each':[notification], '$position':0}}})


            
        else:    
            mongo.db.messages.update_one({'members':[username,usernameToContact]},{'$push':{'messages': conversation}})
            mongo.db.messages.update_one({'members':[usernameToContact,username]},{'$push':{'messages': conversation}})

            messages= mongo.db.messages.find({'members':[username,usernameToContact],'members':[usernameToContact,username] })
            notification = 'You have a new message from ' + username
            mongo.db.users.update_one( { "username" : usernameToContact },{ '$push':{'notifications' : {'$each':[notification], '$position':0}}})
               
        
        return render_template('messages.html',listOfUsers=listOfUsers, allCurrentUsernames=allCurrentUsernames, listOfProjectNames=listOfProjectNames, user_notifications=user_notifications,messages=messages,username=username,usernameToContact=usernameToContact )
    
    
    
    

    return render_template('messages.html',listOfUsers=listOfUsers, allCurrentUsernames=allCurrentUsernames, listOfProjectNames=listOfProjectNames, user_notifications=user_notifications,messages=messages,username=username,usernameToContact=usernameToContact )


@app.route('/convo_list/')
def convo_list():  
    listOfUsers = mongo.db.users.find()
    allCurrentUsernames = mongo.db.users.distinct("username")
    listOfProjectNames = mongo.db.projects.distinct('projectTitle')
    user = (session["user"])
    users = mongo.db.users.find()
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"] 
    user_notifications = mongo.db.users.find_one({'username':user})
    myConversations = mongo.db.messages.find({'members': username})

    return render_template('convo-list.html',listOfUsers=listOfUsers,allCurrentUsernames=allCurrentUsernames,listOfProjectNames=listOfProjectNames,user_notifications=user_notifications,myConversations=myConversations, username=username,users=users ) 


@app.route('/contact/<usernameToContact>', methods=['GET', 'POST'])
def contact(usernameToContact):
    listOfUsers = mongo.db.users.find()
    allCurrentUsernames = mongo.db.users.distinct("username")
    listOfProjectNames = mongo.db.projects.distinct('projectTitle')
    user = (session["user"])
    user_notifications = mongo.db.users.find_one({'username':user})
    usernameToContact=usernameToContact
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"] 
    selectedUser= mongo.db.users.find_one({'username':usernameToContact})  
    conversationExists = mongo.db.messages.find({'members':[username,usernameToContact],'members':[usernameToContact,username] })

    if conversationExists:
        messages= mongo.db.messages.find({'members':[username,usernameToContact],'members':[usernameToContact,username] })

        return redirect(url_for('messages', selectedUser=selectedUser, listOfUsers=listOfUsers, user=user, user_notifications=user_notifications,allCurrentUsernames=allCurrentUsernames,listOfProjectNames=listOfProjectNames, usernameToContact=usernameToContact, username=username, messages=messages))
    
    else:
        if request.method == 'POST':
            
            
            conversation = {
                'username': username,
                'message': request.form.get('message'),
                'date': datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            }
            
            convoExists1 = mongo.db.messages.count_documents({'members':[username,usernameToContact]})
            convoExists2 = mongo.db.messages.count_documents({'members':[usernameToContact,username]})

            if convoExists1 == 0 and convoExists2 == 0 :
                mongo.db.messages.insert_one({ 'members':[username,usernameToContact]})
                mongo.db.messages.insert_one({ 'members':[usernameToContact,username]})
                mongo.db.messages.update_one({'members':[username,usernameToContact]},{'$push':{'messages': conversation}})
                mongo.db.messages.update_one({ 'members':[usernameToContact,username]},{'$push':{'messages': conversation}})
                messages= mongo.db.messages.find({'members':[username,usernameToContact],'members':[usernameToContact,username] })

                notification = 'You have a new message from ' + username
                mongo.db.users.update_one( { "username" : usernameToContact },{ '$push':{'notifications' : {'$each':[notification], '$position':0}}})


                
            else:    
                mongo.db.messages.update_one({'members':[username,usernameToContact]},{'$push':{'messages': conversation}})
                mongo.db.messages.update_one({'members':[usernameToContact,username]},{'$push':{'messages': conversation}})

                messages= mongo.db.messages.find({'members':[username,usernameToContact],'members':[usernameToContact,username] })

                notification = 'You have a new message from ' + username
                mongo.db.users.update_one( { "username" : usernameToContact },{ '$push':{'notifications' : {'$each':[notification], '$position':0}}})
                
            
            flash('Message Sent')

            

            return redirect(url_for('messages', selectedUser=selectedUser, listOfUsers=listOfUsers, user=user, user_notifications=user_notifications,allCurrentUsernames=allCurrentUsernames,listOfProjectNames=listOfProjectNames, usernameToContact=usernameToContact, username=username, messages=messages))
    

    return render_template('contact.html',listOfUsers=listOfUsers, allCurrentUsernames=allCurrentUsernames, listOfProjectNames=listOfProjectNames, user_notifications=user_notifications,usernameToContact=usernameToContact )        

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)