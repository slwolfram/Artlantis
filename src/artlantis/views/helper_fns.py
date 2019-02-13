import os
import secrets
from PIL import Image
from flask_mail import Message

from artlantis import mail

def save_picture(form_picture, picture_dir):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(picture_dir, picture_fn)
    
    if picture_dir == 'static/profile_pics':
        output_size = (125, 125)
    else:
        output_size = (800, 800)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def send_mail(recipients, sender, subject, body):
    msg = Message(
        subject, body=body, sender=sender, recipients=recipients)
    mail.send(msg)