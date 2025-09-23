from fastapi_users import FastAPIUsers

from app.db.models import User
from app.db.types import UserIdType

from app.api.dependencies.authentication import get_user_manager
from app.api.dependencies.authentication import authentication_backend

fastapi_users = FastAPIUsers[User, UserIdType](
    get_user_manager,
    [authentication_backend],
)

current_active_user = fastapi_users.current_user(active=True)
current_active_superuser = fastapi_users.current_user(active=True, superuser=True)
