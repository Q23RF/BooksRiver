from flask import Flask, render_template, request, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import os

app = Flask(__name__)
app.secret_key = os.environ['secret_key']
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = '請先登入！'

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(使用者):
    if 使用者 not in users:
        return

    user = User()
    user.id = 使用者
    return user

@login_manager.request_loader
def request_loader(request):
    使用者 = request.form.get('user_id')
    if 使用者 not in users:
        return

    user = User()
    user.id = 使用者
    user.is_authenticated = request.form['password'] == users[使用者]['password']

    return user

users = {'Me': {'password': 'myself'}}

@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template("login.html")

	使用者 = request.form['user_id']
	if (使用者 in users) and (request.form['password'] == users[使用者]['password']):
		user = User()
		user.id = 使用者
		login_user(user)
		flash('welcome!')
		return redirect(url_for('home'))
	flash('login failed!')
	return render_template('login.html')

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/home')
@login_required
def home():
	return "home"

app.run(host='0.0.0.0', port=81)
