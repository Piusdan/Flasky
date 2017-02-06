from flask import render_template, redirect, request, url_for, flash, current_app
from flask.ext.login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User
from . forms import LoginForm, RegistrationForm
from .. import db
from .. email import send_email
from .. send import AfricasTalking


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid usernam or password')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=form.password.data,
                    phonenumber=form.phonenumber.data,
                    email=form.email.data)
        db.session.add(user)
        flash('You can now login')
        db.session.commit()
        token = user.generate_confirmation_token()
        # AT = AfricasTalking(message=token, phonenumber=form.phonenumber.data)
        # AT.send_sms()
        send_email(user.email, 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)
        flash('A confirmation message has been sent to you by email')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and request.endpoint[:5] != 'auth.':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect('main.index')
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    mail = current_user.email
    # phonenumber = current_user.phonenumber
    token = current_user.generate_confirmation_token()
    send_email(to=current_user.email, template='auth/email/confirm',
               subject='Confirm Your Account',
               user=current_user, token=token)
    # AT = AfricasTalking(message=token, phonenumber=phonenumber)
    # AT.send_sms()
    flash('A new confirmation message has been sent to via email to ' + mail)
    return redirect(url_for('main.index'))