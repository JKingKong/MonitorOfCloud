from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from backend.views import *
from backend import views
from django.views.generic import TemplateView



urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^admin/', admin.site.urls),
    # 静态文件路由可以使用 nginx
    url(r'^js/(?P<filename>.*\.js)$', js, name='js'),        # 匹配js、css等静态文件的路由
    url(r'^css/(?P<filename>.*\.css)$', css, name='css'),    # (如果有几十种不同的静态文件 那岂不是要写几十个视图匹配？)
    url(r'^video/(?P<address>.*)/(?P<filename>.*\.mp4)$', video, name='css'),  # (如果有几十种不同的静态文件 那岂不是要写几十个视图匹配？)

    url(r'^address_list/',getAddressList),
    url(r'^address_value/',getAddressValue),                # 用来在获取异常视频.page提供输入地址提醒
    url(r'^guard_info/',getGuardInfo),                      # 获取警卫信息
    url(r'^exceptions_info/',getAddressInfo),               # 获取监控地点的信息，地名、异常次数
    url(r'^video_info/',getExceptionsVideoInfo),            # 获取异常视频信息,(已经保存好了的)
    url(r"^is_new/",getIsNewException),                     # 轮询是否有新的异常从边缘端发来
    url(r"^to_do/", pushToDoExceptionsToPage),              # 待处理的异常列表(在前端异常信息.page展示)
    url(r'^is_deal_exception/', isDealToDoExceptions),      # 异常处理完毕
    url(r'^update_threshold/', updateThreshold),            # 根据地址更新阈值

    # 下边三个是一个连续过程
    url(r'^push_new/', pushEdgeNewExceptionsInfo),      # 边缘端调用,推送一个新的异常信息，并且建立一个新的异常视频对象
    url(r'^deal_new/', pushEdgeLastExceptionInfo),       # 边缘端调用调用, 持续推送该异常视频的 地点和人数 到前端
    url(r'^store_video/', storeEdgeNewExceptionVideo),  # 边缘端调用,传输该新的、被处理过的异常视频到web服务器,并且存储好
]
