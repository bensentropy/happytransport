from flask import Flask

app = Flask('core')
app.config.from_object('core.settings')

import views
