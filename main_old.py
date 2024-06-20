import os
import sys
import json
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout,QHBoxLayout, QPushButton, QWidget, QFileDialog, QListWidget, QStatusBar
from PyQt5.QtGui import QPixmap, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QDir


class ImageLabel(QLabel):
    def __init__(self, status_bar,coord_list_widget):
        super().__init__()
        self.image_path = ""
        self.points = []
        self.data_dict = {}  # 初始化为空字典
        self.first_level_index = 0
        self.second_level_index = 0
        self.third_level_index = 0
        self.status_bar = status_bar
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
        pen = QPen(Qt.red)
        pen.setWidth(5)  # 设置画笔宽度，调整红点的大小
        painter.setPen(pen)
        
        for point in self.points:
            painter.drawPoint(point[0], point[1])


    def updateCoordList(self):
        self.coord_list_widget.clear()
        for i, point in enumerate(self.points):
            self.coord_list_widget.addItem(f"Point {i+1}: ({point[0]}, {point[1]})")

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
            # self.data_dict.clear()
            self.loadImage()
        else:
            self.status_bar.showMessage("已到达第一张图像。")

    def loadNextFolder(self):
        if 0 <= self.second_level_index + 1 < len(files):
            self.second_level_index += 1
            self.third_level_index = 0
            self.points.clear()
            self.data_dict.clear()
            self.loadInitialImage()
        else:
            self.status_bar.showMessage("已到达最后一级目录。")

    def loadPreviousFolder(self):
        if 0 <= self.second_level_index - 1 < len(files):
            self.second_level_index -= 1
            if self.second_level_index < 0:
                self.second_level_index = 0
            self.third_level_index = 0
            self.points.clear()
            self.data_dict.clear()
            self.loadInitialImage()
        else:
            self.status_bar.showMessage("已到达第一级目录。")


    def loadImage(self):
        # image_filename = f"{self.first_level_index:03d}_3D/{self.second_level_index:03d}_01/{self.third_level_index:03d}_01.jpg"
        image_filename = f"{files[self.second_level_index]}/{file_tree[self.second_level_index][self.third_level_index]}"
        image_path = QDir(self.image_path).filePath(image_filename)
        self.save_json_path = QDir(self.image_path).filePath(files[self.second_level_index])
        print(f'loadImage {image_path}')
        image = QImage(image_path)
        pixmap = QPixmap.fromImage(image)
        self.setPixmap(pixmap)
        
        # Update status bar
        # status_text = f"当前文件夹：{self.second_level_index:03d}_01，文件名：{self.third_level_index:03d}_01.jpg"
        status_text = f"当前文件夹：{files[self.second_level_index]}，文件名：{file_tree[self.second_level_index][self.third_level_index]}"
        self.status_bar.showMessage(status_text)

    def saveAnnotations(self):
        # print(self.points)# 这块按标注顺序存了点的坐标，整理后就能报错为json
        # print(self.data_dict)
        # if self.old_points ==self.points:
        #     self.status_bar.showMessage("坐标点已记录。")
        # else:

        # 更新字典用于保存
        for i, key in enumerate(self.data_dict):
            if i<len(self.points):
                self.data_dict[key].append(self.points[i])
            else:
                self.status_bar.showMessage(f"标注点少于需要的点。需要{len(self.data_dict)}，已标注{(len(self.points))}")
        print(self.data_dict)

        print(self.third_level_index+1,'||',len(file_tree[self.second_level_index]))

        # 保存到JSON文件
        # if  self.third_level_index+1 == len(file_tree[self.second_level_index]):
        json_file_path = os.path.join(self.save_json_path, 'data.json')
        print(json_file_path)
        with open(json_file_path, 'w') as json_file:
            json.dump(self.data_dict, json_file)
        self.status_bar.showMessage("坐标点已导出。")

        self.old_points =self.points
        self.status_bar.showMessage("坐标点已记录。")

    def loadInitialImage(self, image_path=""):
        self.old_points = {}
        if self.second_level_index ==0:
            self.image_path = image_path

        # 读取JSON文件
        # json_file_path = os.path.join(self.image_path, files[self.second_level_index],'1.json')
        txt_file_path = os.path.join(self.image_path, files[self.second_level_index],'1.txt')
        print(f'3D坐标文件路径：{txt_file_path}')
        self.status_bar.showMessage(f'3D坐标文件路径：{txt_file_path}')
        # print(json_file_path)
        # if os.path.exists(json_file_path):
        #     with open(json_file_path, 'r') as json_file:
        #         data_dict = json.load(json_file)
        #         # 在这里可以处理data_dict，将点坐标等信息加载到self.points中
        #         # 例如：self.points = data_dict.get('points', [])

        # 读取txt文件
        self.data_dict = read_txt_to_dict(txt_file_path)

        # 更换存储格式
        # self.data_dict = {}
        # for i, key in enumerate(data_dict):
        #     self.data_dict[key] = [data_dict[key]]
        # print(self.data_dict)

        self.loadImage()

def read_txt_to_dict(txt_path):
    with open(txt_path, 'r') as file:
        content = file.read()

    # 初始化字典
    coord_dict = {}
    coord_list = []

    # 逐行读取文件内容
    for line in content.split('\n'):
        # 跳过空行
        if not line:
            continue
        # 使用正则表达式提取括号内的数字
        # print(line)
        matches = re.findall(r'\(([^)]*)\)', line)
        # print(matches)
        # 将匹配的数字分为两个列表
        list1 = [list(map(int, match.split(',')))[:3] for match in matches]
        list2 = [list(map(int, match.split(',')))[3:] for match in matches]
        coord_list.append(list1)
        coord_list.append(list2)

    # print(coord_list)
    # list to dict
    coord_dict = {str(index): item for index, item in enumerate(coord_list)}
    print(coord_dict)

    return coord_dict


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.coord_list_widget = QListWidget()
        self.image_label = ImageLabel(self.status_bar,self.coord_list_widget)
        self.delete_button = QPushButton("删除选定点")
        self.delete_button.clicked.connect(self.deleteSelectedPoint)

        layout = QHBoxLayout(self.central_widget)
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
        # print(f'openImageDirectory {directory}')
        global files
        files = os.listdir(directory)
        # print(f'openImageDirectory{files}')
        global file_tree
        file_tree = []
        image_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
        for file in files:
            file_path =os.path.join(directory,file)
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
            self.image_label.updateCoordList()

    def saveAnnotations(self):
        self.image_label.saveAnnotations()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
