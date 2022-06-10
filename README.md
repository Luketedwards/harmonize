# Project Mission Statement
I developed harmonise as a social media platform aimed at making collaboration between musicians more streamlined and providing a focussed community for likeminded individuals. My main aims were at creating a platform where users could advertise musical projects that they were interested in creating, to individuals suited to their goal. The app would then provide a simple way to communuicate with other project members both individually and as a group, and allow them to share files and other documents relevant to their projects. 

---

![Website Mockup]()


---

# Walkthrough Video - Click To Watch!

[![Harmonise Demo]()]( )

---
# Deployed Project

The deployed site can be viewed [Here](http://www.harmonise-app.co.uk/).

##  User Experience (UX)
---
### User Stories

- As a first time user I want to:

1. Quickly understand the purpose and layout of the site.
2. Understand how to create a profile and navigate the sites functionality.
3. Be able to customise my profile.

- As a returning visitor I want to:

1. Be able to create and edit musical projects and advertise them to relevant site members.
2. Be able to find projects relevant to my skills and interests, and then apply to join them.
3. Be able to communicate with other members/users on the site.
4. Be able to share sheet music, MP3's and other relevant files to project members.
5. Be able to view other members personal profiles, and follow them to build a community.
6. Be notified of any actions on the site relevant to me (direct messages, new followers etc.)

## 1. Strategy
---
## Project purpose
- To provide a streamlined platform for musicians to communicate and collaborate.
- create a tool for useful files to be easilly shared between users.
- create a social environment for likeminded musicians to be able to discover each other based on a variety of parameters (instrument, genre, location etc.) and also follow one anothers accounts.

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
    2. Notifications drop-down that updates with alerts of virtually any action on the website that is of concern to the user (direct message, comment, follow, apllications to a project, the results of an application made by the user, new followers etc.)
    The notifications all feature contextual icons to quickly convey what type it is, and also act as links to instantly traverse the user to the appropriate location.
    3. A projects tab which allows the user to create new projects, browse other projects (either all of them, or only those relevant to them), manage your own projects, and view projects that the user is a member of. Any project that a user is a member of will allow the user to view the 'project hub' for that project, allowing them to view all other members, important information about the project, a group chat, and the ability to both upload or download projects files.
    4. An account section which allows the user access to their own profile in which they can change and update their information, and change their profile picture, and also a 'delete profile' tab which allows the user to remove their profile and all data about them from the site.
    5. A users tab which provides the ability to either view all site members, or view only those fitting certain search criteria.
    6. A connections tab which displays the profiles and information of accounts which are either following or followed by the user.
    7. A messages tab which displays a list of all conversations the user has, and allows access to a direct messaging function.

## 4. Skeleton 
---

### Wireframes

Wire frames for the site were generated using Figma, and can be viewed below.

- [Register Page]()
- [Login Page]()
- [User Profile]()
- [Other Users]()
- [Manage Project]()
- [Create a Project]()
- [Project Hub]()
- [Messages page]()

## 5. Surface 
---

### Colour Scheme

The main colors used in developing the site are a vivid green for the navbar, footer and buttons, yellow for much of the project panels.

### Typography

I used 'Open Sans' for all of the heading throughout the site, 'Source Serif Pro' for the logo and 'Helvetic Neue'. These were backed up by 'Sans Serif'.


### Imagery and Theme

Imagery used throughout the site acts mainly as a backdrop for the page content. I stuck closely with the music theme, making use of images of musicians, and sheet music throughout. 

## 5. Features 
---
### General
---

#### The Navbar

The site features a very feature packed navbar that quickly allows the user access to all areas of the website.

![Desktop Navbar](/static/readme-files/features/navbar-min.png)

The links on the navbar are grouped by category and expand into dropdowns to allow navigation to wherever the user desires.

On smaller screens the navbar collapses into a vertical nav on the left of the screen. All the features and functionality of the full navbar is retained.

![Mobile Navbar](/static/readme-files/features/sidenav-min.png)

#### Notifications

The navbar features a notifications dropdown that is updated when virtually any event of significance to the user happens. The notification is then contextually displayed based on what it is notifiying using an appropriate icon to quickly inform the user of what is being conveyed. 
All of the notifications are also links to instantly take the user to the correct location. For example, a message notificaition informs the user that they have received a message from a certain username. This is displayed with an icon of a letter, and when clicked will take the user to the correct direct message chat.

Examples of notifications created by the site:

- Applications to your project
- Results of an application made by the user
- Direct message received
- A comment on a project the user is in
- being removed by a project host from a project
- A new follower

The notifications display inside a scrollable div, and the current number of notifications is displayed next to the bell icon.
If a user wants to delete all of their notifications this can be done so by clicking the delete notification button.

![Desktop Notifications](/static/readme-files/features/notifications-min.png)

This same notifications system is also available on smaller screens and is displayed instead inside a modal.

![Mobile Notifications](/static/readme-files/features/sidenav-notifications-min.png)


#### Username Search Bar

The both the desktop and side-navbar are also equipped with a search bar that links to other users profiles. The search bar draws from a datalist of all current usernames on the platform, and makes suggestions as the user types.
The search bar is non-case sensitive, and strips off any whitespace that the user may add.
If a username that doesn't exist on the site is entered, the user is taken to their profile and informed that no such user exists.

![Desktop Search Bar](/static/readme-files/features/navbar-search-min.png)


### Register/Login Page
---
#### Password Confirmation
The register profile form is equipped with a password check to ensure the user enters their intended password.

![confirm password](/static/readme-files/features/confirm-password-min.png)

#### Instruments and Genres Dropdown

When the user creates an account their are asked for all information that is relevant to their experience on the website. This includes instruments and genres that they play.
These can be selected through the dropdown lists at the bottom of the form.

![Instrument and Genre select](/static/readme-files/features/instruments-dropdown-min.png)


### Profiles Pages
---
#### User Bio Tabs
At the top of each users profile page is a section which displays all the relevant information about the user. This includes their bio, instruments and genres played, their followers following stats, and their number of projects. The biographic section can be selected via the tabs on the collapsible container.

![Profile information](/static/readme-files/features/profile-min.png)


#### Edit Profile Information
By default the instruments and genres tabs are pre-populated with the information entered during the registration phase, but the bio by default displays a message prompting the user to write some information about themselves.
All of these details can be altered by clicking the edit profile button, which allows the user to change all of the information added during sign-up, along with their bio.

![Edit Profile](/static/readme-files/features/edit-profile-min.png)


#### Change Profile Picture
By default all users have the same profile pictures of a generic silhouette. This can be changed to their own custom upload by clicking the 'Upload Photo' button.

The user is then taken to a form where they can select any .JPG .JPEG or .PNG file that they want. This image is then uploaded to an Amazon S3 bucket, before being streamed back to the website by ImageKit, which compresses the file to improve performance. 
Eachtime a new profile photo is uploaded the previous photo in Amazon S3 is overwritten, and the ImageKit server cache is purged. The new photo then displays a short while later.

![Upload Profile Image](/static/readme-files/features/change-profile-pic-min.png)

#### Follow/Unfollow
The website features a followers system to allow the user to save other users of interest. When visiting another users page, the user is presented with the option to either follow or unfollow them depending on their current following status.
These users can then be viewed through the 'My Connections' section, which displays all of the users who you either follow, or are followed by.

![Follow Button](/static/readme-files/features/follow-user-min.png)
![Unfollow Button](/static/readme-files/features/unfollow-user-min.png)
![list of followers](/static/readme-files/features/following-min.png)

#### Contact Button
The profile page also allows users to contact eachother by pressing the 'contact' button.
When pressed the user is taken to a direct message panel. If a message is sent the recipient is alerted and a new conversation tab is generated in the conversations list page.

![Conversations list](/static/readme-files/features/convo-list-min.png)

#### Users Projects Display
At the bottom of a users profile page, all of their projects are displayed in cards. These cards provide information about the project, the ability to apply to the project, a button to view the project hub of that project should you already be a member, or a button to manage the project is you are the host.

![Profile projects display](/static/readme-files/features/profile-projects-min.png)

### Create Project Page
---
#### Create a Project
By clicking the 'Create a Project' link in the 'projects' tab, the user is taken to a form where they can create a new project.
The form allows them to input information regarding instruments and genres desired, a title, a description, a location an email and other various parameters. 
Once the project has been created it will display on the website to other users, who can then apply to join.

![Create a project](/static/readme-files/features/create-project-min.png)


#### Apply to a Project
Users are able to apply to join a project by pressing the 'apply' button on any project that they are not a member of. This then takes them to a form where they can write a message to the host and select which instrument and genre of the ones asked for that they are applying for.
Once the application is submitted the host of the project is informed.

![Apply to project](/static/readme-files/features/apply-project-min.png)

### Manage Project Page
---
The host is able to manage many aspects of any of their projects, either by navigating to the 'my projects' section, or by clicking the 'manage' button on any of their project cards.

#### Edit Project Information
The manage projects page allows the user to update any of the information about the project. This will then be reflected to all users who view the project, members or not.
The user can also choose to delete the entire project after a confirmation modal is also clicked.
This will delete the project along with all commments, member information or project files associated with it.
The files are also purged from the Amazon S3 bucket when a project is deleted.

![Edit project](/static/readme-files/features/manage-project-min.png)


#### View Project Members
In the manage project page all current members of the project can be viewed, along with some information about their role in the project. 
The host can also choose to kick a member, which will also notify them.

![Kick member](/static/readme-files/features/project-members-min.png)

#### View Project Applications
The user is also able to view all outstanding applications to a project, along with the role applied for, and their message written during the application process. A decision can then be made, and the applicant will be notified of the outcome.

![View project applications](/static/readme-files/features/view-application-min.png)

### Project Hub Page
---
Once a user becomes a member of the project they gain access to the 'project hub'. This is an area which displays all the information about the project, a group chat comment system, and a file sharing section.

![Project Hub](/static/readme-files/features/project-hub-min.png)

#### Project Information and Members
This panel displays all of the current members of a project and their instrument. It also allows quick access to the users profile by clicking their name. If you are the host you are also able to kick members by pressing the 'remove from project' button.

#### Comments Panel
The project hub features a group chat comment system, that allows all of the user to communicate with eachother. Messages can be entered in the text area and submtted to the chat using the button. This will then display the comment alongside your username, which links to your profile, and the time the comment was posted. The date of the comment has been formatted to be more readable ('just now', '1 day ago', '2 weeks ago').
Depending on your role in the group the comment usernames are also color coded, with the host being displayed in green with a star icon next to any of their messages, to more quickly identify important comments.
The scrollable comments div is also automatically loaded at the bottom to always display the most recent comment.

#### File Upload/Storage System
At the bottom of the project hub is a file sharing and storage section. This allows users to upload files through an upload form where they can choose a file name, a preset classification e.g. 'image','audio' etc. And also write a message to be linked to their file.
This is then uploaded to Amazon S3, and displayed in the appropriate dropdown folder. The files can then be viewed, downloaded or if you are the uploader, deleted.

![File Upload](/static/readme-files/features/upload-files-min.png)

![File Storage](/static/readme-files/features/file-storage-min.png)

### Projects I'm In Page
---
This page provides quick access to all projects that you are a member of, along with icons displaying the number of members and comments.

![Projects im in](/static/readme-files/features/projects-im-in.png)

### Browse Projects Pages
---
#### Browse All/Relevant Projects
These tabs allow the user to either view all projects on the website.

![View all projects](/static/readme-files/features/all-projects-min.png)

Or to view a filtered list of only projects relevant to the users played instruments.
The relevant instruments are also highlighted on the project card to quickly convey the suitability of the user.

![Relevant Projects](/static/readme-files/features/relevant-projects-min.png)

### Other Users Page
---
#### View All Users
The all users page displays all current users on the website, along with their profile photo, username which links to their profile, and a collapsible dropdown displaying their instruments, genres and location.

![View all users](/static/readme-files/features/all-users-min.png)

#### Search Users by Parameter
You are also able to filter users on the website by specific parameters should you want to find a person suitable for your needs. e.g. a classical violinist from London. 

Parameters can be entered into the form, and then all users who meet your critera will be diplayed with the relevant information highlighted in green.
The city parameter is non-case sensitive and strips off white space like the user search feature.

![Search user form](/static/readme-files/features/search-users-min.png)

![Search User Results](/static/readme-files/features/user-search-results-min.png)

### Messages Pages
---
#### Conversation List
The conversations list page displays all of your active conversations along with a count for the number of messages exchanged.
Clicking the link takes you to the messages page.

![Conversations panel](/static/readme-files/features/convo-list-min.png)

#### Direct Messaging
This sections of the website allows for direct messaging between users. It operates much like the comments feature, allowing direct messages to be exchanged. It loads at the bottom of the scrollable div to always display the most recent message.

Once a message is sent the recipient is notified that you have contacted them.

![Messages](/static/readme-files/features/direct-messages-min.png)

### Delete Profile
---
If you no longer wish to be a site member you can remove your profile from the system

## Technologies Used 
---

### Languages Used

* HTML5
* CSS3
* Javascript
* Python

### Framework, Software & Libraries Used

1. [Bootstrap 4.4.1](https://getbootstrap.com/):
      * Bootstrap was utilised to quickly build a responsive framework for the website, before being overwritten with a custom CSS stylesheet to add my own style.

2. [Google Fonts](https://fonts.google.com/):
   * Google fonts was used to import the fonts 'Lusitana' for the nav bar and headings, and 'Source Serif 4' for the body text. Both fonts were backed up by 'Sans-serif'.

3. [Font Awesome](https://fontawesome.com/):
   * Font Awesome was used to provide icons for the toggle buttons on the memory tips page.

4. [Git](https://git-scm.com/):
   * Git was used for version control to backup my project. I did this through terminal commands to commit to Git and push externally to GitHub.

5. [GitHub](https://github.com/):
   * GitHub was used to store all of my project code after being pushed from Git. Git hub pages was then used to deploy the project.

6. [Affinity Photo/Publisher](https://affinity.serif.com/en-gb/photo/):
      * Affinity software was used to create my poker chip buttons and favicon image.

7. [Figma](https://figma.com/):
      * The Figma free trial was used to generate my wireframes to guide my design process.

8. [Real Favicon Generator](https://realfavicongenerator.net):
   * Real Favicon Generator was used to turn the image I created into a favicon.ico file.

9. [Website Mockup Generator](https://websitemockupgenerator.com)
   * Website Mockup Generator was used to create the website mockup at the start of this README.

10.  [JQUERY](https://jquery.com)  
      * JQUERY was used throughout the process of creating my Javascript code.

13. [Final Cut Pro](https://www.apple.com/uk/final-cut-pro/)
      * Final Cut Pro was used to edit the demo video included in this read me.

14. [Logic Pro X](https://www.apple.com/uk/logic-pro/)
      * Logic Pro X was used to record and edit the audio voiceover for the demo video included in this read me.

14. [lighthouse](https://developers.google.com/web/tools/lighthouse)
      * Lighthouse was used to assess the performance of the project.

14. [Wave](https://wave.webaim.org/)
      * Wave was used to assess the accessibility of the project.


# Testing User Stories from the User Experience (UX) Section
- As a first time user I want to:

1. Q.  Quickly understand the purpose and layout of the game
      * The website features a very streamlined and simple navigation bar that quickly allows users to access a clear set of game instructions. The game itself is also well equipped with user messages, buttons with contextual text, and informative pop-ups and modals.

2. Q. Understand how to play the game
      * The game features access to both a clear instructions page which detail exactly how to play the game, and also a very in-depth resource that both explains the techniques needed to beat the game and also allows users to generate the necessary tools to win.

3. Q .Receive tips and guidance on how to improve my score
      * The "Memory Tips" page both gives a comprehensive history of the techniques of memorisation, along with detailed instructions as to how the user can quickly improve their memory. This page also has a tool that allows the user to generate their own PAO system and save it to their computer. The ability to play at differing difficulty levels, and to track previous scores also aid the player in improving their scores.

- As a returning visitor I want to:

1. Q. Have different levels of difficulty to challenge myself
      * The game features three seperate dificulty levels. Easy: 10 cards, Medium: 25 cards, Hard: 52 cards.

2. Q. Have a system to track my previous score so that I can try and improve my skill
      * The game has a "Previous Scores" button that saves the users previous efforts to local storage for them to keep track of their last attempt across browser sessions.

3. Q. Have tools to help me develop a method to learn the skills of memorisation
      * The "Memory Tips" page contains both detailed historical information surrounding the pursit of memory techniques, along with detailed instructions on how to best memorise the deck of cards among other things. It also has a PAO generator section to allow the user to create their own memory tool to beat the game.

## Further Testing
---
### Validator Results
* All Html pages passed through the official [W3C Validator](https://validator.w3.org) validator with no errors.

Results can be found here:
[Game Page](assets/readme-images/new-index.html-validator-min.png)|[How To Play](assets/readme-images/how-to-play-html-validator.png)|[Memory Tips](assets/readme-images/memory-tips-html-validator.png)|

* The CSS stylesheets all passed through the official [W3C Validator](https://validator.w3.org) with no issues.

CSS validation results can be found here: 
[style.css](assets/readme-images/style.css-validator.png)| [memory-tips.css](assets/readme-images/memorytips.css-validator.png)| [How-to-play.css](assets/readme-images/gameinstructions.css-validator.png)

### Manual Testing
* The website was tested on multiple web-browsers including Safari, Chrome, Firefox and Brave.

* The website was viewed on multiple devices with varying screen sizes. These include multiple iPhone 11's, an iPad air, an iPad pro, a 16 inch Macbook pro and a 13 inch Acer laptop.

* All links and pages were tested thoroughly across various browsers and screen sizes.

* Family members trialled the website on their own devices to both give feedback and look for bugs. 

### Known Bugs
* On my current version of Safari browser, some of the buttons are slightly misaligned compared to Google Chrome.
* On the iPhones that I tested the site on, the sound files all work perfectly for their first play, however subsequent plays have the very start clipped off. This is a minor issue and is only noticeable when looking for it.
* In the console, the following error message is displayed: "Error with Permissions-Policy header: Unrecognized feature: 'interest-cohort'.". From my research this appears to be an issue with Github Pages.
![Console Error Message](/assets/readme-images/console-error-msg.png)

### Notable Solved Bugs
* After first deploying my site to Github pages, when the game was started and the poker theme was introduced, on ipads the entire interface of the game would rotate and become unusable. This only happened on iPad, not on any phone or computer, however it was present on multiple iPads. 
This fix for this turned out to be a CSS rule to rotate the background image of the Nav and Footer by 90 deg. I did this to change the alignment of the wood grain in the image, however it seemed the iPad misinterpreted this as "Rotate the nav and footer 90 deg". This is now solved.

* On certain screen sizes the cards would become misaligned when flipped. I initially tried to fix this through very tedious testing of media queries to compensate at different screen sizes. This was not an ideal solution. After much testing I found that by using "Scalex(-1)" instead of "Translatex(-100%)" the cards correctly alligned.

## Accessibility and Performance
---
The project was tested using both [lighthouse](https://developers.google.com/web/tools/lighthouse) and [Wave](https://wave.webaim.org/) to check the overall performance and accessibility of the project.

The [Wave](https://wave.webaim.org/) report revealed no errors, and just a few advisory alerts for things such as "potentially erroneous alt text." I investigated all of these and found no issue with them.
Wave results can be viewed here:
[Main page](assets/readme-images/wave-index-min.png)
[Memory Tips](assets/readme-images/wave-memory-tips-min.png)
[How to play](assets/readme-images/wave-how-to-play-min.png)

The [lighthouse](https://developers.google.com/web/tools/lighthouse) report was positive for all areas, particularly on the main game page.
Light house results can be viewed here:
[Main page](assets/readme-images/index.html-performance-min.png)
[Memory Tips](assets/readme-images/memory-tips-performance-min.png)
[How to play](assets/readme-images/game-instructions-performance-min.png)

## Deployment
---

### GitHub Pages

 The project was deployed to GitHub Pages using the following steps...

 1. Log in to GitHub and locate the [GitHub Repository](https://github.com/Luketedwards/memorise-a-deck-of-cards)
 2. At the top of the Repository (not top of page), locate the "Settings" Button on the menu.
     - Alternatively Click [Here](https://raw.githubusercontent.com/) for a GIF demonstrating the process starting from Step 2.
 3. Scroll down the Settings page until you locate the "GitHub Pages" Section.
 4. Under "Source", click the dropdown called "None" and select "Master Branch".
 5. The page will automatically refresh.
 6. Scroll back down through the page to locate the now published site [link](https://luketedwards.github.io/memorise-a-deck-of-cards/index.html) in the "GitHub Pages" section.

 ### Forking the GitHub Repository

 By forking the GitHub Repository we make a copy of the original repository on our GitHub account to view and/or make changes without affecting the original repository by using the following steps...

 1. Log in to GitHub and locate the [GitHub Repository](https://github.com/Luketedwards/memorise-a-deck-of-cards)
 2. At the top of the Repository (not top of page) just above the "Settings" Button on the menu, locate the "Fork" Button.
 3. You should now have a copy of the original repository in your GitHub account.

 ### Making a Local Clone

 1. Log in to GitHub and locate the [GitHub Repository](https://github.com/Luketedwards/memorise-a-deck-of-cards)
 2. Under the repository name, click "Clone or download".
 3. To clone the repository using HTTPS, under "Clone with HTTPS", copy the link.
 4. Open Git Bash
 5. Change the current working directory to the location where you want the cloned directory to be made.
 6. Type `git clone`, and then paste the URL you copied in Step 3.

 ```
 $ git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY
 ```

 7. Press Enter. Your local clone will be created.

 ```
 $ git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY
 > Cloning into `CI-Clone`...
 > remote: Counting objects: 10, done.
 > remote: Compressing objects: 100% (8/8), done.
 > remove: Total 10 (delta 1), reused 10 (delta 1)
 > Unpacking objects: 100% (10/10), done.
 ```

 Click [Here](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository#cloning-a-repository-to-github-desktop) to retrieve pictures for some of the buttons and more detailed explanations of the above process.

 # Credits

## Code 
* Bootstrap4: Bootstrap library was used during the inital setup of my site to help quickly create a responsive design. I also used their code in initially creating one of the modals on the page.
* Sweet alert 2: I used several of their templates to create an aesthetically pleasing modal for my game information, before altering it to suit my requirements.
## Content

## Media

### Images
---
* All poker chip buttons were created in Affinity Photo by the developer using this background provided by [SVG Repo](https://www.svgrepo.com/svg/4886/poker-chip).
* Images for the playing cards were downloaded from [Google Code Archive](https://code.google.com/archive/p/vector-playing-cards/).
* Images of the card suits were downloaded using a free trial from [Adobe](https://stock.adobe.com/images/set-poker-cards-symbols-vector/323996998?as_campaign=TinEye&as_content=tineye_match&epi1=323996998&tduid=f877f64edb5850dacc9d98bf4bac7909&as_channel=affiliate&as_campclass=redirect&as_source=arvato).
* Image for poker table wooden background from [Joshua Bartell on Unsplash](https://unsplash.com/photos/6vvIBTvL90A).
* Green felt poker table background from [Engin Akyurt on Unsplash](https://unsplash.com/photos/HEMIBJ8QQuA).
* Image of brain on "Memory tips" page were downloade using a free trial from [Adobe](https://stock.adobe.com/images/human-brain-on-white-background/26636186?as_campaign=TinEye&as_content=tineye_match&epi1=26636186&tduid=f877f64edb5850dacc9d98bf4bac7909&as_channel=affiliate&as_campclass=redirect&as_source=arvato).
* Image of playing cards from "Game Instructions" page from [Eyestetix on Unsplash](https://unsplash.com/@eyestetix).
 ### Audio
 ---
 * "Try again" sound effect [javapimp on freesound](https://freesound.org/people/javapimp/sounds/439187/).
 * Card flip sound effect [notification sounds](https://notification-sounds.com/1433-card-flip-sound-effect.html).
 * "Congratulations" sound effect [dersuperanton on freesound](https://freesound.org/people/dersuperanton/sounds/433702/) 
 * Card shuffle sound effect [SoundJay](https://www.soundjay.com/misc/sounds/shuffling-cards-1.mp3).
 * Error sound effect [Freesoundeffect](http://freesoundeffect.net/sound/multimedia-error-08-sound-effect).
 * Un-mute audio sound [Freesound](https://freesound.org/people/dland/sounds/320181/).
 * Game Won sound effect [Freesound](https://freesound.org/people/FunWithSound/sounds/456966/).
 * Previous Score sound effect [Freesound](https://freesound.org/people/shinephoenixstormcrow/sounds/337049/).
 * Game Over sound effect [Orangefreesounds](https://orangefreesounds.com/you-lose-game-over/).
 * "Completed Memorising Cards" sound [Freesound](https://freesound.org/people/shinephoenixstormcrow/sounds/337049/).

## Acknowledgements
---

* My mentor Rahul Lakhanpal for his support and invaluable advice throughout my project.

* Code Institute for their excellent learning platform and student support.

* [W3C Schools](https://www.w3schools.com/) and [Stack Overflow](https://stackoverflow.com/) for being valuable resources when I encountered problems in my code. 
