# SquashBug

This project is meant to help you destroy bugs with maximum effectiveness. Track any bug from its First sightings, to there inevitable demise, then store the records incase you find a similar bug in the future.

The web app was built using the Django Python library using a MVC design architecture.  The app includes users creation, login, password reset, and logout.  Each user has a profile which keeps information such as, profile pictures, amounts of each bug type, and completed bugs.  The main view is ordered by date and paginated by a list of the users bugs.  The bug list view also contains graphs displaying the distrubution of bugs categorically.  Each Bug model contains a severity rating, title, description, date created, foreign user key, and completed values.  Bugs can be reported using the new bug form. 

#Live
https://squashbug.xyz/

<img src="https://i.imgur.com/W8h4b9e.png" width="600" height="400" />
<img src="https://i.imgur.com/EIudZRm.png" width="600" height="400" />
<img src="https://i.imgur.com/llYfpQn.png" width="600" height="400" />
