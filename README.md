# market-access-prototype
Alpha of Market Access / Trade Barriers portal and backend

## Features of this application

Runs the front- and back-end of the Market Access (aka Trade Barriers) application for the alpha phase.

## Languages/applications used

Python 3.6.1
Postgres 9.6

It's easier to run the app runs within a virtual environment. To install virtualenv, run

    [sudo] pip install virtualenv
    
Install virtualenvwrapper

    [sudo] pip install virtualenvwrapper

Make a virtual environment for this app:

    mkvirtualenv -p /usr/local/bin/python3.5 market-access-prototype
    
Install dependencies

    pip install -r requirements.txt
    
# Running the application

## Running with django runserver:

    workon market-access-prototype
    python manage.py runserver
Then visit http://localhost:8000

## Running tests

Tests are currently very simple.

    ./manage.py test

## Load the sample data:

    workon market-access-prototype
    ./manage.py loaddata barriers/fixtures/barrier-sources-fixture.json
    ./manage.py loaddata barriers/fixtures/barrier-types.json
    ./manage.py loaddata barriers/fixtures/countries-fixture.json
    ./manage.py loaddata barriers/fixtures/territories-fixture.json
    ./manage.py loaddata barriers/fixtures/demo-barrier-records.json
    ./manage.py loaddata barriers/fixtures/ec-notifications-september-2017-fixture.json
    ./manage.py loaddata barriers/fixtures/wto-notifications-august-2017-fixture.json
