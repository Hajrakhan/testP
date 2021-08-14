from flask import Flask, render_template,request,session
import psycopg2
import json
from datetime import date
from werkzeug.utils import redirect
import random


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
def get_news(newsid):
    cur = con.cursor()
    cur.execute("SELECT * FROM post LEFT JOIN category ON post.postcategory=category.categoryID LEFT JOIN _USER ON post.postAuthor=_user.userid where postid=%s",[newsid])
    posts = cur.fetchall()
    cur.close()
    return(posts)
def _users():
    cur = con.cursor()
    cur.execute("SELECT  * FROM _user;")
    users=cur.fetchall()
    return(users)
def category_Image(id):
    cur = con.cursor()
    cur.execute("SELECT  catimage FROM category WHERE categoryid=%s",[id])
    cate=cur.fetchall()
    return(cate)
def get_news_by_category(cat_id):
    cur = con.cursor()
    cur.execute("SELECT * FROM post LEFT JOIN category ON post.postcategory=category.categoryID LEFT JOIN _user ON post.postAuthor=_user.userID where postcategory=%s ORDER BY post.postID DESC",[cat_id])
    posts = cur.fetchall()
    cur.close()
    return(posts)
def search(term):
    cur = con.cursor()
    cari = "%" + term +"%"
    cur.execute("SELECT * FROM post LEFT JOIN category ON post.postcategory=category.categoryID LEFT JOIN _USER ON post.postAuthor=_user.userid WHERE post.posttitle LIKE %s or post.postdescription LIKE %s ORDER BY postID DESC ",(cari,cari))
    posts = cur.fetchall()
    cur.close()
    return(posts)
#update_functions
def category_details(id):
    cur=con.cursor()
    cur.execute('SELECT * FROM category WHERE categoryid=%s',[id])
    data=cur.fetchall()
    cur.close()
    return(data)
def update_category(id,name):
    cur=con.cursor()
    cur.execute('UPDATE category SET categoryname=%s WHERE categoryid=%s',[name,id])
    cur.close()
    return()
def add_category_function(name):
    cur=con.cursor()
    r=random.randint(1,2000)
    cur.execute("INSERT INTO category(categoryid,categoryname,categoryposts,catimage) VALUES (%s,%s,%s,%s)",[r,name,'0','global.jpg'])
    cur.close()
    return()

def user_details(id):
    cur=con.cursor()
    cur.execute('SELECT * FROM _user WHERE userid=%s',[id])
    data=cur.fetchall()
    cur.close()
    return(data)
def update_user(id,fname,lname,user):
    cur=con.cursor()
    cur.execute('UPDATE _user SET firstname=%s, lastname=%s, username=%s WHERE userid=%s',[fname,lname,user,id])
    cur.close()
    return()
def add_user_function(fname,lname,username,passwrd,role):
    cur=con.cursor()
    r=random.randint(1,2000)
    cur.execute("INSERT INTO _user(userid,firstname,lastname,username,userpassword,userrole) VALUES (%s,%s,%s,%s,%s,%s)",[r,fname,lname,username,passwrd,role])
    cur.close()
    return()
def update_post(id,title,des):
    cur=con.cursor()
    cur.execute('UPDATE post SET postTitle=%s, postDescription=%s WHERE postid=%s',[title,des,id])
    cur.close()
    return()
def add_post_function(title,des,cat,slider,image):
    cur=con.cursor()
    iddd=0
    r=random.randint(1,2000)
    today = date.today()
    date1=today.strftime("%d/%m/%Y")
    cur.execute("INSERT INTO post(postid,postTitle,postDescription,postImage,slider,postDate,postCategory,postAuthor) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",[r,title,des,image,slider,date1,cat,session['id']])
    cur.close()
    return()

@app.route("/")
def Home():
    category=categories()
    posts=get_posts()
    return render_template('index.html',params=params,category=category,posts=posts)


@app.route('/apply',)
def Apply():
    cate=categories()
    return render_template('apply.html',params=params,category=cate)

@app.route('/about')
def About():
    cate=categories()
    return render_template('about.html',params=params,category=cate)

@app.route('/contact')
def contact():
    cate=categories()
    return render_template('Contact.html',params=params,category=cate)


@app.route('/news/<post_slug>')
def News_route(post_slug):
    category=categories()
    news=get_news(post_slug)
    posts=get_posts()
    return render_template('News.html',posts=posts,params=params,category=category,news=news)

@app.route('/category/<post_slug>')
def category(post_slug):
    category=categories()
    posts=get_news_by_category(post_slug)
    catimage=category_Image(post_slug)
    return render_template('category.html',catimage=catimage,params=params,category=category,posts=posts)

@app.route('/search',methods=['POST'])
def search_route():
    Term= request.form['search']
    category=categories()
    results=search(Term)
    posts=get_posts()
    return render_template('search.html',posts=posts,results=results,params=params,category=category,search_term=Term)


