'''
"C:/Users/YSJ/Pictures/test/1/01007962-1.BMP"
'''
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QScrollArea, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap

class ScrollImageLabelDemo(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # 创建QLabel并加载图片
        image_path = "C:/Users/YSJ/Pictures/test/1/01007962-1.BMP"  # 替换为你的图片路径
        pixmap = QPixmap(image_path)
        self.label = QLabel()
        self.label.setPixmap(pixmap)

        # 将QLabel放在QScrollArea中
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.label)

        layout.addWidget(scroll_area)

        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('Scrollable Image QLabel Demo')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = ScrollImageLabelDemo()
    sys.exit(app.exec_())