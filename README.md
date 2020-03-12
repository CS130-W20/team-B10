# Wander.io
Intelligently generates a travel itinerary with minimal user inputs.

## Directory Structure
/maps contains the python backend logic

/maps/templates/maps contains the frontend html files

/maps/static/maps contains the css, javascript and media files


## Installation/Run instructions
To run on localhost:
```shell
virtualenv -p /home/example_username/opt/python-3.6.2/bin/python3 venv
source venv/bin/activate
pip install -r requirements.txt
python wander_io/manage.py runserver
```
Head to http://localhost:8000 on your browser.

Note: we will be removing our Google API from the repository. To add your own, please edit /wander_io/settings.py

## Thanks to
Corey M Schafer for his fantastic Django tutorial series.

## Relevant Links 
- [Working URL](https://wander-io.com/)

