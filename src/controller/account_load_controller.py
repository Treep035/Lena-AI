from model.account.account_load import account_picture_load, account_username_load

def account_picture_load_controller():
        user_image_path = account_picture_load()
        return user_image_path

def account_username_load_controller():
        username = account_username_load()
        return username