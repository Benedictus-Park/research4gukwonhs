from sqlalchemy.engine import Engine

class GoalDao:
    def __init__(self, engine:Engine):
        self.engine = engine

    def insert_goal(self, uid:int, goal:str) -> bool:
        param = {
            "uid":uid,
            "goal":goal
        }

        sql = "SELECT COUNT(*) FROM goals"
        flag_success = int(self.engine.execute(sql)[0])

        sql = f"INSERT INTO goals(uid, goal) VALUES(:uid, :goal)"
        self.engine.execute(sql, param)

        sql = "SELECT COUNT(*) FROM goals"
        flag_success -= int(self.engine.execute(sql)[0])

        return False if flag_success else True

    def complete_goal(self, idx:int, uid:int) -> bool:
        param = {
            "idx":idx,
            "uid":uid
        }

        sql = "SELECT COUNT(*) FROM goals WHERE idx=:idx AND uid=:uid AND completed=TRUE"
        flag_success = int(self.engine.execute(sql, param)[0])

        sql = "UPDATE goals SET completed=TRUE WHERE idx=:idx AND uid=:uid"
        self.engine.execute(self.engine.execute(sql, param))

        sql = "SELECT COUNT(*) FROM goals WHERE idx=:idx AND uid=:uid AND completed=TRUE"
        flag_success -= int(self.engine.execute(sql, param)[0])

        return False if flag_success else True

    def get_goals(self, uid:int) -> tuple:
        result = []

        sql = f"SELECT idx, goal, completed FROM goals WHERE uid={uid}"
        records = self.engine.execute(sql)

        for row in records:
            result.append({
                "idx":row['idx'],
                "goal":row['goal'],
                "completed":row['completed']
            })
        
        return tuple(result)