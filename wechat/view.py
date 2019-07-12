from django.http.response import HttpResponse
import hashlib
from django.views.decorators.csrf import csrf_exempt


def make_view(robot):

    @csrf_exempt
    def werobot_view(request):
        if request.method == 'GET':
            signature = request.GET.get('signature')
            timestamp = request.GET.get('timestamp')
            nonce = request.GET.get('nonce')
            echostr = request.GET.get('echostr')
            token = 'leartd'

            hashlist = [token, timestamp, nonce]
            hashlist.sort()
            print('[token, timestamp, nonce]', hashlist)

            # 这里必须增加encode('utf-8'),否则会报错
            hashstr = ''.join([s for s in hashlist]).encode('utf-8')

            print('hashstr befor sha1', hashstr)
            hashstr = hashlib.sha1(hashstr).hexdigest()
            print('hashstr sha1', hashstr)
            if hashstr == signature:
                # 必须返回echostr
                return HttpResponse(echostr)

            else:
                # 可根据实际需要返回
                return HttpResponse('error')
        else:
            # 可根据实际需要返回
            return HttpResponse('chenggong')
    return werobot_view