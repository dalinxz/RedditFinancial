# -*- coding: utf-8 -*-

# app.py
from flask import Flask, session        # import flask
from flask import render_template, request
from forms import front_page_form, search_results_form
from flask import render_template, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
import requests

ID = ''
app = Flask(__name__)             # create an app instance
app.config['SECRET_KEY'] = 'you-will-never-guess'
@app.route("/", methods=['GET', 'POST'])              # at the end point /<name>
def index():
    form = front_page_form()
    data = [{'url': 'https://www.reddit.com/r/flask/comments/hrquu9/how_to_pass_a_variable_between_routes_without/'}, 
            {'url': 'https://www.reddit.com/r/help/comments/ague8j/how_do_i_view_my_own_posts/'},
            {'url': 'https://www.reddit.com/r/wallstreetbets/comments/l9cz1k/for_everyone_that_just_joined_because_of_gme_and/'}
            ]
    if form.validate_on_submit():
        session['search_val'] = form.search_box.data
        return redirect('/search_results')
    return render_template('index.html', form=form, data=data)

@app.route("/search_results", methods=['GET', 'POST'])
def search_results():
    form = search_results_form()
    my_var = session.get('search_val', None)
    print(my_var)
    return render_template('search_results.html', form=form)

def get_top_3():
    

if __name__ == "__main__":
    port_used = 5000
    app.run(port=port_used) 
                          # run the flask app
    
    