# coding: utf-8
"""
    wp2tumblr
    ~~~~~~

    A simple tool to import a Wordpress XML file into Tumblr

    :copyright: (c) 2014 by Jon Thornton.
    :license: BSD, see LICENSE for more details.
"""

import datetime
from xml.dom import minidom
# import types

from flask import Flask
from flask import g, session, request, url_for, flash
from flask import redirect, render_template
from flask_oauthlib.client import OAuth
import pytumblr


app = Flask(__name__, static_folder='static', static_url_path='')
app.config.from_envvar('WP2TUMBLR_SETTINGS')

POST_STATES = {
    'publish': 'published',
    'draft': 'draft',
    'pending': 'draft',
    'private': 'private',
    'future': 'queue'
}

oauth = OAuth(app)

tumblr_oauth = oauth.remote_app(
    'tumblr',
    app_key='TUMBLR',
    request_token_url='http://www.tumblr.com/oauth/request_token',
    access_token_url='http://www.tumblr.com/oauth/access_token',
    authorize_url='http://www.tumblr.com/oauth/authorize',
    base_url='https://api.tumblr.com/v2/',
)




@tumblr_oauth.tokengetter
def get_tumblr_token():
    if 'tumblr_oauth' in session:
        resp = session['tumblr_oauth']
        return resp['oauth_token'], resp['oauth_token_secret']


@app.route('/oauthorized')
@tumblr_oauth.authorized_handler
def oauthorized(resp):
    if resp is None:
        flash('You denied the request to sign in.')
    else:
        session['tumblr_oauth'] = resp

    return redirect(url_for('index'))

@app.before_request
def before_request():
    g.tumblr = None

    if 'tumblr_oauth' in session:
        g.tumblr = pytumblr.TumblrRestClient(
            app.config['TUMBLR_CONSUMER_KEY'],
            app.config['TUMBLR_CONSUMER_SECRET'],
            session['tumblr_oauth']['oauth_token'],
            session['tumblr_oauth']['oauth_token_secret'],
        )



@app.route('/login')
def login():
    return tumblr_oauth.authorize()


@app.route('/logout')
def logout():
    flash('You\'ve logged out')
    session.pop('tumblr_oauth', None)
    return redirect(url_for('index'))

@app.route('/')
def index():
    userinfo = None
    if g.tumblr:
        userinfo = g.tumblr.info()
    return render_template('index.html', userinfo = userinfo)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if g.tumblr is None:
        return redirect(url_for('login'))

    tumblog_name = request.form.get('tumblog_name') or request.args.get('tumblog_name')
    if not tumblog_name:
        return redirect(url_for('index'))

    bloginfo = g.tumblr.blog_info(tumblog_name)
    if 'meta' in bloginfo and bloginfo['meta']['status'] != 200:
        flash('Invalid blog name')
        return redirect(url_for('index'))

    if request.method == 'POST':
        # try:
        post_count = do_import(tumblog_name, request.files['wordpress_xml'])
        # except Exception, detail:
        #     print 'XML file must be well-formed. You\'ll need to edit the file to fix the problem.'
        #     print detail

        if 'LOG_FILE' in app.config:
            userinfo = g.tumblr.info()

            with open(app.config['LOG_FILE'], 'a') as f:
                f.write('%s\t%s\t%s\t%s\t%d posts\n' % (
                    datetime.datetime.now().isoformat(),
                    userinfo['user']['name'],
                    bloginfo['blog']['title'],
                    bloginfo['blog']['url'],
                    post_count)
                );

        flash('%d posts from your Wordpress blog have been imported into %s!' % (post_count, tumblog_name))
        return redirect(url_for('index'))

    return render_template('upload.html', bloginfo=bloginfo, tumblog_name=tumblog_name)


def do_import(tumblog_name, xml_file):
    dom = minidom.parse(xml_file)

    post_count = 0
    for item in dom.getElementsByTagName('item'):

        # only import posts, not pages or other stuff
        if item.getElementsByTagName('wp:post_type')[0].firstChild.nodeValue != 'post':
            continue;

        if len(item.getElementsByTagName('title')[0].childNodes) == 0:
            continue;

        post = {
            'type': 'text',
            'title': item.getElementsByTagName('title')[0].firstChild.nodeValue.strip().encode('utf-8', 'xmlcharrefreplace'),
            'date': item.getElementsByTagName('pubDate')[0].firstChild.nodeValue,
            'state': POST_STATES.get(item.getElementsByTagName('wp:status')[0].firstChild.nodeValue)
        }

        if post['state'] is None:
            continue

        content = item.getElementsByTagName('content:encoded')[0].firstChild

        if content.__class__.__name__ != 'CDATASection':
            continue

        post['body'] = item.getElementsByTagName('content:encoded')[0].firstChild.nodeValue.encode('utf-8', 'xmlcharrefreplace')
        print post["title"]

        g.tumblr.create_text(tumblog_name,
                            type=post['type'],
                            title=post['title'],
                            body=post['body'],
                            date=post['date'],
                            state=post['state'])

        post_count += 1

    return post_count

if __name__ == '__main__':
    app.run()
