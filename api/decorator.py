from api.exceptions import NotAuthorizedError


def auth_required(func):
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except NotAuthorizedError:
            self.auth()
            return func(self, *args, **kwargs)

    return wrapper
