tracktool
=========

Introduction
------------

This project was made in 6 days, then management decided to stop development.
the initial commit (or tag 0.1) is exactly what has been done. (except I deleted some vital parts such as passwords)

In the coming time I'll restart development and try to make it the app it deserved to be.


Installation
------------

Clone this repository by using

    git clone https://github.com/jghyllebert/tracktool.git

Install the requirements

    pip install -r tracktool/requirements/base.txt

Don't forget to add a ``SECRET KEY`` in the ``settings.py`` file. Also, add a Database setup.

If you want to use Google Drive to store data, follow these instructions:

* Create a new project on https://console.developers.google.com/project
* Enable the ``Google Drive API``
* On the left sidebar click on ``credentials``
* Create a new ``Client ID`` (under Oauth)
* Choose for ``Web application`` as application type
* Fill in your url at ``AUTHORIZED JAVASCRIPT ORIGINS``
* Make sure that the url in ``AUTHORIZED REDIRECT URI`` matches the value of ``REDIRECT_URL`` in ``settings.py``
* Complete ``settings.py`` with ``CLIENT ID`` and ``CLIENT SECRET``
* Add a ``consent screen`` (found in the left sidebar)
* Log in to your Google Drive and create a folder where the app can store the data in
    * You can find the id of the folder at the url, it's the last part (eg. https://drive.google.com/drive/u/0/#folders/0B1Kf87md0ZV-SENsU2JoTXc1UE0)
    * add **0B1Kf87md0ZV-SENsU2JoTXc1UE0** as value for ``DRIVE_PARENT_FOLDER_ID`` in ``settings.py``

Sync the database using

    cd tracktool
    python tracktool/manage.py syncdb
    python tracktool/manage.py migrate

First, we will allow the application to use our Google drive. Let's start our server:

    python tracktool/manage.py runserver

Then, in our browser, give in the url http://__YOUR URL__/auth_google/ (eg. http://127.0.0.1:8000/auth_google/) and click on ``Authenticate``.
You will be presented with the consent screen you created earlier, click on ``OK`` and you'll be presented with the data we got from Google.
As this setup needs to be completed only once, you can choose to remove the two urls for this.

You can test if everything works by going to the admin panel and just save the pre-installed Country (Belgium).
If you look up the model again, you'll notice the ``Drive Folder Id`` field is now filled in. In your Google Drive there should be a new folder.


What does it do?
----------------

It tracks the progress of a sale. A sale goes through a set of predefined steps (Sales, Photographer, Production and Invoicing).

At the moment it does just this, but it could be extended with graphs and other charts to analyse every step.


Changelog
---------
### 0.2

* Workflow placeholder editable
* Can work on any Google account
* Fixtures for world regions and groups
