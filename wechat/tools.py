import os
import pathlib


# 获取目录下的所有文件
def get_path(path):
    file_list = []

    # 返回一个列表，其中包含在目录条目的名称(google翻译)
    files = os.listdir(path)
    for f in files:
        if os.path.isfile(path+'/'+str(f)):
            # 添加文件
            file_list.append(str(f))
    return file_list


# 获取目录下的所有文件
def get_path_id(path, user_id):
    file_list = []

    # 返回一个列表，其中包含在目录条目的名称(google翻译)
    files = os.listdir(path)
    for f in files:
        if os.path.isfile(path+'/'+str(f)):
            if str(f).find(user_id) != -1:
                # 添加文件
                file_list.append(str(f))
    return file_list


# 获取文件文本
def get_file_text(file_path):
    line = ''
    path = pathlib.Path(file_path)
    if path.exists():
        file_object = open(file_path, 'r')
        try:
            all_the_line = file_object.readlines()
            for line in all_the_line:
                line += line + "\r\n"
        finally:
            file_object.close()
    return line


# 是否位数字
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False
