from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from backend.models import SecurityGuard, ExceptionsVideo,ToDoExceptions,Address
from django.http.response import JsonResponse
from MonitorOfCloud import settings
import os

def home(request):
    with open('fronted/dist/index.html', 'rb') as f:
        content = f.read()
    return HttpResponse(content)


def js(request, filename):
    with open('fronted/dist/static/js/{}'.format(filename), 'rb') as f:
        js_content = f.read()
    return HttpResponse(content=js_content,
                        content_type='application/javascript')  # 返回 js 响应


def css(request, filename):
    with open('fronted/dist/static/css/{}'.format(filename), 'rb') as f:
        css_content = f.read()
    return HttpResponse(content=css_content,
                        content_type='text/css')


def video(request, address,filename):
    with open('fronted/dist/static/video/{}/{}'.format(address,filename), 'rb') as f:
        video_content = f.read()
    return HttpResponse(content=video_content,
                        content_type='video/mpeg4')

def getIsNewException(request):
    '''
    前端不断ajax短轮询，判断是否来了新的异常
    :param request:
    :return:
    '''
    if settings.new_exception != {}:
        if "is_new" in settings.new_exception.keys():
            # 表示有新的异常
            jsonData = JsonResponse(
                {
                    "is_new":"true",
                    "new_info": "false",

                })
            settings.new_exception = {}
            return jsonData
        if "new_info" in settings.new_exception.keys():
            # 表示持续推送的异常信息
            jsonData = JsonResponse(
                {
                    "is_new": "false",
                    "new_info":"true",
                })
            settings.new_exception = {}
            return jsonData
    else:
        return JsonResponse(
                {
                    "is_new":"false",
                    "new_info": "false"
                })

def pushToDoExceptionsToPage(request):
    '''
    推送待-处理异常消息-到预警信息界面
    :param request:
    :return:
    '''
    to_do_exceptions = ToDoExceptions.objects.filter(is_deal=False)
    to_do_exceptions_list = []
    for item in to_do_exceptions:
        dic = {
            "tid":item.tid,
            "address": item.address,
            "time": item.time.strftime("%Y-%m-%d %H:%M:%S"),
            "number":item.number,
            "name": item.name,
            "phone": item.phone,
        }
        to_do_exceptions_list.append(dic)
    jsonData = JsonResponse(
        {
            "to_do": to_do_exceptions_list
        })
    return jsonData

def isDealToDoExceptions(request):
    '''
    前端 异常信息.page点击了删除按钮，表示异常视频地点处理完成

    :param request:
    :return:
    '''
    tid = request.GET.get("tid")
    to_do_exception = ToDoExceptions.objects.filter(tid=tid)
    to_do_exception.update(is_deal=True)
    return JsonResponse(
        {
            "success": "is_deal=True"
        })



def pushEdgeNewExceptionsInfo(request):
    '''
    边缘端调用,推送一个新的异常信息，并且建立一个新的异常视频对象
        边缘端传过来的：
        1、异常地点信息
    {
        "vid":-1,
        "address": "一个地址",
        "number": "异常地点的人数(数字)"
    }
    :param request:
    :return:
    '''
    # 获取边缘端传来的参数
    print("-------------------------------------")
    vid = request.GET.get("vid",default="-1")
    address = request.GET.get("address",default="NoneArea")
    number = request.GET.get("number",default="0")
    if vid == "-1":
        # 表示边缘端刚检测视频异常
        # 创建此次异常视频的数据库对象
        print("开始创建异常视频对象")
        exceptions_video = ExceptionsVideo()
        exceptions_video.address = address
        exceptions_video.number = number
        exceptions_video.save()

        print("异常发生次数+1")
        # 该地点 异常发生次数+1
        addr = Address.objects.filter(address=address).first()
        tmp = addr.exception_times
        print("原异常次数：",addr.exception_times)
        addr.exception_times = tmp + 1
        addr.save()
        print("+1后的异常次数：", addr.exception_times)

        # 获取该地警卫的信息
        guard = SecurityGuard.objects.filter(address=address).first()
        name = guard.name
        phone = guard.phone
        # 存储信息到ToDoExceptions表,默认表示这个是未处理的异常
        print("存储信息到ToDoExceptions表,默认表示这个是未处理的异常")
        to_do_exceptions = ToDoExceptions()
        to_do_exceptions.address = address
        to_do_exceptions.number = number
        to_do_exceptions.name = name
        to_do_exceptions.phone = phone
        # 与视频对象相关联
        print("to_do_exceptions与视频对象相关联")
        to_do_exceptions.vid = exceptions_video.vid
        to_do_exceptions.save()

        # 用来标记有一个新的异常视频
        settings.new_exception['is_new'] = "true"

        # 返回vid给边缘端,使边缘端异常视频对应web端的一个异常视频对象
        jsonData = JsonResponse(
            {
                "vid": exceptions_video.vid
            })
        return jsonData
    else:
        jsonData = JsonResponse(
            {
                "vid": -1
            })
        return jsonData

