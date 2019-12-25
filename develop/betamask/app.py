import os
from flask import Flask
from flask import render_template
from flask_jwt import JWT
# from models import Fcuser, db
from models2 import Users, db
from api_v2 import api as api_v2
app = Flask(__name__)

# app.register_blueprint(api_v1, url_prefix="/api/v1")
app.register_blueprint(api_v2, url_prefix="/api/v2")

## api_betamast
# @app.route('/first')
# def first():
#     return render_template('first-page.html')
#
# @app.route('/signup')
# def signup():
#     return render_template('signup-page.html')
#
# # api
# @app.route('/register')
# def register():
#     return render_template('test/register.html')
#
#
# @app.route('/login')
# def login():
#     return render_template('test/login.html')
#
@app.route('/mnemonic')
def mnemonic():
    return render_template('mnemonic.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/')
def index():
    return render_template('index.html')


# config

basedir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basedir, 'db2.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'gyu12345'

db.init_app(app)
db.app = app
db.create_all()


# def authenticate(username, password):
#     # 인증하는 부분을 함수로 만들어야함. JWT 는
#     # 플라크스에서 JWT 는 userid 가 아닌 username 을 사용하게 되어 있음
#     user = Fcuser.query.filter(Fcuser.userid == username).first()
#
#     if user.password == password:
#         return user
#
#
# def identity(payload):
#     # 복호화 과정? JWT
#     userid = payload['identity']
#     return Fcuser.query.filter(Fcuser.id == userid).first()


# jwt = JWT(app, authenticate, identity)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
