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
           "name": "未处理信息",
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
    print(message.content)
    return '感谢关注：）'


# @robot.filter('密码')
# def joke(message):
#     print(message.content)
#     return 'cetc28_jd'
#
#
# @robot.filter('cetc28_jd')
# def joke(message):
#     print(message.content)
#     file_list = tools.get_path(text_path)
#     info = ''
#     for path in file_list:
#         file = open(path, 'r')
#         info += file.readline() + "\r\n"
#     return info


# 文本消息
@robot.text
def echo(message):
    con = message.content.replace('，', ',')

    if len(con) <= 5:
        return '录入失败！消息过短'
    # text_name = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S') + '.txt'
    text_name = message.source + '_' + str(message.create_time) + '.txt'
    file = open(text_path + text_name, 'w')
    file.write(con)
    file.close()


# image 修饰的 Handler 只处理图片消息
@robot.image
def image(message):
    # 下载文件并上传资源，重新返回
    image_name = message.source + '_' + str(message.create_time) + '.jpg'
    #image_name = message.source + '_' + datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S') + '.jpg'
    urlretrieve(message.img, image_path+image_name)
    print('Recive Image:' + image_name)
    # media_file = open('/home/ubuntu/wechat-aws/wechat/media_file.jpg')
    # print('Download image as /home/ubuntu/wechat-aws/wechat/media_file for upload')
    # media_resp = client.upload_media('image', media_file)
    # print('Upload media id is '+media_resp['media_id'])
    return "图片接收成功！"


# voice 修饰的 Handler 只处理语音消息
@robot.voice
def voice(message):
    print('Recive Voice:' + message.media_id)
    return message.recognition


# video 修饰的 Handler 只处理视频消息
@robot.video
def video(message):
    print('Recive video:' + message.type)
    return "抱歉，暂不支持接收视频消息"


# shortvideo 修饰的 Handler 只处理短视频消息
@robot.shortvideo
def shortvideo(message):
    print('Recive shortvideo:' + message.type)
    return "抱歉，暂不支持接收短视频消息"


# link 修饰的 Handler 只处理链接消息
@robot.link
def link(message):
    print('Recive link:' + message.type)
    return "抱歉，暂不支持接收链接消息"


# location 修饰的 Handler 只处理位置消息
@robot.location
def location(message):
    msg_time = datetime.datetime.fromtimestamp(message.create_time).strftime('%Y-%m-%d %H:%M:%S')
    print('Recive Location:' + message.label + '(' + str(message.location_x) + ',' + str(message.location_y) + ',' + msg_time + ')')
    #datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    return '定位:' + message.label + '(' + str(message.location_x) + ',' + str(message.location_y) + ',' + msg_time + ')'


# 其他消息返回
@robot.handler
def hello(message):
    return '抱歉，不能识别该消息'


# location_event 修饰的 Handler 只处理上报位置 (Event)
@robot.location_event
def location_event(message):
    print('Recive Location Event:'+message.label)
    return 'Location Success!'


@robot.click
def click(message):
    print('Recive Menu Event:' + message.key)
    if message.key == "V1001_TODAY_SEND":
        return "消息需带有位置信息，可通过发送位置获取定位信息，消息长度不得小于6字符"
    if message.key == "V1001_TODAY_ACCEPT":
        result = ''
        user_id = message.source
        file_paths = tools.get_path_id(text_path, user_id)
        for file_path in file_paths:
            file_text = tools.get_file_text(text_path + "/" + file_path)
            if file_text != '':
                result += datetime.datetime.fromtimestamp(int(file_path.split('_')[1])).strftime('%Y-%m-%d %H:%M:%S') + ":\r\n" + file_text
        if result != '':
            return result
        else:
            return '您没有未处理信息'


robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.run()

