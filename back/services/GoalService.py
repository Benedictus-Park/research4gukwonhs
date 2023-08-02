from ..dao.GoalDao import GoalDao
class GoalService:
    def __init__(self, dao:GoalDao):
        self.dao = dao