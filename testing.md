# Testing During Development

During development I continually testing the project in a number of ways.

- I manually tested the responsiveness of each page and element within the development environment by running the application and checking the output within the browser.

- Once happy with any new additions the code was pushed to Heroku. I then ran the same tests using other devices, and had family and friends do the same on their own devices, before passing on any feedback or suggestions.

## Manual Testing

* During testing I used numerous web browsers to ensure the site performed well on a range of browsers. On desktop I used the following:

1. Safari
2. Chrome
3. Firefox
4. Brave

* I used Google devtools to simulate different screen sizes and devices to check useability and responsiveness on a range of screen sizes.

* I also tested the site on an iPhone 11 and an ipad pro and air, using both Safari and Chrome.


# Testing User Stories from the User Experience Section

## User Stories:
---
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

## Responses to User Stories

- As a first time user I want to:

1. Q.  Quickly understand the purpose and layout of the site.
      * The site is layed out in an organised manner with quick access to any area from the navbar. The process of ceating and joining musical projects is intuitive and streamlined.

2. Q. Understand how to create a profile and navigate the sites functionality.
      * The website features a very streamlined and simple navigation bar that quickly allows users access to any area of the site within 2-3 mouse clicks. All areas of the site are neatly organised to make navigation as streamlined as possible.
      The Registeration process is quick and clear and can easily be completed in just a minute.

3. Q. Be able to customise my profile.
      * The user is easilly able to update and change any aspect of their profile. They are also able to upload their own custom profile picture.

4. Q. Be able to view other users profiles and interact with them.
    * There are multiple ways to quickly search for an access other users profiles. This includes a username search bar, a form to search for users by parameter and a list of all users.
    There is also the option to follow other users to created a saved list of users you would like to store. 
    User accounts are also very easy to navigate to. Any time a username is visible on the site, for example in a message, comment or project card, the username can be clicked to take you to their profile.


- As a returning visitor I want to:

1. Q. Be able to create and edit musical projects and advertise them to relevant site members.
      * The site allows for creation and updating of musical projects with ease. There is lots of scope for specifying exactly what you want to achieve with the project. The projects are then easilly found by other users including by relevance.

2. Q. Be able to find projects relevant to my skills and interests, and then apply to join them.
      * The process for finding projects relevant to your profile is very quick and seamless. Once found applying to join the project is extremely quick via a short form.

3. Q. Be able to communicate with other members/users on the site.
      * There are two simple ways to communicate with othe users, either through a communal project chat, or via direct message.

4. Q. Be able to share sheet music, MP3's and other relevant files to project members.
      * The "Memory Tips" page contains both detailed historical information surrounding the pursit of memory techniques, along with detailed instructions on how to best memorise the deck of cards among other things. It also has a PAO generator section to allow the user to create their own memory tool to beat the game.

5. Q. Be able to view other members personal profiles, and follow them to build a community.
      * The "Memory Tips" page contains both detailed historical information surrounding the pursit of memory techniques, along with detailed instructions on how to best memorise the deck of cards among other things. It also has a PAO generator section to allow the user to create their own memory tool to beat the game.

6. Q. Be notified of any actions on the site relevant to me (direct messages, new followers etc.)
      * There is a simple and orgnaised project upload system built into the project hub page which allows upload of any file you may want to share. This can then be ordganised by type, and displayed with the information of file uploader, file description, a custom file name, upload date and the ability to view or download the file.              


- As a frequent visitor I want to:

1. Q. Be able to delete projects and content that I have created.
    * Deleting a project and all of it's related data is very simple and can be done so from the 'manage projects' tab. 

2. Q. Be able to remove my account and all associated data.
    * Deleting your account can be achieved very easily and removes all data about the user apart from messages to other users. 
    This includes all profile data, all following/followers data, all of the users projects and the data associated with them including the files stored on Amazon S3, the users profile image is also deleted. 
    
## Further Testing
---
### Validator Results
* All Html pages passed through the official [W3C Validator](https://validator.w3.org) validator with no errors outside of some warnings caused by some of the materialize dropdowns.

* The CSS stylesheet passed through the official [W3C Validator](https://validator.w3.org) with no issues.

Results can be found [here](/static/readme-files/validator-results/)


### Known Bugs

* Occasionally during development the Javascript would fail to initialise when a page was loaded, causing the materialize dropdowns to not work. This is easilly resolved by reloading the page.

* on some of the ipads tested, when using safari and in landscape mode, the dropdown instrument selection is inaccurate and selects the item either above or below the intended target

### Notable Solved Bugs

* After integrating ImageKit into my project to compress user profile images and improve responsiveness, after uploading a new profile image the previous image would remain on the site and the new one would fail to load. This turned out to be a cache issue with ImageKit, and was solved by calliing for the cache to be purged each time a new image is uploaded by the user. The new image is now displayed shortly after its upload. 


## Accessibility and Performance
---
The project was tested using both [lighthouse](https://developers.google.com/web/tools/lighthouse) and [Wave](https://wave.webaim.org/) to check the overall performance and accessibility of the project.

The [Wave](https://wave.webaim.org/) report revealed some errors however I believe these were irrelevant. For example the link for the side nav is a burger icon. Due to its' lack of text Wave reported this as an empty link error. Some of the labels for the instrument and genre dropdowns are also not recognised despite being present.
Wave results can be viewed [here](/static/readme-files/wave/)

The [lighthouse](https://developers.google.com/web/tools/lighthouse) report was positive for almost all areas, particularly for accessibility, SEO and best practises. Some marks were lost again due to an 'Empty link' for the side nav being present in the 'base.html' file, and thus occuring on every page.
Performance was generally rated positively, and the site seems to run very well on all tested devices.
Light house results can be viewed [here](/static/readme-files/lighthouse/)

The python file was run through the PEP8 validator to ensure no syntax errors, and the Javascript files were validated using JsHint.
I used both autopep8 and an online tool to try to adhere to PEP8 guidlines with the python code. In some cases the code is longer than the suggested 79 characters. I chose to leave these as they were as any alterations I made resulted in much less readable code.

[Return to README](/README.md)