import os
import pathlib
import re


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


def send(message):
    send_pattern = "s:*?,*?,*?"
    con = message.replace('，', ',')
    if re.match(send_pattern, con):
        info = con.replace('s:', '').split(',', 3)
        jjm = info[0].strip()
        lon = info[1].replace(' ', '')
        lat = info[2].replace(' ', '')

        if jjm == '':
            return '录入失败！船舶名称不能为空'

        if is_number(lon) is False:
            return '录入失败！经度('+lon+')为非数字'
        else:
            if float(lon) < -180.0 or float(lon) > 180.0:
                return '录入失败！经度('+lon+')超出范围'

        if is_number(lat) is False:
            return '录入失败！纬度('+lat+')为非数字'
        else:
            if float(lat) < -90.0 or float(lat) > 90.0:
                return '录入失败！纬度('+lat+')超出范围'

        return jjm + '('+lon+','+lat+')录入成功！'

    else:
        return '录入失败！信息格式有误'