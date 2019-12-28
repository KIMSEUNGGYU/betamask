import os
from flask import Flask
from flask import render_template
from flask import request, jsonify
from sqlalchemy import desc
from models import Users, db
from tx_models import Tx_history, db2
from api_v2 import api as api_v2
from develop.bitcoin_api.mnemonic import make_mnemonic
from develop.bitcoin_api.transaction import get_total_money

app = Flask(__name__)

SATOSHI = 100000000
app.register_blueprint(api_v2, url_prefix="/api/v2")

@app.route('/main/<address>', methods=['GET'])
def main(address):
    total_money = get_total_money(address)
    total_money /= SATOSHI


    # tx_history = Tx_history()

    ## sql 내림차순
    history = Tx_history.query.filter(Tx_history.address == address).order_by(desc(Tx_history.id)).all()
    # print('history', history.serialize)

    print(len(history))
    # user = Users.query.filter(Users.fake_password == password).first()

    history_length = len(history)
    if history_length > 5:
        history_length = 5

    result = []
    for i in range(history_length):
        result.append(history[i].serialize['tx'])

    # print('result', result)

    data_object = {
        'address': address,
        'value': total_money,
        'historys': result

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
        user = Users.query.filter(Users.fake_password == password).first()
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
dbfile2 = os.path.join(basedir, 'txs.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
app.config['SQLALCHEMY_BINDS'] = {
    'test2': 'sqlite:///' + dbfile,
    'test1': 'sqlite:///' + dbfile2
}
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'gyu12345'

db.init_app(app)
db.app = app
db.create_all()

db2.init_app(app)
db2.app = app
db2.create_all()


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
