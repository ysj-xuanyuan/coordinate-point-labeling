import re
# 打开文件
with open('1.txt', 'r') as file:
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
    print(line)
    matches = re.findall(r'\(([^)]*)\)', line)
    print(matches)

    # 将匹配的数字分为两个列表
    list1 = [list(map(int, match.split(',')))[:3] for match in matches]
    list2 = [list(map(int, match.split(',')))[3:] for match in matches]
    coord_list.append(list1)
    coord_list.append(list2)

    # # 将信息添加到字典中，键为物体编号
    # threat_dict[key] = values

# 打印结果
print(coord_list)

# list to dict
coord_dict = {str(index): item for index, item in enumerate(coord_list)}

print(coord_dict)