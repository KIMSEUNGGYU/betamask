import os
from flask import Flask
from flask import render_template
from flask import request, jsonify
from flask_jwt import JWT
from models import Users, db
from api_v2 import api as api_v2
from develop.bitcoin_api.mnemonic import (make_mnemonic, get_bitcoin_address)
from develop.bitcoin_api.transaction import get_total_money
#

app = Flask(__name__)

# app.register_blueprint(api_v1, url_prefix="/api/v1")
app.register_blueprint(api_v2, url_prefix="/api/v2")

@app.route('/main/<address>', methods=['GET'])
def main(address):
    total_money = get_total_money(address)
    print('total_money', total_money)

    data_object = {
        'address': address,
        'value': total_money
    }

    return render_template('main.html', data=data_object)


@app.route('/mnemonic/<address>', methods=['GET'])
def user_detail(address):
    if request.method == 'GET':
        mnemonic_code = make_mnemonic(address)

        return render_template('mnemonic.html', mnemonic_code=mnemonic_code)

@app.route('/mnemonic')
def mnemonic():
    return render_template('mnemonic.html')

@app.route('/update')
def update():
    return render_template('update.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        data = request.get_json()
        password = data['password']

        print('password', password)
        user = Users.query.filter(Users.password == password).first()
        print('user', user)

        if user == None:
            return jsonify(), 202         # 값은 수신했지만, 올바른 값 없음

        return jsonify({'data': user.serialize['address']}), 200

    return render_template('signin.html')

@app.route('/')
def index():
    return render_template('index.html')


# config

basedir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basedir, 'db_user.sqlite')

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
