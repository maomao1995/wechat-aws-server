from django.http import HttpResponse
import re


def test(request):
    return HttpResponse("success ! ")


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


if __name__ == '__main__':
    conn = send('s: sa,12 0,23.21,')
    print(conn)
