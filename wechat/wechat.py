# coding:utf-8

from werobot import WeRoBot

robot = WeRoBot(token='awswechat')


# 明文模式不需要下面三项
robot.config["APP_ID"]='wx354be169ddce26e2'
robot.config["APP_SECRET"]='6e1138ffb0f1e79a433e15f42da5c90f'
#obot.config['ENCODING_AES_KEY'] = ''

client = robot.client
client.create_menu({
   "button":[
       {
           "type": "click",
           "name": "新闻",
           "key": "V1001_TODAY_NEWS"
       },
       {
           "type": "click",
           "name": "天气",
           "key": "V1001_TODAY_WEATHER"
       },
       {
           "name": "Help",
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
    return '''Hello World!
And nice to meet you.
:）
'''

@robot.filter('新闻')
def joke(message):
    data = '华为：获中国首个5G无线数据终端电信设备进网许可证'
    return data

# 文本消息返回原文
@robot.text
def echo(message):
    return message.content


# 其他消息返回
@robot.handler
def hello(message):
    return '(O_o)??'

@robot.click
def click(message):
    print('Recive Menu Event:' + message.key)
    if message.key == "V1001_TODAY_NEWS":
        return "华为：获中国首个5G无线数据终端电信设备进网许可证"
    if message.key == "V1001_TODAY_WEATHER":
        return "天气不好"


robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.run()

