import os
from flask import Flask, redirect, render_template, jsonify, request, send_from_directory, flash, session
from flask_cors import CORS
from sqlalchemy.exc import OperationalError
from App.models import db, get_migrate, create_db, Book, Review  
import json
from datetime import timedelta
def create_app():
    
    create_db(app)
    app.app_context().push()
    return app
def loadConfig(app, config):
    app.config['ENV'] = os.environ.get('ENV', 'DEVELOPMENT')
    if app.config['ENV'] == "DEVELOPMENT":
      app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
      app.config['TEMPLATES_AUTO_RELOAD'] = True
      app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'data.db')
      app.config['DEBUG'] = True
      app.config['SECRET_KEY'] = 'MySecretKey'
     
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
        app.config['DEBUG'] = os.environ.get('ENV').upper() != 'PRODUCTION'
        app.config['ENV'] = os.environ.get('ENV')
        app.config['PREFERRED_URL_SCHEME'] = 'https'
    for key, value in config.items():
        app.config[key] = config[key]

def create_app(config={}):
    app = Flask(__name__, static_url_path='/static')
    CORS(app)
    loadConfig(app, config)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['PREFERRED_URL_SCHEME'] = 'https'
    create_db(app)
    app.app_context().push()
    return app
app = create_app()

migrate = get_migrate(app)
def get_all_books_as_json():
  books = Book.query.all()
  if not books:
        return []
  books = [book.toDict() for book in books]
  return books
@app.route('/add_review', methods=['POST'])
def add_review():
  data = request.form
  new_review = Review(text=data['text'],rating=data['group1'],isbn= data['isbn'])
  db.session.add(new_review)
  db.session.commit()
  flash("Review Added")
  return redirect('/') 
@app.route('/del_review/<id>', methods=['POST'])
def delete_review(id):
  review = Review.query.filter_by(id = id).first()
  db.session.delete(review)
  db.session.commit()
  flash("Review Deleted")
  return redirect('/') 

@app.route('/getBooks', methods=['GET'])
def getBooks():
    return json.dumps(get_all_books_as_json())
@app.route('/', methods=['GET'])
def home():
  return render_template('app.html', books = get_all_books_as_json())


@app.route('/static/home', methods=['GET'])
def home2():
  return send_from_directory('static', 'app.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True) 