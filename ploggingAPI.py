#!/usr/bin/env python

from flask import Flask, request, jsonify
from database import *
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
def get_specific_post(post_id):
    postlist = Database.get_post(post_id)
    return jsonify(postlist), 200

@app.get("/posts?term=<string:word>")
def get_post_filter(word):
    word =  request.args.get('term')
    #search the database with the `word` and display result
    return 

@app.put("/posts/<int:post_id>")
def update_post(post_id):
    pass

@app.delete("/posts/<int:post_id>")
def delete_post(post_id):
    
    result = Database.delete_post(post_id)
    if result == 1:
        return jsonify({"Message":"Resource Was Deleted!"})
    else:
        return jsonify({"Message":"No Resource was found or somthing else"})

@app.post("/posts")
def create_post():
    data = json.loads(request.data) 

    values = ( data["title"], data["content"], data["category"] )
    result = Database.add_post(values)
    if result == []:
        return jsonify({"Message":"Post Created Succesfully!"}), 201

if __name__ == "__main__":
    app.run()
