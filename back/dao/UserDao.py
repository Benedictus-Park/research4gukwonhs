from sqlalchemy.engine import Engine

class UserDao:
    def __init__(self, engine:Engine):
        self.engine = engine

    # 유저 삽입, 유저 인출, 공부시간 업데이트 기능 필요. 유저 삽입 시 중복이메일/유저네임 거르기.
    # 유저 삽입 성공 여부는 삽입 후 유저 조회가 되는지 여부로 확인. 조회 안 되면 None이 튀어나옴.