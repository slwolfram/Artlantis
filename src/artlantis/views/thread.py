import os
import secrets
from flask import (Flask, Blueprint, abort, render_template, url_for, 
    flash, redirect, session, request, current_app)
from flask_login import login_required, current_user
from flask_mail import Mail, Message

from artlantis import db
from artlantis.forms import PostForm
from artlantis.models import Thread
from artlantis.views.helper_fns import save_picture

thread = Blueprint('thread', __name__, template_folder='templates')

@thread.route("/thread/new", methods=['GET', 'POST'])
@login_required
def new_thread():
    form = PostForm()
    if form.validate_on_submit():
        picture_file = None
        if form.picture.data:
            picture_dir = os.path.join(
                current_app.root_path, 'static/gallery_pics')
            picture_file = save_picture(form.picture.data, picture_dir)
        thread = Thread(title=form.title.data, 
                        image_file=picture_file, 
                        content=form.content.data, 
                        author=current_user)
        db.session.add(thread)
        db.session.commit()
        flash('Your thread has been created!', 'success')
        return redirect(url_for('mainhome'))
    return render_template('create_thread.html', title='New Thread', 
        form=form, legend='New Thread')

@thread.route("/thread/<int:thread_id>")
def get_thread(thread_id):
    thread = Thread.query.get_or_404(thread_id)
    return render_template('thread.html', title=thread.title, thread=thread)

@thread.route("/thread/<int:thread_id>/update", methods=['GET', 'POST'])
@login_required
def update_thread(thread_id):
    thread = Thread.query.get_or_404(thread_id)
    if thread.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        thread.title = form.title.data
        thread.content = form.content.data
        db.session.commit()
        flash('Your thread has been updated', 'success')
        return redirect(url_for('thread.get_thread', thread_id=thread.id))
    elif request.method == 'GET':
        form.title.data = thread.title
        form.content.data = thread.content
    return render_template('create_thread.html', title='Update Thread', 
        form=form, legend='Update Thread')

@thread.route("/thread/<int:thread_id>/delete", methods=['POST'])
@login_required
def delete_thread(thread_id):
    thread = Thread.query.get_or_404(thread_id)
    if thread.author != current_user:
        abort(403)
    db.session.delete(thread)
    db.session.commit()
    flash('Your thread has been deleted!', 'success')
    return redirect(url_for('home'))