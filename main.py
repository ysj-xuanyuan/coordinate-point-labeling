import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget,QGraphicsScene, QGraphicsView, QGraphicsPixmapItem
from PyQt5.QtWidgets import QListWidget, QVBoxLayout, QPushButton, QWidget, QFileDialog
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets

class ImageLabel(QLabel):
    def __init__(self, coord_list_widget):
        super().__init__()
        self.points = []
        self.coord_list_widget = coord_list_widget

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x, y = event.pos().x(), event.pos().y()
            self.points.append((x, y))
            self.update()
            self.updateCoordList()
            print(f"Clicked at coordinates: ({x}, {y})")

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(Qt.red)
        for point in self.points:
            painter.drawPoint(point[0], point[1])

    def updateCoordList(self):
        self.coord_list_widget.clear()
        for i, point in enumerate(self.points):
            self.coord_list_widget.addItem(f"Point {i+1}: ({point[0]}, {point[1]})")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.coord_list_widget = QListWidget()
        self.image_label = ImageLabel(self.coord_list_widget)
        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.clicked.connect(self.deleteSelectedPoint)

        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.image_label)
        layout.addWidget(self.coord_list_widget)
        layout.addWidget(self.delete_button)

        self.initUI()

    def initUI(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        open_action = file_menu.addAction('Open Image')
        open_action.triggered.connect(self.openImage)

    def openImage(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.jpg *.bmp)")
        if filename:
            image = QImage(filename)
            pixmap = QPixmap.fromImage(image)
            self.image_label.setPixmap(pixmap)

    def deleteSelectedPoint(self):
        selected_item = self.coord_list_widget.currentItem()
        if selected_item:
            index = self.coord_list_widget.row(selected_item)
            del self.image_label.points[index]
            self.image_label.updateCoordList()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())