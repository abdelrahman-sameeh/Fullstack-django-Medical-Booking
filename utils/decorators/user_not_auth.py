from authentication.models import User


def user_not_authenticated(user: User):
    return not user.is_authenticated