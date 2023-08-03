from flask import Response, jsonify

class GoalService:
    def __init__(self, dao):
        self.dao = dao

    def add_goal_service(self, uid:int, goal:str) -> Response:
        if self.dao.insert_goal(uid, goal):
            return Response(status=200)
        else:
            return Response(status=500)
        
    def goal_completion_feat_han_river(self, idx:int, uid:int) -> Response:
        if self.dao.complete_goal(idx, uid):
            return Response(status=200)
        else:
            return Response(status=500)
        
    def get_all_goals(self, uid:int):
        return self.dao.get_goals(uid)