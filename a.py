import bcrypt

try:
    print(bcrypt.__about__.__version__)
except AttributeError:
    print("bcrypt does not have the attribute '__about__'")