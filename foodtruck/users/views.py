from flask import Blueprint, request, render_template, redirect, url_for
from flask.ext.login import login_user

from foodtruck.data import db
from .models import User
from .forms import LoginForm

users = Blueprint('users', __name__)

@users.route('/login', methods=['POST'])
def login():
  login_form = LoginForm(request.form)
  return render_template('auth/login.html', form=login_form)

