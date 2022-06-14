# Project Mission Statement
I developed harmonise as a social media platform aimed at making collaboration between musicians more streamlined and providing a focused community for like-minded individuals. My main aims were creating a platform where users could create and advertise musical projects that they were interested in, to individuals that are suited and relevant to their needs. The app would then provide a simple way to communuicate with other project members both individually and as a group, and allow them to share important files and other documents such as sheet music and MP3's that are relevant to their projects. 

---

![Website Mockup](/static/readme-files/all-devices-black.png)

---

# Deployed Project

The deployed site can be viewed [Here](http://www.harmonise-app.co.uk/).

As much of the websites functionality revloves around interacting with other users I have created two accounts for you to use for marking purposes. These each have one project created, and are a member of the others project for you to test the project hub section. You can also test the messages function and other features that require two accounts.
Please feel free to also create your own account from scratch; I just thought this would save a little time and make the marking process more streamlined.

## Demo Log in details

Username: codeinstitute1
Password: password

Username: codeinstitute2
Password: password

# Project Overview

The purpose of this project is to develop and present my skills in the follow areas:

1. Handling data
      - Build a database structure backed by flask that allows me to create, read, update and delete user data in a manner useful to my project.

2. User functionality
      - Develop functionality for users to create, read, update and delete data records on the site.

3. Use of technologies
      - Make use of an array of technologies including custom HTML, CSS and Javascript to develop the fontend, and Python for the back-end.    

4. Documentation
      - Create a README.md document explaining the purpose of the project and its benefit to users.

5. Version control
      - Use Git and Github for version control of my code.

6. Deployment
      - Use the hosting platform Heroku to deploy and host my final code.

## A note on relational vs non-relational databases     

I have created this project using MongoDb as my database. I chose to use MongoDb due to comments in the course material stating that for something like a social media platform, where the database content is very varied and changing, that a non-relational databse might be the best choice.
Although MongoDb is technically a non-relational database, I have used it in a relational manner, where all data associated (messages, projects, files) with a user is tied to their unique username. I spoke to the assessments team to check that this is okay, and they have confirmed to me that it is.

My database is structured into 3 collections. 

- the User collection stores all the data about a user as a document. The document contains all of their biographical and instrument information, personal details, following/followers list, and the link to their profile photo.

![User Collection](/static/readme-files/features/user-collection.png)

- The projects collection creates a new document for each project that is created. This document stores all the information about the project, the list of outstanding user applications, the project members, an array of all of the comments in the group chat, and links and data for all of the project files.
![Projects Collection](/static/readme-files/features/projects-collection.png)

- The Messages collection creates a new document for each conversation between two usernames. The messages are then all stored within this document as objects, containing the message and date data.
![Messages Collection](/static/readme-files/features/messages-collection.png)

All of the information between these collections are connected using the users username, which is a unique identifier.
                          
##  User Experience (UX)
---
### User Stories

- As a first time user I want to:

1. Quickly understand the purpose and layout of the site.
2. Understand how to create a profile and navigate the sites functionality.
3. Be able to customise my profile.
4. Be able to view other users profiles and interact with them.

- As a returning visitor I want to:

1. Be able to create and edit musical projects and advertise them to relevant site members.
2. Be able to find projects relevant to my skills and interests, and then apply to join them.
3. Be able to communicate with other members/users on the site.
4. Be able to share sheet music, MP3's and other relevant files to project members.
5. Be able to view other members personal profiles, and follow them to build a community.
6. Be notified of any actions on the site relevant to me (direct messages, new followers etc.)

- As a frequent visitor I want to:

1. Be able to delete projects and content that I have created.
2. Be able to remove my account and all associated data.

## 1. Strategy
---
## Project purpose
- To provide a streamlined platform for musicians to communicate and collaborate.
- create a tool for useful files to be easilly shared between users.
- create a social environment for like-minded musicians to be able to discover each other based on a variety of parameters (instrument, genre, location etc.) and also follow one anothers accounts to build a community of useful contacts.

## 2. Scope
---
- I wanted a simple and intuitive user experience.
- I wanted all content to be displayed in a slick and aesthetic manner.
- I wanted to incorporate many aspects common to social media platforms (direct messaging, groups, followers, search function, notifications, personal profiles etc.)
- I wanted an intuitive interface to upload and securely store project files in the cloud.
- I wanted a slick looking experience that functions well on a variety of screen sizes.

## 3. Structure
---
- The site features a comprehensive navigation bar which allows the user to easilly traverse the entire sites functionality.
- The sites notification system is built into the navbar with a icon that updates according to new notifications.
- The sites functionality is split accross several drop-down tabs:

    1. An autocompleting search bar to allow the user to find another user by their username
    2. Notifications drop-down that updates with alerts of virtually any action on the website that is of concern to the user (direct message, comment, follow, applications to a project, the results of an application made by the user, new followers etc.)
    The notifications all feature contextual icons to quickly convey what type it is, and also act as a link to instantly traverse the user to the appropriate location.
    3. A projects tab which allows the user to create new projects, browse other projects (either all of them, or only those relevant to them), manage your own projects, and view projects that the user is a member of. Any project that a user is a member of will allow the user to view the 'project hub' for that project, allowing them to view all other members, important information about the project, a group chat, and have the ability to both upload or download projects files.
    4. An account section which allows the user access to their own profile in which they can change and update their information, change their profile picture, and also a 'delete profile' tab which allows the user to remove their profile and all data about them from the site.
    5. A users tab which provides the ability to either view all site members, or view only those fitting certain search criteria.
    6. A connections tab which displays the profiles and information of accounts which are either following or followed by the user.
    7. A messages tab which displays a list of all conversations the user has, and allows access to a direct messaging function.

## 4. Skeleton 
---

### Wireframes

Wire frames for the site were generated using Figma, and can be viewed [here](/static/readme-files/wireframes/harmonise-wireframes.png)

## 5. Surface 
---

### Colour Scheme

The main colors used in developing the site are #39583a green for the navbar and footer. #395758 teal for the buttons and links, and #583957 purple for much of the project panels and collapsibles. I used [canva's complimentary color wheel](https://www.canva.com/colors/color-wheel/) to choose these colors.

### Typography

I used 'Open Sans' for all of the heading throughout the site, 'Source Serif Pro' for the logo and 'Helvetic Neue'. These were backed up by 'Sans Serif' and imported from [Google Fonts](https://fonts.google.com/)


### Imagery and Theme

Imagery used throughout the site acts mainly as a backdrop for the page content. I stuck closely with the music theme, making use of images of musicians, and sheet music throughout. All of the imagery was taken from Unsplash and is credited at the end of this README.

## 5. Features 
---
## General
---

### The Navbar

The site features a very feature packed navbar that quickly allows the user access to all areas of the website.

![Desktop Navbar](/static/readme-files/features/navbar-min.png)

The links on the navbar are grouped by category and expand into dropdowns to allow navigation to wherever the user desires.

On smaller screens the navbar collapses into a vertical nav on the left of the screen. All the features and functionality of the full navbar is retained.

![Mobile Navbar](/static/readme-files/features/sidenav-min.png)

### Notifications

The navbar features a notifications dropdown that is updated when virtually any event of significance to the user happens. The notification is then contextually displayed based on what it is notifiying using an appropriate icon to quickly inform the user of what is being conveyed. 
All of the notifications are also links to instantly take the user to the correct location. For example, a message notificaition informs the user that they have received a message from a certain username. This is displayed with an icon of a letter, and when clicked will take the user to the correct direct message chat.

Examples of notifications created by the site:

- Applications to your project
- Results of an application made by the user
- Direct messages received
- A comment on a project the user is in
- being removed by a project host from a project
- A new follower

The notifications display inside a scrollable div, and the current number of notifications is displayed next to the bell icon.
If a user wants to delete all of their notifications this can be done so by clicking the delete notification button located either at the end of the list on desktop, or at the top of the modal on mobile.

![Desktop Notifications](/static/readme-files/features/notifications-min.png)

This same notifications system is also available on smaller screens and is displayed instead inside a modal.

![Mobile Notifications](/static/readme-files/features/sidenav-notifications-min.png)


### Username Search Bar

Both the desktop and side-navbar are also equipped with a search bar that links to other users profiles. The search bar draws from a datalist of all current usernames on the platform, and makes suggestions as the user types.
The search bar is non-case sensitive, and strips off any whitespace that the user may add.
If a username that doesn't exist on the site is entered, the user is taken to their own profile and informed that no such user exists.

![Desktop Search Bar](/static/readme-files/features/navbar-search-min.png)


## Register/Login Page
---
### Password Confirmation
The register profile form is equipped with a password check to ensure the user enters their intended password.

![confirm password](/static/readme-files/features/confirm-password-min.png)

### Instruments and Genres Dropdown

When the user creates an account they are asked for all information that is relevant to their experience on the website. This includes instruments and genres that they play.
These can be selected through the dropdown lists at the bottom of the form.

![Instrument and Genre select](/static/readme-files/features/instruments-dropdown-min.png)


## Profiles Pages
---
### User Bio Tabs
At the top of each users profile page is a section which displays all the relevant information about the user. This includes their bio, instruments and genres played, their followers/following stats, and their number of projects. The biographic section can be selected via the tabs on the collapsible container.

![Profile information](/static/readme-files/features/profile-min.png)


### Edit Profile Information
By default the instruments and genres tabs are pre-populated with the information entered during the registration phase, but the bio by default displays a message prompting the user to write some information about themselves.
Upon opening the 'edit profile' page, all of the users current details are automatically pre-populated into the form.
All of these details can be altered by clicking the edit profile button, which allows the user to change all of the information added during sign-up, along with their bio.

![Edit Profile](/static/readme-files/features/edit-profile-min.png)


### Change Profile Picture
By default all users have the same profile pictures of a generic silhouette. This can be changed to their own custom upload by clicking the 'Upload Photo' button.

The user is then taken to a form where they can select any .JPG .JPEG or .PNG file that they want. This image is then uploaded to an Amazon S3 bucket, before being streamed back to the website by ImageKit, which compresses the file to improve performance. 
Each time a new profile photo is uploaded the previous photo in Amazon S3 is overwritten, and the ImageKit server cache is purged. The new photo then displays a short while later.

![Upload Profile Image](/static/readme-files/features/change-profile-pic-min.png)

### Follow/Unfollow
The website features a followers system to allow the user to save other users of interest. When visiting another users page, the user is presented with the option to either follow or unfollow them depending on their current following status.
These users can then be viewed through the 'My Connections' section, which displays all of the users who you either follow, or are followed by.

![Follow Button](/static/readme-files/features/follow-user-min.png)
![Unfollow Button](/static/readme-files/features/unfollow-user-min.png)
![list of followers](/static/readme-files/features/following-min.png)

### Contact Button
The profile page also allows users to contact eachother by pressing the 'contact' button.
When pressed the user is taken to a direct message panel. If a message is sent the recipient is alerted and a new conversation tab is generated in the conversations list page.

![Conversations list](/static/readme-files/features/convo-list-min.png)

### Users Projects Display
At the bottom of a users profile page, all of their projects are displayed in cards. These cards provide information about the project, the ability to apply to the project, a button to view the project hub of that project should you already be a member, or a button to manage the project if you are the host.

![Profile projects display](/static/readme-files/features/profile-projects-min.png)

## Create Project Page
---
### Create a Project
By clicking the 'Create a Project' link in the 'projects' tab, the user is taken to a form where they can create a new project.
The form allows them to input information regarding instruments and genres desired, a title, a description, a location, email and other various parameters. 
Once the project has been created it will display on the website to other users, who can then apply to join.

![Create a project](/static/readme-files/features/create-project-min.png)


### Apply to a Project
Users are able to apply to join a project by pressing the 'apply' button on any project that they are not a member of. This then takes them to a form where they can write a message to the host and select which instrument and genre of the ones asked for that they are applying for.
Once the application is submitted the host of the project is informed.

![Apply to project](/static/readme-files/features/apply-project-min.png)

## Manage Project Page
---
The host is able to manage many aspects of any of their projects, either by navigating to the 'my projects' section, or by clicking the 'manage' button on any of their project cards.

### Edit Project Information
The manage projects page allows the user to update any of the information about the project. This will then be reflected to all users who view the project, members or not.
The user can also choose to delete the entire project after a confirmation modal is also clicked.
This will delete the project along with all commments, member information or project files associated with it.
The files are also purged from the Amazon S3 bucket when a project is deleted.

![Edit project](/static/readme-files/features/manage-project-min.png)


### View Project Members
In the manage project page all current members of the project can be viewed, along with some information about their role in the project. 
The host can also choose to kick a member, which will also notify them
of their removal.

![Kick member](/static/readme-files/features/project-members-min.png)

### View Project Applications
The user is also able to view all outstanding applications to a project, along with the role applied for, and their message written during the application process. A decision can then be made, and the applicant will be notified of the outcome.

![View project applications](/static/readme-files/features/view-application-min.png)

## Project Hub Page
---
Once a user becomes a member of the project they gain access to the 'project hub'. This is an area which displays all the information about the project, a group chat comment system, and a file sharing section.

![Project Hub](/static/readme-files/features/project-hub-min.png)

### Project Information and Members
This panel displays all of the current members of a project and their instrument. It also allows quick access to the users profile by clicking their name. If you are the host you are also able to kick members by pressing the 'remove from project' button.

### Comments Panel
The project hub features a group chat comment system, that allows all of the user to communicate with each-other. Messages can be entered in the text area and submtted to the chat using the button. This will then display the comment alongside your username, which links to your profile, and the time the comment was posted. The date of the comment has been formatted to be more readable ('just now', '1 day ago', '2 weeks ago').
Depending on your role in the group the comment usernames are also color coded, with the host being displayed in green with a star icon next to any of their messages, to more quickly identify important comments.
The scrollable comments div is also automatically loaded at the bottom to always display the most recent comment.

### File Upload/Storage System
At the bottom of the project hub is a file sharing and storage section. This allows users to upload files through an upload form where they can choose a file name, a preset classification e.g. 'image','audio' etc. And also write a message to be linked to their file.
This is then uploaded to Amazon S3, and displayed in the appropriate dropdown folder. The files can then be viewed, downloaded or if you are the uploader, deleted.

![File Upload](/static/readme-files/features/upload-files-min.png)

![File Storage](/static/readme-files/features/file-storage-min.png)

## Projects I'm In Page
---
This page provides quick access to all projects that you are a member of, along with icons displaying the number of members and comments.

![Projects im in](/static/readme-files/features/projects-im-in.png)

## Browse Projects Pages
---
### Browse All/Relevant Projects
These tabs allow the user to either view all projects on the website...

![View all projects](/static/readme-files/features/all-projects-min.png)

Or to view a filtered list of only projects relevant to the users played instruments.
The relevant instruments are highlighted on the project card to quickly convey the reason he project is suitable to the user.

![Relevant Projects](/static/readme-files/features/relevant-projects-min.png)

## Other Users Page
---
### View All Users
The all users page displays all current users on the website, along with their profile photo, username which links to their profile, and a collapsible dropdown displaying their instruments, genres and location.

![View all users](/static/readme-files/features/all-users-min.png)

### Search Users by Parameter
You are also able to filter users on the website by specific parameters should you want to find a person suitable for your needs. e.g. a classical violinist from London. 

Parameters can be entered into the form, and then all users who meet your critera will be displayed with the relevant information highlighted in green.
The city parameter is non-case sensitive and strips off white space like the user search feature.

![Search user form](/static/readme-files/features/search-users-min.png)

![Search User Results](/static/readme-files/features/user-search-results-min.png)

## Messages Pages
---
### Conversation List
The conversations list page displays all of your active conversations along with a count for the number of messages exchanged.
Clicking the link takes you to the messages page.

![Conversations panel](/static/readme-files/features/convo-list-min.png)

### Direct Messaging
This section of the website allows for direct messaging between users. It operates much like the comments feature, allowing direct messages to be exchanged. It loads at the bottom of the scrollable div to always display the most recent message.

Once a message is sent the recipient is notified that you have contacted them.

![Messages](/static/readme-files/features/direct-messages-min.png)

## Delete Profile
---
If you no longer wish to be a site member you can remove your profile from the system through the 'Delete Profile' page.
After confirming your decision your profile will be wiped clean from the site.

This includes:
- Removing you from all projects
- Removing you from all followers/following lists
- Deleting all of your projects and the files within them from the S3 bucket
- Deleting your profile image from the server

Any messages you had with other users are retained, but when they click the link to your profile within the messenger panel, they are informed that your account no longer exists.

![Delete Profile](/static/readme-files/features/delete-account-min.png)

## Technologies Used 
---

### Languages Used

* HTML5
* CSS3
* Javascript
* Python

### Framework, Software & Libraries Used

1. [Materialize](https://materializecss.com/):
      * Materialize was used to quickly generate a layout for the navbar and some elements of the site, before being overwritten by custom CSS.

2. [Google Fonts](https://fonts.google.com/):
   * Google fonts was used to import the fonts used throughout the site..

3. [Font Awesome](https://fontawesome.com/):
   * Font Awesome was used to provide icons for various elements on the site.

4. [Git](https://git-scm.com/):
   * Git was used for version control to backup my project. I did this through terminal commands to commit to Git and push externally to GitHub.

5. [GitHub](https://github.com/):
   * GitHub was used to store all of my project code after being pushed from Git.

6. [Figma](https://figma.com/):
      * The Figma free trial was used to generate my wireframes to guide my design process.

7. [Real Favicon Generator](https://realfavicongenerator.net):
   * Real Favicon Generator was used to create a favicon.ico file.

8. [Website Mockup Generator](https://websitemockupgenerator.com)
   * Website Mockup Generator was used to create the website mockup at the start of this README.

9.  [JQUERY](https://jquery.com)  
      * JQUERY was used throughout the process of creating my Javascript code.

10. [lighthouse](https://developers.google.com/web/tools/lighthouse)
      * Lighthouse was used to assess the performance of the project.

11. [Wave](https://wave.webaim.org/)
      * Wave was used to assess the accessibility of the project.

12. [ImageKit](https://imagekit.io/)
      * Image kit was used to compress and serve images stored in the Amazon S3 server to increase performance.

13. [Amazon S3](https://aws.amazon.com/s3/)
      * Amazon S3 was used to store all uploaded user files.    

14. [Flask](https://flask.palletsprojects.com/en/2.1.x/)
      * Flask was used as the framework to create my project.        

15. [MongoDb](https://mongodb.com)
      * MongoDb was used as my database to store all data about users, projects and messages. This information was then all related to eachother using ID and username parameters.

16. [Pymongo](https://pymongo.readthedocs.io/en/stable/)
      * Pymongo was used to interact with the MongoDb database. 

17. [image compressor](https://imagecompressor.com/)
      * Imagecompressor was used to compress all of my static files to improve performance.

18. [Heroku](https://heroku.com/)
      * Heroku was used to host my project.                      
             

## Further Testing
---
Details of testing can be found in the [Testing](/testing.md) file.

## Deployment
---

### **Heroku**
  Before you can deploy your app to Heroku, initialize a local Git repository and commit your application code to it.

  #### **Create a Heroku Remote**
  Git remotes are versions of your repository that live on other servers. You deploy your app by pushing its code to a special Heroku-hosted remote that’s associated with your app.

  #### **For a New App**:

  The heroku create CLI command creates a new empty application on Heroku, along with an associated empty Git repository. If you run this command from your app’s root directory, the empty Heroku Git repository is automatically set as a remote for your local repository.

      heroku create -a harmonise

  You can use the "git remote -v" command to confirm that a remote named heroku has been set for your app.

  #### **For an Existing App**:

  Add a remote to your local repository with the heroku git:remote command. All you need is your Heroku app’s name:

      heroku git:remote -a harmonise

  #### **Deploy Your Code**:
  To deploy your app to Heroku, use the "git push" command to push the code from your local repository’s main branch to your heroku remote. For example:

      git push heroku main

  Use this same command whenever you want to deploy the latest committed version of your code to Heroku.

  Heroku only deploys code that you push to the master or main branches of the remote. Pushing code to another branch of the heroku remote has no effect.

  ---

  ### **Forking the GitHub Repository**
  By forking the GitHub Repository you make a copy of the original repository on your GitHub account to view and/or make changes without affecting the original repository.

  You can do this by completing the following steps:

  1. Log in to GitHub and locate the GitHub Repository
  2. At the top of the Repository (not top of page) just above the "Settings" Button on the menu, locate the "Fork" Button.
  3. You should now have a copy of the original repository in your GitHub account.

  ---

  ### **Making a Local Clone**:
  1. Log in to GitHub and locate the GitHub Repository
  2. Under the repository name, click "Clone or download".
  3. To clone the repository using HTTPS, under "Clone with HTTPS", copy the link.
  4. Open Git Bash
  5. Change the current working directory to the location where you want the cloned directory to be made.
  6. Type git clone, and then paste the URL you copied in Step 3.

    $ git clone https://github.com/Luketedwards/harmonize.git


 # Credits

## Code 
* Materialize was used to generate the initial layout of my UI, and some of their components (dropdown menus, container with tabs) was used in the final version of the project.

## Content

### Images
---
All images on the site were sourced from [Unsplash](https://unsplash.com)

* [Sheet Music Image for Project Upload](https://unsplash.com/photos/2zHGVCrdxHw)
* [Delete Account Background Image](https://unsplash.com/photos/BwMcYuHI9OI)
* [Messages Background Image](https://unsplash.com/photos/VPTSnznXtyQ)
* [Log In Background Image](https://unsplash.com/photos/qYHyn4ztNkc)
* [Project Hub Background Image](https://unsplash.com/photos/pH88tHG-1yw)
* [All Users Background Image](https://unsplash.com/photos/ECI6l_JwOew)
* [Upload Profile Photo Background Image](https://unsplash.com/photos/ECI6l_JwOew)
* [Register Background Image](https://unsplash.com/photos/i3yZJaQgR7k)

## Acknowledgements
---

* My mentor Rahul Lakhanpal for his support and invaluable advice throughout my project.

* Code Institute for their excellent learning platform and student support.

* [W3C Schools](https://www.w3schools.com/) and [Stack Overflow](https://stackoverflow.com/) for being valuable resources when I encountered problems in my code. 
