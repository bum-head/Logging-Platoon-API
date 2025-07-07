#!/usr/bin/env python

from flask import Flask, request, jsonify
import mysql.connector as sql


app = Flask(__name__)


@app.get("/posts")
def get_all_posts():
    return jsonify(postlist), 200

@app.get("/posts/<int:post_id>") ## post_id is substitute for the id?               
def get_post():
    return 200

@app.get("/posts?term=<string:word>")
def get_post_filter():
    return 

@app.put("/posts/<int:post_id>")
def update_post():
    pass

@app.delete("/posts/<int:post_id>")
def delete_post():
    pass

@app.post("/posts")
def add_post():
    return 201    


if __name__ == "__main__":
    app.run()