def pushEdgeLastExceptionInfo(request):
    '''
    边缘端调用调用, 持续推送该异常视频的 地点和人数到前端
    :param request:
    :return:
    '''
    vid = request.GET.get("vid")
    # address = request.GET.get("address")
    number = request.GET.get("number")
    print(vid)
    if vid != "-1":
        # web端发现异常视频后，已经返回了vid，使边缘端异常视频对应web端的一个异常视频对象
        to_do_e = ToDoExceptions.objects.filter(vid=vid).first()
        to_do_e.number = number
        to_do_e.save()
        # ev = ExceptionsVideo.objects.filter(vid=vid).first()
        # ev.number = number
        # ev.save()
        settings.new_exception["new_info"] = "true"
        jsonData = JsonResponse(
            {
                "vid": vid
            })
        return jsonData



def storeEdgeNewExceptionVideo(request):
    '''
     边缘端调用,传输该新的、被处理过的异常视频到 web服务器,
     并且根据 vid
     并且构造一个video_path存储好
    :param request:
    :return:
    '''
    vid = request.POST.get("vid",default=-1)
    if vid != -1:

        # --------这里有个功能
        # 获取边缘端传来的视频数据
        # 存放视频
        #
        # 保存视频路径(实际视频物理文件在服务器存放的路径)
        ex_video = request.FILES.get('file')
        ev = ExceptionsVideo.objects.filter(vid=vid).first()
        # half_path = /static/video/地点名/人数_时间.avi
        half_path =  '/static/video/{}/{}_{}.mp4'.format(ev.address,
                                                         ev.number,
                                                         ev.time.strftime("%Y-%m-%d_%H-%M-%S"))
        # 前端http请求文件的路径
        url_path = settings.my_http + half_path
        ev.video_path = url_path
        ev.save()

        if not (os.path.isdir("fronted/dist/static/video/{}".format(ev.address))):
            # 如果该目录不存在，则创建目录
            os.makedirs("fronted/dist/static/video/{}".format(ev.address))

        # 服务器上的物理文件的路径
        real_path = "fronted/dist" + half_path
        # 保存文件
        with open(real_path, 'wb') as f:
            # 3.获取上传文件的内容并写到创建的文件中
            for content in ex_video.chunks():  # pic.chunks() 文件的内容
                f.write(content)

        # 以下代码仅用于测试，实际此函数并不返回任何
        # 当在生产环境时注释掉
        jsonData = JsonResponse(
            {
                "vid": vid
            })
        return jsonData


def getAddressList(request):
    '''
    获取地址列表
    :param request:
    :return:
    '''
    addr = Address.objects.all()
    address_list = []
    for item in addr:
        dic = {
            "address": item.address,
            "threshold":item.threshold
        }
        address_list.append(dic)
    jsonData = JsonResponse(
        {
            "address_list": address_list
        })
    return jsonData

def updateThreshold(request):
    address = request.GET.get("address", default='Test_A')
    threshold = request.GET.get("threshold", default='5')
    addr = Address.objects.filter(address=address).first()
    addr.threshold = threshold
    addr.save()
    jsonData = JsonResponse(
        {
            "success": "success"
        })
    return jsonData

def getAddressValue(request):
    '''
    获取地址列表
    :param request:
    :return: [{"value":"这是一个地址"},
               {"value":"这是第二个个地址"}
                ]
    '''
    securityGuard = SecurityGuard.objects.all()
    address_value = []
    for item in securityGuard:
        dic = {
            "value": item.address,
        }
        address_value.append(dic)
    jsonData = JsonResponse(
        {
            "address_value": address_value
        })
    return jsonData


def getGuardInfo(request):
    '''
    获取异常地区安保人员信息
    :param request:
    :return:
    '''
    address = request.GET.get("address", default='Test_A')
    securityGuard = SecurityGuard.objects.filter(address=address).first()
    data = {
        "address": securityGuard.address,
        "name": securityGuard.name,
        "phone": securityGuard.phone
    }
    return JsonResponse(data)

def getAddressInfo(request):
    '''
    获取异常信息，   地区，异常次数
    用来给前端根据异常次数  从大到小排序
    :param request:
    :return:
    '''
    address = Address.objects.all()
    exceptions_info = []
    for item in address:
        dic = {
            "address": item.address,
            "exception_times": item.exception_times
        }
        exceptions_info.append(dic)
    jsonData = JsonResponse(
        {
            "exceptions_info": exceptions_info
        })
    return jsonData


def getExceptionsVideoInfo(request):
    '''
    获取指定 "address" 的异常视频信息
    :param request:
    :return:
    '''
    address = request.GET.get("address", default='Test_A')
    exceptions_videos = ExceptionsVideo.objects.filter(address=address).all()
    video_info = []
    for item in exceptions_videos:
        if item.video_path != "null":       # 保证只获取那些已经保存异常视频的--异常视频对象
            dic = {
                "vid": item.vid,
                "address": item.address,
                "number": item.number,
                "time": item.time.strftime("%Y-%m-%d %H:%M:%S"),
                "video_path":item.video_path
            }
            video_info.append(dic)
    jsonData = JsonResponse(
        {
            "video_info": video_info
        })
    return jsonData
