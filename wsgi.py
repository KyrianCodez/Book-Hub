from asyncore import read
import click
from flask import Flask, jsonify
from App import create_db, db, app
import csv
import json

from App.models import Book

@app.cli.command("init")
def initialize():
    

    with open('./books.csv', newline='',encoding='cp1252') as f:
       
        # Darth_Sourav https://stackoverflow.com/questions/51966824/how-to-remove-double-quotes-in-csv-file-with-python
        f = f.read().replace('"', '').replace('"', '').replace(',', '').replace(',', '').replace('&amp;',' & ').replace('LÃ?Â¼bbe','Lübbe').splitlines() 
        reader = csv.DictReader(f,delimiter=';',lineterminator='\n', escapechar='"', quoting=csv.QUOTE_NONE,)
        print(reader.fieldnames)
        for row in reader:
            book = Book(isbn = row.get('ISBN'), title=row.get("Book-Title"), author=row.get("Book-Author"), publication_year = row.get("Year-Of-Publication"),publisher = row.get("Publisher"),image_s = row.get("Image-URL-S"), image_m = row.get("Image-URL-M"), image_l = row.get("Image-URL-L"))
            try:
                db.session.add(book) 
                db.session.commit()
            except:
                db.session.rollback
                print('Book failed to add')
            print('Book added')
        create_db(app)
        print('database intialized')
        