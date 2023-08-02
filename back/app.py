from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine

from dao.GoalDao import GoalDao
from dao.UserDao import UserDao
from services.GoalService import GoalService
from services.UserService import UserService

class Services:
    pass

DB_ID = "root"
DB_PWD = "0000"
DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "metastudy"

DB_URL = f"mysql+pymysql://{DB_ID}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

app = Flask(__name__)
CORS(app)

# Database Layer
engine = create_engine(DB_URL, encoding="utf-8")

# Persistence Layer
goaldao = GoalDao(engine)
userdao = UserDao(engine)

# Business Layer
services = Services()
services.goal = GoalService(goaldao)
services.user = UserService(userdao)

@app.route("/login", methods=["POST"])
def login():
    payload = request.get_json()

    email = payload['email']
    pwd = payload['pwd']