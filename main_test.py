import os
import sys
import json
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QPushButton, QWidget, QFileDialog, QListWidget, QStatusBar
from PyQt5.QtGui import QPixmap, QImage, QPainter
from PyQt5.QtCore import Qt, QDir

class ImageLabel(QLabel):
    def __init__(self, status_bar):
        super().__init__()
        self.image_path = ""
        self.points = []
        self.data_dict = {}  # 初始化为空字典
        self.first_level_index = 0
        self.second_level_index = 0
        self.third_level_index = 0
        self.status_bar = status_bar

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x, y = event.pos().x(), event.pos().y()
            self.points.append([x, y, self.first_level_index])
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(Qt.red)
        for point in self.points:
            painter.drawPoint(point[0], point[1])

    def loadNextImage(self):
        if 0 <= self.second_level_index < len(files) and 0 <= self.third_level_index + 1 < len(file_tree[self.second_level_index]):
            self.third_level_index += 1
            self.points.clear()
            self.loadImage()
        else:
            self.status_bar.showMessage("已到达最后一张图像。")

    def loadPreviousImage(self):
        if 0 <= self.second_level_index < len(files) and 0 <= self.third_level_index - 1 < len(file_tree[self.second_level_index]):
            self.third_level_index -= 1
            if self.third_level_index < 0:
                self.third_level_index = 0
            self.points.clear()
            self.loadImage()
        else:
            self.status_bar.showMessage("已到达第一张图像。")

    def loadNextFolder(self):
        if 0 <= self.second_level_index + 1 < len(files):
            self.second_level_index += 1
            self.third_level_index = 0
            self.points.clear()
            self.loadImage()
        else:
            self.status_bar.showMessage("已到达最后一级目录。")

    def loadPreviousFolder(self):
        if 0 <= self.second_level_index - 1 < len(files):
            self.second_level_index -= 1
            if self.second_level_index < 0:
                self.second_level_index = 0
            self.third_level_index = 0
            self.points.clear()
            self.loadImage()
        else:
            self.status_bar.showMessage("已到达第一级目录。")

    def loadImage(self):
        # image_filename = f"{self.first_level_index:03d}_3D/{self.second_level_index:03d}_01/{self.third_level_index:03d}_01.jpg"
        image_filename = f"{files[self.second_level_index]}/{file_tree[self.second_level_index][self.third_level_index]}"
        image_path = QDir(self.image_path).filePath(image_filename)
        print(f'loadImage {image_path}')
        image = QImage(image_path)
        pixmap = QPixmap.fromImage(image)
        self.setPixmap(pixmap)
        
        # Update status bar
        status_text = f"当前文件夹：{files[self.second_level_index]}，文件名：{file_tree[self.second_level_index][self.third_level_index]}"
        self.status_bar.showMessage(status_text)

    def saveAnnotations(self):
        # 更新字典
        self.updateDataDict()

        # 保存到JSON文件
        json_file_path = os.path.join(self.image_path, 'data.json')
        with open(json_file_path, 'w') as json_file:
            json.dump(self.data_dict, json_file)

        print("Annotations saved.")

    def updateDataDict(self):
        # 将self.points中的坐标更新到self.data_dict中
        for point in self.points:
            key = str(point[2])  # 使用first_level_index作为字典的键
            if key not in self.data_dict:
                self.data_dict[key] = []
            self.data_dict[key].append(point[:2])

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.image_label = ImageLabel(self.status_bar)
        self.coord_list_widget = QListWidget()
        self.delete_button = QPushButton("删除选定点")
        self.delete_button.clicked.connect(self.deleteSelectedPoint)

        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.image_label)
        layout.addWidget(self.coord_list_widget)
        layout.addWidget(self.delete_button)

        self.initUI()

    def initUI(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('文件')

        open_action = file_menu.addAction('打开图像目录')
        open_action.triggered.connect(self.openImageDirectory)

        next_image_action = file_menu.addAction('加载下一张图像')
        next_image_action.triggered.connect(self.loadNextImage)
        next_image_action.setShortcut(Qt.Key_Right)  # Right arrow key

        previous_image_action = file_menu.addAction('加载上一张图像')
        previous_image_action.triggered.connect(self.loadPreviousImage)
        previous_image_action.setShortcut(Qt.Key_Left)  # Left arrow key

        next_folder_action = file_menu.addAction('加载下一级目录')
        next_folder_action.triggered.connect(self.loadNextFolder)
        next_folder_action.setShortcut(Qt.Key_Down)  # Down arrow key

        previous_folder_action = file_menu.addAction('加载上一级目录')
        previous_folder_action.triggered.connect(self.loadPreviousFolder)
        previous_folder_action.setShortcut(Qt.Key_Up)  # Up arrow key

        save_action = file_menu.addAction('保存标记')
        save_action.triggered.connect(self.saveAnnotations)
        save_action.setShortcut(Qt.CTRL + Qt.Key_S)  # Ctrl + S

    def openImageDirectory(self):
        directory = QFileDialog.getExistingDirectory(self, "打开图像目录")

        # 生成文件tree
        global files
        files = os.listdir(directory)
        global file_tree
        file_tree = []
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
        for file in files:
            file_path = os.path.join(directory, file)
            if os.path.isdir(file_path):
                imgs = [img for img in os.listdir(file_path) if os.path.splitext(img)[1].lower() in image_extensions]
                file_tree.append(imgs)
        
        print(f'openImageDirectory {file_tree}')

        if directory:
            self.image_label.loadInitialImage(directory)
            self.image_label.image_path = directory

    def loadNextImage(self):
        self.image_label.loadNextImage()

    def loadPreviousImage(self):
        self.image_label.loadPreviousImage()

    def loadNextFolder(self):
        self.image_label.loadNextFolder()

    def loadPreviousFolder(self):
        self.image_label.loadPreviousFolder()

    def deleteSelectedPoint(self):
        selected_item = self.coord_list_widget.currentItem()
        if selected_item:
            index = self.coord_list_widget.row(selected_item)
            del self.image_label.points[index]
            self.image_label.update()

    def saveAnnotations(self):
        self.image_label.saveAnnotations()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
