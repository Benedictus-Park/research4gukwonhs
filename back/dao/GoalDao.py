from sqlalchemy.sql import text
from sqlalchemy.engine import Engine

class GoalDao:
    def __init__(self, engine:Engine):
        self.engine = engine

    def insert_goal(self, uid:int, goal:str) -> bool:
        param = {
            "uid":uid,
            "goal":goal
        }

        sql = f"INSERT INTO goals(uid, goal) VALUES(:uid, :goal)"
        self.engine.execute(text(sql), param)

        sql = "SELECT COUNT(*) FROM goals WHERE uid=:uid AND goal=:goal"
        return bool(self.engine.execute(text(sql), param))

    def complete_goal(self, idx:int, uid:int) -> bool:
        param = {
            "idx":idx,
            "uid":uid
        }

        sql = "UPDATE goals SET completed=TRUE WHERE idx=:idx AND uid=:uid"
        self.engine.execute(text(sql), param)

        sql = "SELECT COUNT(*) FROM goals WHERE idx=:idx AND uid=:uid AND completed=TRUE"
        return bool(self.engine.execute(text(sql), param))

    def get_goals(self, uid:int) -> dict:
        result = []

        sql = f"SELECT idx, goal, completed FROM goals WHERE uid={uid}"
        records = self.engine.execute(text(sql))

        for row in records:
            result.append({
                "idx":row['idx'],
                "goal":row['goal'],
                "completed":row['completed']
            })
        
        return {
            "count":len(result),
            "records":result
        }