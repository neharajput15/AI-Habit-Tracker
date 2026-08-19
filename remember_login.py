import os

FILE_NAME = "remembered_user.txt"


def save_user(user_id):
    with open(FILE_NAME, "w") as file:
        file.write(str(user_id))


def get_saved_user():
    if not os.path.exists(FILE_NAME):
        return None

    try:
        with open(FILE_NAME, "r") as file:
            user_id = file.read().strip()

        if user_id:
            return int(user_id)

    except:
        return None

    return None


def clear_saved_user():
    if os.path.exists(FILE_NAME):
        os.remove(FILE_NAME)