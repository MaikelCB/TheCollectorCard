class Session:
    logged_in = False
    user_name = ""

    @classmethod
    def login(cls, user_name):
        cls.logged_in = True
        cls.user_name = user_name

    @classmethod
    def logout(cls):
        cls.logged_in = False
        cls.user_name = ""
