from flask import Blueprint
from flask import render_template, url_for,flash, redirect, request, abort, send_from_directory, make_response
from tasty import db, bcrypt, mail
from tasty.models import User, Post,Product, Boisson, Food
from werkzeug import secure_filename
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from tasty.Blog.forms import AddPost
from tasty.Blog.utils import save_picture_carte
import pandas as pd
import secrets
import os
from datetime import timedelta
import math
import json
from flask import jsonify
import datetime
######### LOADING BDD ########
#exec(open(os.getcwd() + '/tasty/MongoConnection/Functions_Mongo.py').read())
#exec(open('MongoConnection/Functions_Mongo.py').read())

### Acces to the DB ####
#db_mongo  = Get_MongoDB()
#ColNames = db_mongo.collection_names()
#ColNames.sort()

blog = Blueprint('blog',__name__)

@blog.route("/allblog")
def allblog():
    post = Post.query.all()
    return render_template('Blog/all_blog.html',post=post)

# creer une boisson :
@blog.route("/blog/add_blog",  methods=['GET','POST'])
#@login_required
def addpost():
    form = AddPost()
    if form.validate_on_submit():
        post = Post(image_file = save_picture_carte(form.picture.data),title=form.title.data, details = form.details.data, content=form.content.data)
        db.session.add(post)
        db.session.commit()
        flash('post ajoutée','success')
        return redirect(url_for('blog.addpost'))
    return render_template('Blog/add_post.html', title = 'Ajouter un post', form =form)



#update prod
#@login_required
@blog.route("/blog/<int:blog_id>/update", methods=['GET','POST'])
def update_post(blog_id):
    post = Post.query.get_or_404(blog_id)
    form = AddPost()
    if form.validate_on_submit():
        if form.picture.data != None:
            post.image_file = save_picture_carte(form.picture.data)
        post.title = form.title.data
        post.content =form.content.data
        post.details =form.details.data
        db.session.commit()
        flash('Post modifié','success')
        return redirect(url_for('blog.allblog'))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.details.data = post.details
        form.picture.data = post.image_file
    return render_template('Blog/add_post.html', title = 'modifier un post', form =form)


# Delete prod
#@login_required
@blog.route("/blog/<int:blog_id>/delete", methods=['GET','POST'])
def delete_post(blog_id):
    post = Post.query.get_or_404(blog_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post effacé', 'success')
    return redirect(url_for('blog.allblog'))
