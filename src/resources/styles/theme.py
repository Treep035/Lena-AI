def change_theme(self, theme):

    if theme == "default":
        theme_color = ["#2C3E50", "#233240", "#3F556B", "#2b3b4a", "white"]
    
    elif theme == "light":
        theme_color = ["#B6B6B6", "#D9D9D9", "#9FA0A1", "#878787", "black"]
    
    elif theme == "dark":
        theme_color = ["#202226", "#2F2F2F", "#353639", "#131313", "white"]
    
    elif theme == "pink":
        theme_color = ["#FFC8F7", "#FFD3F9", "#FFBBF5", "#e8a7de", "black"]

    elif theme == "special":
        theme_color = ["#3E0149", "#520161", "#33003C", "#1f0025", "white"]
    
    else:
        theme_color = ["#2C3E50", "#233240", "#3F556B", "#2b3b4a", "white"]
    
    return theme_color