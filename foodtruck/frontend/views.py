from flask import Blueprint, render_template

vis = Blueprint('vis', __name__, template_folder='templates', static_folder='static', static_url_path='/static/vis')

@vis.route('/', methods=['GET'])
def index():
  return render_template('index.html')
