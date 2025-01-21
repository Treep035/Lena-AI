from PyQt5.QtCore import QObject, pyqtSignal

class StopAnimationSignal(QObject):
    _instance = None

    @staticmethod
    def get_instance():
        if StopAnimationSignal._instance is None:
            StopAnimationSignal._instance = StopAnimationSignal()
        return StopAnimationSignal._instance
    
    stop_animation_signal = pyqtSignal()
