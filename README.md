tracktool
=========

Introduction
------------

This project was made in 6 days, then management decided to stop development.
the initial commit (or tag 0.1) is exactly what has been done. (except I deleted some vital parts as passwords)

In the coming time I'll restart development and try to make it the app it deserved to be.


Installation
------------

Clone this repository by using

    git clone https://github.com/jghyllebert/tracktool.git

Install the requirements

    pip install -r tracktool/requirements/base.txt

At the moment I need to do some cleanup so the application can store data on any Google Drive.
We only need the Google Drive API enabled.

Don't forget to add a ``SECRET KEY`` in the ``settings.py`` file. Also, add a Database setup.


What does it do?
----------------

It tracks the progress of a sale. A sale goes through a set of predefined steps (Sales, Photographer, Production and Invoicing).

At the moment it does just this, but it could be extended with graphs and other charts to analyse every step.
