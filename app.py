from flask import Flask, render_template
import psycopg2
import json

with open('config.json', 'r') as c:
    params = json.load(c)["params"]
app = Flask(__name__)
con = psycopg2.connect(database="d7kuslrveqbabl", user="lyawunaedvwsuv", password="29f7357bdc32e4f28a0b5a3bb6e629e60a672805e7ea7dbaac586ddbae722fbc", host="ec2-44-195-209-130.compute-1.amazonaws.com", port="5432")
def get_posts():
    cur = con.cursor()
    cur.execute("SELECT * FROM post	LEFT JOIN category ON post.postcategory=category.categoryID LEFT JOIN _user ON post.postAuthor=_user.userID ORDER BY post.postID DESC;")
    posts = cur.fetchall()
    cur.close()
    return(posts)
def categories():
    cur = con.cursor()
    cur.execute("SELECT  * FROM category;")
    cate=cur.fetchall()
    return(cate)
@app.route("/")
def Home():
    category=categories()
    posts=get_posts()
    return render_template('index.html',params=params,category=category,posts=posts)

