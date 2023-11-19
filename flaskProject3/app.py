import logging
import pymysql
from flask import Flask, render_template, request, jsonify, redirect, session
# from register import register_user  # 从 register 模块中导入 register_user 函数
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_migrate import Migrate
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 设置一个用于加密 session 的密钥

# MYSQL的主机名
HOSTNAME = "127.0.0.1"
# MySQL监听的端口号
PORT = 3306
# 连接MySQL的用户名
USERNAME = "root"
# 密码
PASSWORD = "18060922680"
# mysql数据库名称
DATABASE = "database_learn"


# 其它路由和视图函数...
#在app.config中设置好连接的数据库的信息
#
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
db = SQLAlchemy(app)

migrate = Migrate(app, db)

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # historys = db.relationship("History", back_populates = "user")

class History(db.Model):
    __tablename__ = "history"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time_ans = db.Column(db.String(200), nullable=False)
    content_ans = db.Column(db.String(200), nullable=False)
    # 外键
    history_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # history = db.relationship("User", back_populates = "historys")
    history_user = db.relationship("User", backref="historys")
# history = History(time_ans = "202311190937", content_ans = "4458")
# print(history.title)
# 获取该用户所有历史


# user = User(username = "oyzy", password = "832101319")
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
    return render_template('calculator.html')
##################################
@app.route('/register', methods=['POST'])
def add_user():
    username = request.form['username']
    password = request.form['password']
    # 检查用户名是否已经存在
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return "用户名已经被注册，请选择其他用户名"
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    return "注册成功！"
@app.route('/', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # 查询数据库中是否存在匹配的用户名和密码
    user = User.query.filter_by(username=username).first()
    if user:
        if user.password == password:
            session['username'] = username  # 将用户名存入 session
            return redirect('/calculator')  # 登录成功，跳转到 calculator 页面
        else:
            return render_template('login.html', error="密码错误")  # 密码错误，重新渲染登录页面并显示错误信息
    else:
        return redirect('/register')  # 用户不存在，跳转到注册页面


@app.route('/user/query')
def query_user():
    # 1.get查找
    # user = User.query.get(1)
    # print(f"{user.id}:{user.username}-{user.password}")
    # 2.fifilter_by查找
    users = User.query.filter_by(username = "oyzy")
    # print(type(users)) # Query对象
    return "查询成功！"

@app.route('/user/update')
def update_user():
    user = User.query.filter_by(username="法外狂徒oyzy").first()
    user.password = "21126364"
    db.session.commit()
    return "修改上传成功！"


@app.route('/user/delete')
def delete_user():
    # get查找
    user = User.query.get(1)
    db.session.delete(user)
    db.session.commit()
    return "删除成功！"

##############################
@app.route('/history/add')
def add_history():
    history = History(time_ans = "202311190937", content_ans = "4458")
    history.history_user = User.query.get(2)
    # db.session.add_all(history)
    db.session.add(history)
    db.session.commit() # 同步
    return "计算答案添加成功！"

@app.route('/history/query')
def query_history():
    # 1.get查找
    user = User.query.get(2)
    for history in user.historys:
        print(history.time_ans)
    return "历史查询成功！"

if __name__ == '__main__':
    app.run()

# flask db init一次/migrate/upgrade