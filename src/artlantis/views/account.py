import os
from flask import (Blueprint, current_app, flash, redirect, 
    request, render_template, url_for)
from flask_login import current_user, login_required
from artlantis import db
from artlantis.forms import UpdateAccountForm
from artlantis.models import User, Thread
from artlantis.views.helper_fns import save_picture

account = Blueprint(
    'account', __name__, template_folder='templates')

@account.route("/account", methods=['GET', 'POST'])
@login_required
def user_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_dir = os.path.join(
                current_app.root_path, 'static/profile_pics')
            picture_file = save_picture(form.picture.data, picture_dir)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account.user_account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for(
        'static', filename='profile_pics/' + current_user.image_file)
    return render_template(
        'account.html', title='Account', image_file=image_file, form=form)

@account.route("/user/<string:username>")
def user_threads(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    threads = Thread.query.filter_by(author=user) \
        .order_by(Thread.date_posted.desc()) \
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', threads=threads, user=user)

