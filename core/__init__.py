from flask import Flask

app = Flask('core')
app.config.from_object('core.settings')

# if app.debug:
#     from werkzeug import DebuggedApplication
#    app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True)
    # from google.appengine.ext.appstats import recording
    # app.wsgi_app = recording.appstats_wsgi_middleware(app.wsgi_app)

import views
