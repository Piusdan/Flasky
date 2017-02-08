from flask.ext.mail import Message
from threading import Thread
from flask import render_template
from flask import current_app
from . import mail


def send_email(to, subject, template, **kwargs):
    msg = Message(current_app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=current_app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    with current_app.app_context():
        mail.send(msg)
    # thr = Thread(target=send_async_email, args=[current_app, msg])
    # thr.start()
    # return thr


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)
