from flask import Flask
import psycopg2
import json

with open('config.json', 'r') as c:
    params = json.load(c)["params"]
app = Flask(__name__)
con = psycopg2.connect(database="d7kuslrveqbabl", user="lyawunaedvwsuv", password="29f7357bdc32e4f28a0b5a3bb6e629e60a672805e7ea7dbaac586ddbae722fbc", host="ec2-44-195-209-130.compute-1.amazonaws.com", port="5432")

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
