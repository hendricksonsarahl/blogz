#Web app using HTML/CSS/Python/Flask/Jinja2/MySQL which allows users to create and view blog posts. Made for LC101. 

New features added since Build-A-Blog:
<li>User accounts!</li>
User account required to create new blogs and used to keep track of bligs by user id. Restricted website access when no user logged in.
<li>Login and Signup!</li>
Create new user accounts, login to start session, access full website with login.
<li>Logout and navigation!</li>
Logout to end session.
<li>Required login!</li>
Only specific routes allowed when user not logged in, full access when user in session.
<li>Home/Index page!<l1>
Add a new index route where all usernames are displayed. User-specific blog pages link from there.
<li>Dynamic user pages!</li>
Each registered user is listed as a link in '/index' page, link navigates to a dynamic page which displays all blog posts for the selected user. User's name is linked below each blog post in all views.
<li>New and improved Pagination and Hashing!</li>
Pagination, password hashing/salting added.

