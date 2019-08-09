from app import app, db, user_datastore

@app.before_first_request
def setup():
  # create admin user
  db.create_all()
  user_datastore.create_user(username='admin', password='admin')
  db.session.commit()

@app.route('/')
def index():
    return "Hello world!"
