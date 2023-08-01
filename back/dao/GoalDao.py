from sqlalchemy.engine import Engine

class GoalDao:
    def __init__(self, engine:Engine):
        self.engine = engine

    # 목표 등록, 목표 달성, 목표 열람 기능 필요.