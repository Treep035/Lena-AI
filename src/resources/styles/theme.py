def change_theme(self, theme):

    if theme == "default":
        theme_color = ["#2C3E50", "#233240", "#3F556B", "white"]
    
    elif theme == "light":
        theme_color = ["#B6B6B6", "#D9D9D9", "#9FA0A1", "black"]
    
    elif theme == "dark":
        theme_color = ["#202226", "#2F2F2F", "#353639", "white"]
    
    else:
        theme_color = ["#2C3E50", "#233240", "#3F556B", "white"]
    
    return theme_color