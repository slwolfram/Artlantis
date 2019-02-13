from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin
import enum

from artlantis import app, db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Role(enum.Enum):
    ADMIN = 'Administrator',
    OWNER = 'Owner',
    MOD = 'Moderator',
    USER = 'User'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(
        db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='USER')
    threads = db.relationship('Thread', backref='author', lazy=True)
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User( \
            '{self.username}', '{self.email}', '{self.image_file}')'"

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    image_file = db.Column(db.String(20))
    date_posted = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    cat = db.Column(db.String(20), nullable=False, default='None')
    subcat = db.Column(db.String(20), nullable=False, default='None')

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)

    posts = db.relationship("Post")
    def __repr__(self):
        return f"Thread('{self.title}', '{self.date_posted}'"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image_file = db.Column(db.String(20))
    date_posted = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)

    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'))
    thread = db.relationship("Thread", backref="post")

    replies = db.relationship("Reply")

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}'"

class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    image_file = db.Column(db.String(20))
    date_posted = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)

    user_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship("Post", backref="reply")

    def __repr__(self):
        return f"Reply('{self.title}', '{self.date_posted}'"

