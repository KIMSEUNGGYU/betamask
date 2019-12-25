import os
import sys
sys.path.append(os.path.abspath("/Users/SG/git/bitcoin"))


from flask import jsonify
from flask import request
# from flask_jwt import jwt_required
from models2 import Users, db
from . import api  # __init__ 에 있는 api
from develop.bitcoin_api.mnemonic import (make_mnemonic, get_bitcoin_address)

@api.route('/test')
def test():
    return jsonify()

@api.route('/user/create', methods=['POST'])
def create_user():
    if request.method == 'POST':
        data = request.get_json()
        password = data.get('password')

        bitcoin_address = get_bitcoin_address(password)
        mnemonic_code = make_mnemonic(password)

        print('비트코인 주소:', bitcoin_address)
        print('mnemonic_cde:', mnemonic_code)

        print('len', len(bitcoin_address))
        print('len', len(password))
        print('len', len(mnemonic_code))
        users = Users()
        users.address = bitcoin_address
        users.password = password
        users.mnemonic = mnemonic_code

        db.session.add(users)
        db.session.commit()

        # fcuser = Fcuser()
        #         fcuser.userid = userid
        #         fcuser.username = username
        #         fcuser.password = password

        return jsonify( {
            'mnemonic':mnemonic_code,
            'address': bitcoin_address
        }), 201

# @api.route('/users', methods=['GET', 'POST'])
# @jwt_required()
# def users():
#     if request.method == 'POST':
#         print('in POST')
#         data = request.get_json()
#         print('post data', data)
#         userid = data.get('userid')
#         username = data.get('username')
#         password = data.get('password')
#         re_password = data.get('re-password')
#
#         print('rr', userid, username, password, re_password)
#         if not (userid and username and password and re_password):
#             return jsonify({'error': 'No arguments'}), 400
#
#         if password != re_password:
#             return jsonify({'error': 'Wrong password'}), 400
#
#         fcuser = Fcuser()
#         fcuser.userid = userid
#         fcuser.username = username
#         fcuser.password = password
#
#         db.session.add(fcuser)
#         db.session.commit()
#
#         return jsonify(), 201
#
#     print('get')
#     # get 요청인 경우
#     users = Fcuser.query.all()
#     print('get2', [user.serialize for user in users])
#     print('get2', jsonify([user.serialize for user in users]))
#     return jsonify([user.serialize for user in users])
#
#
# @api.route('/users/register', methods=['POST'])
# def users_register():
#     if request.method == 'POST':
#         print('in POST')
#         data = request.get_json()
#         print('post data', data)
#         userid = data.get('userid')
#         username = data.get('username')
#         password = data.get('password')
#         re_password = data.get('re-password')
#
#         print('rr', userid, username, password, re_password)
#         if not (userid and username and password and re_password):
#             return jsonify({'error': 'No arguments'}), 400
#
#         if password != re_password:
#             return jsonify({'error': 'Wrong password'}), 400
#
#         fcuser = Fcuser()
#         fcuser.userid = userid
#         fcuser.username = username
#         fcuser.password = password
#
#         db.session.add(fcuser)
#         db.session.commit()
#
#         return jsonify(), 201
#
#     # get 요청인 경우
#     users = Fcuser.query.all()
#     return jsonify([user.serialize for user in users])
#
#
# @api.route('/users/<uid>', methods=['GET', 'PUT', 'DELETE'])
# def user_detail(uid):
#     if request.method == 'GET':
#         user = Fcuser.query.filter(Fcuser.id == uid).first()
#         return jsonify(user.serialize)
#     elif request.method == 'DELETE':
#         Fcuser.query.delete(Fcuser.id == uid)
#         return jsonify(), 204
#         # 성공을 의미하며, 앞으로 해당 컨텐츠 사용 불가 (204 - db 에서 삭제 했으므로)
#
#     # 데이터 가져오기
#     data = request.get_json()
#
#     print('data', data)
#     # userid = data.get('userid')
#     # username = data.get('username')
#     # password = data.get('password')
#
#     # updated_data = {}
#     # if userid:
#     #     updated_data['userid'] = userid
#     # if username:
#     #     updated_data['username'] = username
#     # if password:
#     #     updated_data['password'] = password
#
#     Fcuser.query.filter(Fcuser.id == uid).update(data)
#     user = Fcuser.query.filter(Fcuser.id == uid).first()
#     return jsonify(user.serialize)
