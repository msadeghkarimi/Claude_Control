import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from gui.dashboard import Dashboard

def main():
    app = QApplication(sys.argv)
    
    # Set app icon
    app.setWindowIcon(QIcon("assets/icon.ico"))
    
    # Load stylesheet
    try:
        with open("styles/dark.qss", "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except:
        pass
    
    # Show dashboard
    window = Dashboard()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()