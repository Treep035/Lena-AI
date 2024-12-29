from model.theme.get_theme import get_theme
from model.theme.update_theme import update_theme

def get_theme_controller():
    theme = get_theme()
    return theme

def update_theme_controller(theme_option):
    update_theme(theme_option)