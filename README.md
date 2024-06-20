# 使用

运行`标点工具.exe`

## 运行

选择文件路径为--image_path

# 文件结构

--image_path

​	--001_3D

​		--001_01.jpg

​		--001_02.jpg

​		--001_03.jpg

​		--001_04.jpg

​		--001_05.jpg

​		--001_06.jpg

​		--1.txt

​	--002_3D

​	--003_3D



上下控制二级目录。左右控制三级目录（默认读取第一个01.jpg）

二维图像坐标：左上角为坐标原点（0,0）

## 1.txt 格式

```txt
VDBox.AddThreatMarks(500, 347, 33, 545, 400, 80);//knife 
VDBox.AddThreatMarks(500, 391, 81, 600, 239, 120);//felighter 
VDBox.AddThreatMarks(500, 200, 151, 584, 284, 200);//portablebattery
VDBox.AddThreatMarks(500, 150, 210, 554, 210, 260);
VDBox.AddThreatMarks(500, 180, 270, 554, 290, 310);

VDBox.AddThreatMarks(400, 347, 33, 445, 400, 80);//knife 
VDBox.AddThreatMarks(400, 391, 81, 500, 239, 120);//felighter 
VDBox.AddThreatMarks(400, 200, 151, 484, 284, 200);//portablebattery
VDBox.AddThreatMarks(400, 150, 210, 454, 210, 260);
VDBox.AddThreatMarks(400, 180, 270, 454, 290, 310);
```



# ！！！注意事项！！！

1、标点顺序必须和1.json中存储的坐标点顺序相同

2、删除标记点的功能最好只删除最新标注的点

3、单张图像标注完成后再点击保存。并且每次保存功能不要多次点击，一次就够，下方状态栏会提示保存成功

4、在标注完整个文件夹下图像之前不要关闭软件，软件暂不支持关闭后继续标注