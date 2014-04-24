# Import a Wordpress Blog into Tumblr: wp2tumblr


wp2tumblr is a simple [Flask](http://flask.pocoo.org/docs/) app that will import a Wordpress XML export into Tumblr with publishing dates intact.

## Alpha Version

This app is under active development and has minimal testing. Use at your own risk.

## Requirements

* [Python](http://www.python.org/getit/)
* [pip](https://pypi.python.org/pypi/pip)

## Usage

A hosted version of wp2tumblr is available at http://wp2tumblr.jonthornton.com. If you'd like to run your own copy, follow these steps:

1. Clone the wp2tumblr repo.
2. Visit http://www.tumblr.com/oauth/apps and register a new application. Set the default callback url to ```http://127.0.0.1:5000/oauthorized```. The rest of the fields can be filled in however you want.
3. Copy settings.py.sample to settings.py and fill in your client keys.
4. Export the path to the settings file: ```$ export WP2TUMBLR_SETTINGS=/path/to/settings.py```
5. Install the required packages: ```$ pip install -r requirements.txt```
6. Start the server ```$ python wp2tumblr.py```
7. Open your browser to http://127.0.0.1:5000 and follow the instructions


## Help

Submit a [GitHub Issues request](https://github.com/jonthornton/wp2tumblr/issues/new).

------------------

This software is made available under the open source MIT License. &copy; 2014 [Jon Thornton](http://jonthornton.com).
