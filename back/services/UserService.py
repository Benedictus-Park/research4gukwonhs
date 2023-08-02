import jwt
import bcrypt
import datetime
from flask import jsonify, Response

from ..dao.UserDao import *

class UserService:
    def __init__(self, dao:UserDao, JWT_SECRET_KEY:str):
        self.dao = dao
        self.JWT_SECRET_KEY = JWT_SECRET_KEY

    def check_token(self, token:str) -> int:
        uid = None

        try:
            uid = int(jwt.decode(token, self.JWT_SECRET_KEY, 'HS256')['uid'])
        except jwt.InvalidTokenError:
            return -1
        
        return uid
    
    def registration_service(self, username:str, email:str, pwd:str) -> Response:
        hashed_pwd = bcrypt.hashpw(pwd.encode(), bcrypt.gensalt()).decode('utf-8')

        result = self.dao.insert_user(username, email, hashed_pwd)

        if result == INSERT_SUCCESS:
            return Response("회원가입 성공!", 200)
        elif result == INSERT_DUPLICATE_UNAME:
            return Response("이미 사용중인 유저명이에요.", 400)
        elif result == INSERT_DUPLICATE_EMAIL:
            return Response("이미 사용중인 이메일이에요.", 400)
        else:
            return Response("알 수 없는 오류가 발생했어요.", 500)

    def login_service(self, email:str, pwd:str) -> Response:
        user = self.dao.get_user(email)

        if user == None:
            return Response("로그인 정보가 틀렸어요.", 401)
        elif not bcrypt.checkpw(pwd.encode('utf-8'), user['hashed_pwd'].encode('utf-8')):
            return Response("로그인 정보가 틀렸어요.", 401)
        
        access_token = jwt.encode({
            'uid':user['uid']
        }, self.JWT_SECRET_KEY, 'HS256', )

        return jsonify({
            'exp':datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'uname':user['username'],
            'token':access_token
        })