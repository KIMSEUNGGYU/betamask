import os
path = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0] # 상위 디렉토리 추출
path = os.path.split(path)[0]                                       # 상위 디렉토리 추출
path = os.path.split(path)[0]                                       # 상위 디렉토리 추출

import sys
# sys.path.append(os.path.abspath("/Users/SG/git/bitcoin"))
sys.path.append(os.path.abspath(path))

# print('pathsss', path)

from flask import jsonify
from flask import request
# from flask_jwt import jwt_required
from models import Users, db
from . import api  # __init__ 에 있는 api
from develop.bitcoin_api.mnemonic import (make_mnemonic, get_bitcoin_address)

@api.route('/test')
def test():
    return jsonify()

@api.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        data = request.get_json()
        password = data.get('password')
        mnemonic = data.get('mnemonic')

        query_result = Users.query.filter(Users.mnemonic == mnemonic).first()

        ## 올바르지 않는 경우
        if query_result == None:
            return jsonify(), 202       # 값은 수신했지만, 올바른 값 없음

        data = query_result.serialize

        ## 올바른 경우 - 업데이트 진행

        print('data', data)

        data['password'] = password

        print('data', data)
        Users.query.filter(Users.mnemonic == mnemonic).update(data)

        return jsonify(), 200
        # print('password', password)
        # print('mnemonic', mnemonic)

@api.route('/user/create', methods=['POST'])
def create_user():
    if request.method == 'POST':
        data = request.get_json()
        password = data.get('password')

        bitcoin_address = get_bitcoin_address(password)
        mnemonic_code = make_mnemonic(bitcoin_address)

        users = Users()
        users.address = bitcoin_address
        users.password = password
        users.mnemonic = mnemonic_code

        filter_result = Users.query.filter(Users.address == bitcoin_address).first()

        # 가입이 가능할 경우
        if filter_result == None:
            print("DB 에 저장")
            db.session.add(users)
            db.session.commit()
            return jsonify( {
                'address':bitcoin_address,
            }), 201

        ## 가입이 불가
        return jsonify(), 500

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
