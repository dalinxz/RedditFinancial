# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 12:55:48 2020

@author: aliakbari, suryagandikota
"""



# app.py
from flask import Flask           # import flask
from flask import render_template, request
from forms import front_page_form, search_results_form
from flask import render_template, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

ID = ''
app = Flask(__name__)             # create an app instance
app.config['SECRET_KEY'] = 'you-will-never-guess'
@app.route("/", methods=['GET', 'POST'])              # at the end point /<name>
def index():
    form = front_page_form()
    if form.validate_on_submit():
        return render_template('search_results.html', form=front_page_form())
    return render_template('index.html', form=form)

@app.route("/search_results", methods=['GET', 'POST'])
def search_results():
    form = search_results_form()
    if form.validate_on_submit():
        redirect('/search_results')
    return render_template('search_results.html', form=form)

if __name__ == "__main__":
    port_used = 5000
    app.run(port=port_used) 
                          # run the flask app
    
    