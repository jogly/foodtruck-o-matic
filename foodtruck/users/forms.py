from wtforms import Form, TextField, PasswordField, validators

class LoginForm(Form):
  email = TextField('Email', [validators.Email(), validators.Length(-1, 64)])
  password = PasswordField('Password', [validators.Required(), validators.Length(8, 32)])
