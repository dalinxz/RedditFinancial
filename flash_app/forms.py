# -*- coding: utf-8 -*-
"""
Created on Wed Jul  8 17:37:40 2020

@author: aliakbari
"""


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired
import pandas as pd
import os
from datetime import datetime
from datetime import timedelta

class front_page_form(FlaskForm):
    search_box = StringField('')
    search = SubmitField('Search')

class search_results_form(FlaskForm):
    search = SubmitField('Search')