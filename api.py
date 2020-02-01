from eve import Eve
from flask import render_template,request,redirect,url_for, session, escape,Response,jsonify, send_file
from eve.auth import BasicAuth
from eve.methods.get import get_internal
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from werkzeug import secure_filename
from bson import regex
from random import randint
import json,pathlib,hashlib
import requests,random,os
from datetime import datetime
import re
import smtplib
import math
import smtplib
from werkzeug import secure_filename
import reverse_geocoder as rg
from math import radians, cos, sin, asin, sqrt,atan2
from os import listdir

port = 5000
#host = '142.93.209.128'
host = "0.0.0.0"
class MyBasicAuth(BasicAuth):
    def check_auth(self, username, password, allowed_roles, resource, method):
        return username == 'rahasya' and password == '1313'

app = Eve(__name__, auth=MyBasicAuth)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = '5234124584324'

headers = {'Authorization': 'Basic aGVsbG86Z29h==', 'Content-Type':'application/json'}

app.config['MONGO_HOST'] = '0.0.0.0'
app.config['MONGO_PORT'] = '27017'
app.config['MONGO_DBNAME'] = 'hackit'
app.config['MONGO_USERNAME'] = 'rahasya'
app.config['MONGO_PASSWORD'] = '1313'

UPLOAD_FOLDER = "./static/uploads/"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/index')
def index():
    return render_template("index.html")

	
if __name__ == '__main__':
    app.run(host=host, port=port, debug=True)
    #fetch('http://142.93.209.128:5000/places?where={"$or":[{"Cat": {"$regex":"'+search+'","$options" : "i"}},{"BusinessName": {"$regex":"'+search+'","$options" : "i"}}]}', {
