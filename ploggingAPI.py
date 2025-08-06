#!/usr/bin/env python

from flask import Flask, request, jsonify
from database import *
from datetime import *
import mysql.connector as sql
import json
import flask

app = Flask(__name__)

Database = Database("localhost", "root", "Root34##", "Altera")

Database.connect_to_database()

@app.get("/posts")
def get_all_posts():
    postlist = Database.get_all_post()
    if not postlist: 
        flask.abort(404, "No postlist Found!!")
    return jsonify(postlist), 200

@app.get("/posts/<int:post_id>") 
def get_post():
    postlist = Database.get_post(post_id)
    return jsonify(postlist), 200

@app.get("/posts?term=<string:word>")
def get_post_filter():
    word =  request.args.get('term')
    #search the database with the `word` and display result
    return 

@app.put("/posts/<int:post_id>")
def update_post():
    pass

@app.delete("/posts/<int:post_id>")
def delete_post():
    pass

@app.post("/posts")
def add_post():
    data = json.loads(request.data) 
    date_now = datetime.now()
    date_now = date_now.strftime("%b %d %Y %H:%M:%S")

    id = len(Database.get_all_post())+1

    values = (id , data["title"], data["content"], data["category"], data["tags"], date_now, date_now)
    result = Database.add_post(values)
    if result == []:
        return 201


if __name__ == "__main__":
    app.run()
