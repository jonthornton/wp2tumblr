# This project is abandonded

Tumblr is no longer the same company and community it was when I wrote this application, and I decided to stop supporting it in 2018. You're free to continue using the code on your own.

# Import a Wordpress Blog into Tumblr: wp2tumblr

wp2tumblr is a simple [Flask](http://flask.pocoo.org/docs/) app that will import a Wordpress XML export into Tumblr with publishing dates intact.

## Requirements

* [Python](http://www.python.org/getit/)
* [pip](https://pypi.python.org/pypi/pip)

## Usage

A hosted version of wp2tumblr is available at http://wp2tumblr.jonthornton.com. If you'd like to run your own copy, follow these steps:

1. Clone the wp2tumblr repo.
2. Visit http://www.tumblr.com/oauth/apps and register a new application. Set the default callback url to ```http://127.0.0.1:5000/oauthorized```. The rest of the fields can be filled in however you want.
3. Copy settings.py.sample to settings.py and fill in your client keys. Set ```DEBUG = False``` to enable posting.
4. Install the required packages: ```$ pip install -r requirements.txt```
5. Start the server ```$ WP2TUMBLR_SETTINGS=/path/to/settings.py; python wp2tumblr.py```
6. Open your browser to http://127.0.0.1:5000 and follow the instructions


## Help

Submit a [GitHub Issues request](https://github.com/jonthornton/wp2tumblr/issues/new).

------------------

This software is made available under the open source MIT License. &copy; 2014 [Jon Thornton](http://jonthornton.com).
