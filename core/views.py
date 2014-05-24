# -*- coding: UTF-8 -*-

from core import app
from google.appengine.api import urlfetch

urlfetch.set_default_fetch_deadline(120)


@app.route("/")
def home():
    return "Hello World!"
