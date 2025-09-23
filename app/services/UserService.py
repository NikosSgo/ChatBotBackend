from sqlalchemy.orm import Session


class UserService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.crud_user = None

    def create_user():
        pass

    def get_user_by_id():
        pass

    def update_user_by_id():
        pass

    def delete_user_by_id():
        pass
