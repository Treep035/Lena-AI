import sys
from PyQt5.QtWidgets import QApplication
from model.protocol.handle_lenaai_url import handle_lenaai_url

def handle_lenaai_url_controller(url):
    handle_lenaai_url(url)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
        app = QApplication(sys.argv)  # Solo creamos la app para el diálogo
        handle_lenaai_url_controller(url)
        sys.exit(app.exec_())
    else:
        print("No URL argument provided.")