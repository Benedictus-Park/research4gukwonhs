from sqlalchemy.sql import text
from sqlalchemy.engine import Engine

class UserDao:
    def __init__(self, engine:Engine):
        self.INSERT_SUCCESS = 1
        self.INSERT_DUPLICATE_UNAME = 2
        self.INSERT_DUPLICATE_EMAIL = 3
        self.INSERT_UNSPECIFIED_ERR = 4
        self.engine = engine

    def insert_user(self, username:str, email:str, hashed_pwd:str) -> int:
        # CODE 1 -> 성공
        # CODE 2 -> 중복 유저명
        # CODE 3 -> 중복 이메일
        # CODE 4 -> Error, unspecified

        param = {
            "username":username,
            "email":email,
            "hashed_pwd":hashed_pwd,
        }

        sql = "SELECT COUNT(*) FROM users WHERE username=:username"
        if int(self.engine.execute(text(sql), param).fetchone()[0]):
            return self.INSERT_DUPLICATE_UNAME
        
        sql = "SELECT COUNT(*) FROM users WHERE email=:email"
        if int(self.engine.execute(text(sql), param).fetchone()[0]):
            return self.INSERT_DUPLICATE_EMAIL
        
        sql = "INSERT INTO users(username, email, hashed_pwd) VALUES(:username, :email, :hashed_pwd)"
        self.engine.execute(text(sql), param)

        sql = "SELECT COUNT(*) FROM users WHERE username=:username AND email=:email"
        if int(self.engine.execute(text(sql), param).fetchone()[0]) == 0:
            return self.INSERT_UNSPECIFIED_ERR
        
        return self.INSERT_SUCCESS

    def get_user(self, email:str) -> dict:
        param = {
            "email":email
        }

        sql = "SELECT uid, username, hashed_pwd, studied_time FROM users WHERE email = :email"
        record = self.engine.execute(text(sql), param).fetchone()

        return {
            "uid":record['uid'],
            "username":record['username'],
            "hashed_pwd":record['hashed_pwd'],
            "studied_time":record['studied_time']
        } if record else None

    def get_studiedtime(self, uid:int) -> int:
        param = {
            "uid":uid
        }

        sql = "SELECT studied_time FROM users WHERE uid=:uid"
        studied_time = self.engine.execute(text(sql), param).fetchone()

        return studied_time[0] if studied_time or studied_time == 0 else -1
    
    def add_studiedtime(self, uid:int, secs:int) -> bool:
        studied_time = self.get_studiedtime(uid)
        param = {
            "uid":uid,
            "studied_time":studied_time + secs
        }

        if param["studied_time"] == -1:
            return False
        
        sql = "UPDATE users SET studied_time=:studied_time WHERE uid=:uid"
        self.engine.execute(text(sql), param)

        return True