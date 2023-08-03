import jwt
from functools import wraps
from flask_cors import CORS
from flask import Flask, request, Response, g, jsonify
from sqlalchemy import create_engine

from dao.GoalDao import GoalDao
from dao.UserDao import UserDao
from services.GoalService import GoalService
from services.UserService import UserService

from config import *

DB_URL = f"mysql+pymysql://{DB_ID}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

app = Flask(__name__)
CORS(app)

# Database Layer
engine = create_engine(DB_URL, encoding="utf-8")

# Persistence Layer
goaldao = GoalDao(engine)
userdao = UserDao(engine)

# Business Layer
goal_service = GoalService(goaldao)
user_service = UserService(userdao, JWT_SECRET_KEY)

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get("token")

        if token is None:
            return Response("잘못된 접근이거나, 로그인이 만료되었습니다.", 401)
        else:
            try:
                payload = jwt.decode(token, JWT_SECRET_KEY, 'HS256')
            except jwt.InvalidTokenError:
                return Response("잘못된 접근이거나, 로그인이 만료되었습니다.", 401)
            
            g.uid = payload['uid']

        return f(*args, **kwargs)
    return wrapper
        

@app.route("/login", methods=["POST"])
def login():
    payload = request.get_json()

    email = payload['email']
    pwd = payload['pwd']

    return user_service.login_service(email, pwd)

@app.route("/registration", methods=["POST"])
def registration():
    payload = request.get_json()

    username = payload['uname']
    email = payload['id']
    pwd = payload['pwd']

    return user_service.registration_service(username, email, pwd)

@app.route("/sync-profile", methods=["POST"])
@login_required
def sync_userdata():
    secs = request.get_json()['secs']
    user_service.studied_time_service_add(g.uid, secs)

    return jsonify({
        "studied_time":user_service.studied_time_service_get(g.uid),
        "goals":goal_service.get_all_goals(g.uid)
    })

@app.route("/add-goal", methods=["POST"])
@login_required
def add_goal():
    goal = request.get_json()['goal']
    return goal_service.add_goal_service(g.uid, goal)

@app.route("/goal-completion", methods=["POST"])
@login_required
def goal_complete():
    idx = request.get_json()['idx']
    return goal_service.goal_completion_feat_han_river(idx, g.uid)

app.run(host="127.0.0.1", port=4444, debug=True)