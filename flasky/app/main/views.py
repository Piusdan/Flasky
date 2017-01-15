from datetime import datetime
from flask import render_template, session, redirect, url_for, abort
from flask.ext.login import logout_user, login_required
from . import main
from .forms import NameForm
from .. import db
from ..models import User
from ..email import send_email


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            session['known'] = False
            if main.config['FLASKY_ADMIN']:
                send_email(main.config['FLASKY_ADMIN'],
                           'New User', 'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('.index'))
    return render_template('index.html',
                           form=form, name=session.get
                           ('name'), known=session.get('known', False))


@main.route('/user/<username>')
def user(username):
    app_user = User.query.filter_by(username=username).first()
    if app_user is None:
        abort(404)
    return render_template('user.html', user=app_user)