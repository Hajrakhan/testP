from os import close
from flask import Flask, render_template,flash
from flask import request,session
import json
from werkzeug.utils import redirect,secure_filename
from flask_mysqldb import MySQL
import psycopg2
import random

app.route('/')
def updatepost():
    return render_template('hell.html')

if __name__ == '__main__':
   app.run()
