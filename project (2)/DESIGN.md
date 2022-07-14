MusicReviewer Design Document

	MusicReviewer was implemented using the CS50 IDE and was modeled after Finance. Similar to Finance, MusicReviewer uses Flask, Jinja, Javascript, Python, HTML, phpliteadmin, and CSS. We used the skeleton of Finance to format our website.
	
    We used “layout.html,” “apology.html,” “login.html,” “register.html,” and “logout.html” from Finance. Additionally, we borrowed elements from Finance’s “styles.css” file to style the elements of our website that are borrowed from Finance.

    Also similar to Finance, our helpers.py is borrowed from Finance, and the framework for our “app.py” is additionally borrowed from Finance, mainly the libraries at the top of “app.py” and the structure of our functions. In our “app.py,” we have eight functions: index (for displaying our feed),  review (for posting a review), search (for searching for another user), profile (for accessing your own reviews), login (for logging in),  logout (for logging out),  register (for registering an user), and errorhandler (for return error messages).

    Our database is named “musicreviewer.db.” We have three tables in our database: “album_covers,” “reviews,” and “users.” “Album_covers” is used to store our images alongside their respective reviews. “Reviews” contains all of the information displayed in the review and the user’s id. “Users” contains identifying information about the users.

    For our html files, we have: “apology.html,” “index.html,” layout.html,” “login.html,” “postreview.html,” “register.html,” and “search.html.” “Apology.html” is borrowed from Finance and displays the “Error Message Cat” whenever a recognizable error occurs. “Index.html” displays MusicReviewer’s feed. “Layout.html” is used to keep the formatting of MusicReviewer, such as the navigation bar, present. “Login.html” is used to log a user in. “Postreview.html” displays the “Add Review'' page. “Profile.html” displays the “Profile” page. “Register.html” is used to register a user. “Search.html” is used to display the “Search” page and search for a user.

    In search.html, we used Javascript to implement a function we found online that loops through all of the usernames as the user types in a username, only displaying usernames that correspond with the user’s given input.

    We formatted our review cards using the “Album” example from Bootstrap. Our website is additionally formatted using some of Finance’s HTML and CSS.

    Hope you all enjoy it! This is MusicReviewer50.
