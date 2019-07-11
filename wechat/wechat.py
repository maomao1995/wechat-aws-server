# coding:utf-8

from werobot import WeRoBot
from urllib.request import urlretrieve
import re
import datetime
from wechat import tools

robot = WeRoBot(token='awswechat')


# 明文模式不需要下面三项
robot.config["APP_ID"]='wx354be169ddce26e2'
robot.config["APP_SECRET"]='6e1138ffb0f1e79a433e15f42da5c90f'
#obot.config['ENCODING_AES_KEY'] = ''

text_path = '/home/ubuntu/wechat/text/'
image_path = '/home/ubuntu/wechat/image/'

client = robot.client
client.create_menu({
   "button":[
       {
           "type": "click",
           "name": "信息上传",
           "key": "V1001_TODAY_SEND"

       },
       {
           "type": "click",
           "name": "信息接收",
           "key": "V1001_TODAY_ACCEPT"
       },
       {
           "name": "链接",
           "sub_button": [
               {
                   "type": "view",
                   "name": "中国电科",
                   "url": "http://www.cetc.com.cn"
               },
               {
                   "type": "view",
                   "name": "船讯网",
                   "url": "http://www.shipxy.com"
               }
           ]
      }]
})


# 被关注
@robot.subscribe
def subscribe(message):
    print(message.context)
    return '感谢关注：）'


@robot.filter('密码')
def joke(message):
    print(message.context)
    return 'cetc28_jd'


@robot.filter('cetc28_jd')
def joke(message):
    print(message.context)
    file_list = tools.get_path(text_path)
    info = ''
    for path in file_list:
        file = open(path, 'r')
        info += file.readline() + "\r\n"
    return info


# 文本消息
@robot.text
def echo(message):
    send_pattern = "s:*?,*?,*?"
    con = message.context.replace('，', ',')
    if re.match(send_pattern, con):
        info = con.replace('s:', '').split(',', 3)
        jjm = info[0].strip()
        lon = info[1].replace(' ', '')
        lat = info[2].replace(' ', '')

        if jjm == '':
            return '录入失败！船舶名称不能为空'

        if tools.is_number(lon) is False:
            return '录入失败！经度(' + lon + ')为非数字'
        else:
            if float(lon) < -180.0 or float(lon) > 180.0:
                return '录入失败！经度(' + lon + ')超出范围'

        if tools.is_number(lat) is False:
            return '录入失败！纬度(' + lat + ')为非数字'
        else:
            if float(lat) < -90.0 or float(lat) > 90.0:
                return '录入失败！纬度(' + lat + ')超出范围'

        text_name = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S') + '.txt'
        file = open(text_name, 'w')
        if info.len == 3:
            file.write(jjm + '(' + lon + ',' + lat + ')')
        else:
            other = info[3].strip()
            file.write(jjm + '(' + lon + ',' + lat + '):'+ other)
            file.close()
        return jjm + '(' + lon + ',' + lat + ')录入成功！'
    else:
        return '录入失败！信息格式有误'


# image 修饰的 Handler 只处理图片消息
@robot.image
def image(message):
    # 下载文件并上传资源，重新返回
    image_name = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S') + '.jpg'
    urlretrieve(message.img, image_path+image_name)
    print('Recive Image:' + image_name)
    # media_file = open('/home/ubuntu/wechat-aws/wechat/media_file.jpg')
    # print('Download image as /home/ubuntu/wechat-aws/wechat/media_file for upload')
    # media_resp = client.upload_media('image', media_file)
    # print('Upload media id is '+media_resp['media_id'])
    return "图片保存成功！"


# voice 修饰的 Handler 只处理语音消息
@robot.voice
def voice(message):
    print('Recive Voice:' + message.media_id)
    return message.recognition


# video 修饰的 Handler 只处理视频消息
@robot.video
def video(message):
    print('Recive video:' + message.media_id)
    return message.recognition


# shortvideo 修饰的 Handler 只处理短视频消息
@robot.shortvideo
def shortvideo(message):
    print('Recive shortvideo:' + message.media_id)
    return message.recognition


# link 修饰的 Handler 只处理短视频消息
@robot.shortvideo
def link(message):
    print('Recive link:' + message.media_id)
    return message.recognition


# location 修饰的 Handler 只处理位置消息
@robot.location
def location(message):
    print('Recive Location:'+message.label)
    return 'Location:' + message.label


# 其他消息返回
@robot.handler
def hello(message):
    return '抱歉，不能识别该信息'


# location_event 修饰的 Handler 只处理上报位置 (Event)
@robot.location_event
def location_event(message):
    print('Recive Location Event:'+message.label)
    return 'Location Success!'


@robot.click
def click(message):
    print('Recive Menu Event:' + message.key)
    if message.key == "V1001_TODAY_SEND":
        return "请以以下格式输入位置信息：\r\n" + "s:船名,经度,纬度,说明\r\n" + "例如: s:粤渔###,123.2123,21.2312,不明渔船"
    if message.key == "V1001_TODAY_ACCEPT":
        return "请输入密码"


# robot.config['HOST'] = '0.0.0.0'
# robot.config['PORT'] = 80
# robot.run()

