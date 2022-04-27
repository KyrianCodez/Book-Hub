from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def get_migrate(app):
    return Migrate(app, db)

def create_db(app):
    db.init_app(app)
    db.create_all(app=app)
    
def init_db(app):
    db.init_app(app)

class Book(db.Model):
    isbn = db.Column(db.String, primary_key=True)
    title = db.Column(db.String)
    author = db.Column(db.String)
    publication_year = db.Column(db.Integer)
    publisher = db.Column(db.String)
    image_s = db.Column(db.String)
    image_m= db.Column(db.String)
    image_l = db.Column(db.String)
    reviews = db.relationship('Review')


    def get_avg_rating(self, reviews):
        if not reviews:
          return 0
        count = len(reviews)
        sum = 0
        for review in reviews:
          sum = sum + review['rating']
        avg = sum / count
        avg = round(avg)
        return avg
          
   
    
    def toDict(self):
        if self.reviews:
            reviews = Review.query.filter_by(isbn=self.isbn).all()
            reviews = [review.toDict() for review in reviews]
        else:
            reviews = None
        return {
            "isbn": self.isbn,
            "title":self.title,
            "author":self.author,
            "publication_year":self.publication_year,
            "publisher":self.publisher,
            "image_s":self.image_s,
            "image_m":self.image_m,
            "image_l":self.image_l,
            "reviews" : reviews,
            "ratings" : self.get_avg_rating(reviews)
        }


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String)
    rating = db.Column(db.Integer)
    isbn = db.Column(db.String,  db.ForeignKey('book.isbn'))

    def toDict(self):
        return {
            "id": self.id,
            "text":self.text,
            "rating":self.rating,
            "isbn":self.isbn,
        }
   