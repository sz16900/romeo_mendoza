from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash

import json

app = Flask(__name__)

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')



def page(name):
    """Dynamically create & register a route for a given file/route name
    We do this since currently the logic for each of the 5 sub-pages is identical.
    """
    def handler():
        with open('data/{}.json'.format(name)) as fp:
            arts = json.load(fp)
        return render_template('page.html', arts=arts)
    app.add_url_rule('/{}.html'.format(name), name, handler)

page('hiperrealismo')
page('bocetos')
page('surrealismo')
page('otros')
page('taller')
