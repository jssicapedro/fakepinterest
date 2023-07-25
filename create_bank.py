from Fakepinterest import database, app
from Fakepinterest.models import User, Post

with app.app_context():
    database.create_all()