import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL配置
HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = "root"
PASSWORD = "18060922680"
DATABASE = "database_learn"

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    history = db.relationship("History", backref="user", lazy="dynamic")

class History(db.Model):
    __tablename__ = "history"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time_ans = db.Column(db.String(200), nullable=False)
    content_ans = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class Rate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    principal = db.Column(db.Float)
    rate = db.Column(db.Float)
    time = db.Column(db.Float)
    compound_frequency = db.Column(db.Float)
    simple_interest = db.Column(db.Float)
    compound_interest = db.Column(db.Float)
    total_amount = db.Column(db.Float)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('registry_database.html')

@app.route('/calculator')
def calculator():
    if 'username' in session:
        return render_template('calculator.html', username=session['username'])
    else:
        return redirect('/')

@app.route('/rate')
def rate():
    if 'username' in session:
        return render_template('rate.html', username=session['username'])
    else:
        return redirect('/')

@app.route('/register', methods=['POST'])
def add_user():
    # 注册新用户
    username = request.form['username']
    password = request.form['password']
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return "用户名已经被注册，请选择其他用户名"
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return "注册成功！"

@app.route('/', methods=['POST'])
def login():
    # 用户登录
    username = request.form['username']
    password = request.form['password']
    user = User.query.filter_by(username=username).first()
    if user:
        if user.password == password:
            session['username'] = username
            return redirect('/calculator')
        else:
            return render_template('login.html', error="密码错误")
    else:
        return redirect('/register')

@app.route('/save_history', methods=['POST'])
def save_history():
    # 存储历史记录
    if 'username' in session:
        data = request.get_json()
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        content_ans = data.get('content_ans')
        user = User.query.filter_by(username=session['username']).first()
        history = History(time_ans=time_now, content_ans=content_ans, user_id=user.id)
        db.session.add(history)
        db.session.commit()
        return "History saved successfully"
    else:
        return "User not logged in"

@app.route('/history')
def history():
    # 获取历史记录
    user_id = session.get('user_id')  # 假设用户ID存在于session中
    history = History.query.filter_by(user_id=user_id).all()
    return render_template('history.html', history=history)

if __name__ == '__main__':
    app.run()
