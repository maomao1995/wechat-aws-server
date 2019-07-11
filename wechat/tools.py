import os


# 获取目录下的所有文件
def get_path(path):
    file_list = []

    # 返回一个列表，其中包含在目录条目的名称(google翻译)
    files = os.listdir(path)
    for f in files:
        if os.path.isfile(path+'/'+f):
            # 添加文件
            file_list.append(f)
    return file_list


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
