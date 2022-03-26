DEFAULT_KEY_PREFIX = "winterfun"


def prefixed_key(f):
    def prefixed_method(self, *args, **kwargs):
        key = f(self, *args, **kwargs)
        return f"{self.prefix}:{key}"
    return prefixed_method


class key_schema:
    def __init__(self, prefix: str = DEFAULT_KEY_PREFIX):
        self.prefix = prefix

    @prefixed_key
    def hello_key(self) -> str:
        """
        The rendered hello key test.
        Format: winterfun:hello
        """
        return "hello"

    @prefixed_key
    def get_user_key(self, username) -> str:
        """
        The rendered profile based on the username.
        Format: winterfun:user:username
        """
        return f"user:{username}"

    @prefixed_key
    def my_friends_key(self, username) -> str:
        """
        The rendered friend list of my profile.
        Format: winterfun:profile:friends:username
        """
        return f"profile:friends:{username}"

    @prefixed_key
    def user_list_key(self) -> str:
        """
        The rendered all users from the model users
        Format: winterfun:user:all
        """
        return f"user:all"

    @prefixed_key
    def google_token(self, username) -> str:
        """
        The rendered all users from the model users
        Format: winterfun:google_token:username
        """
        return f"google_token:{username}"

    @prefixed_key
    def google_refresh_token(self, username) -> str:
        """
        The rendered all users from the model users
        Format: winterfun:google_refresh_token:username
        """
        return f"google_refresh_token:{username}"

    @prefixed_key
    def user(self) -> str:
        return "users:ids"

    @prefixed_key
    def profile_id(self, profile_id: int) -> str:
        return f"profile:{profile_id}"





def user_list_view():
    """
    User.objects.all()
    Format: user:list-view
    """
    return "user:list-view"


def my_profile_view():
    """

    Format: profile:my-profile-view
    """
    return "profile:my-profile-view:"
