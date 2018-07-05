# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 10:05:21 2018

@author: Stuming
"""

from flask import Flask, render_template


app = Flask(__name__)


@app.route('/')
def index(name=None):
    return 'Index Page'

@app.route('/login')
def login():
    pass

@app.route('/hello')
def hello_world():
    return 'Hello World!'

@app.route('/user/<username>')
def show_user_profile(username):
    return 'User: {}'.format(username)

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post: {}'.format(post_id)


if __name__ == '__main__':
    app.run()
    