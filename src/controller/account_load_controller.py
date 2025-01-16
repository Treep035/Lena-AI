from model.account.account_load import account_picture_load, account_username_load

def account_picture_load_controller(theme_color):
        user_image_path = account_picture_load(theme_color)
        return user_image_path

def account_username_load_controller():
        username = account_username_load()
        return username