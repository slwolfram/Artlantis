from flask import (
    Blueprint, redirect, request, render_template)

from artlantis.models import Thread

main = Blueprint('main', __name__, template_folder='templates')

@main.route("/")
@main.route("/home")
def home():
    return render_template('home.html', title='Home')

@main.route("/about")
def about():
    return render_template('about.html', title='About')

@main.route("/gallery")
def gallery():
    page = request.args.get('page', 1, type=int)
    threads = Thread.query.order_by(Thread.date_posted.desc()) \
        .paginate(page=page, per_page=10)
    return render_template('gallery.html', threads=threads)

@main.route("/courses")
def courses():
    return render_template('courses.html', title='Courses')

@main.route("/contact")
def contact():
    return render_template('contact.html', title='Contact Us')

@main.route("/events")
def events():
    return render_template('events.html', title='Events')

"""
@main.route("/events/new")
@login_required
def new_event():
    if current_user.role == 'USER':
        return current_app.login_manager.unauthorized()
    form = EventForm()
    if form.validate_on_submit():
        event = Event(title=form.title.data, 
                    content=form.content.data, author=current_user)
        db.session.add(event)
        db.session.commit()
        flash('Your event has been created!', 'success')
        return redirect(url_for('events'))
    return render_template('create_event.html', title='New Event', 
        form=form, legend='New Event')
"""
