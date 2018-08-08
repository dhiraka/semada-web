from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from .forms import SignInForm
from myapp.oauth2.oauth2client import OAuth2Client

from . import main

from myapp.models.db_models import User


# decorators to register functions as handlers for events

# http://localhost:5000/
@main.route('/')
def index():
    form = SignInForm()

    # HTTP POST
    if form.validate_on_submit():
        # # Validate and sign in the user.
        user = User.query.filter_by(
            email_address=form.email_address.data).first()
        if (user is not None and user.verify_password(form.password.data)):
            # Flask-Login login_user() function to record the user is logged in
            # for the user session.
            login_user(user)
            flash('Signed in successfully.', 'info')
            # Post/Redirect/Get pattern, so a redirect but two possible
            # destinations. The next query string argument is used when
            # the login form was used to prevent unauthorized access.
            return redirect(request.args.get('next') or url_for('api.overview'))

        flash('Invalid username or password.', 'error')
        # Return back to homepage

    # HTTP GET
    return render_template(
        'oauth2/oauth2.html',
        title='Sign in to continue - Semada',
        form=form)
    # return render_template('main/index.html', title='Welcome to Semada')
