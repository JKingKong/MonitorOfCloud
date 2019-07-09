from django.db import models
from django.contrib.auth.models import User

# class SecurityTeam(models.Model):
#     sid = models.AutoField(primary_key=True)
#     area = models.CharField(max_length=60)
#     team_name = models.CharField(max_length=60)


# class SecurityGuard(models.Model):
#     gid = models.AutoField(primary_key=True)
#     security_team = models.ForeignKey(SecurityTeam,
#                               related_name='guards',
#                               on_delete=models.CASCADE)           #
#     phone = models.CharField(max_length=20)


# 被监控的地点
class Address(models.Model):
    aid = models.AutoField(primary_key=True)                # 地址id
    address = models.CharField(max_length=200,unique=True)  # 地点名字
    exception_times = models.IntegerField(default=0)        # 异常发生的次数
    threshold = models.IntegerField(default=5)              # 地点的阈值


# 地点保安人员信息
class SecurityGuard(models.Model):
    gid = models.AutoField(primary_key=True)
    address = models.CharField(max_length=200,unique=True)  # 地点名字
    name = models.CharField(max_length=60)              # 安保人员名字
    phone = models.CharField(max_length=20)



# 异常视频信息
class ExceptionsVideo(models.Model):
    vid = models.AutoField(primary_key=True)
    address = models.CharField(max_length=200)
    number = models.IntegerField()                          # 视频中有几个人
    video_path = models.TextField(default="null")               # 异常视频路径
    time = models.DateTimeField("到来时间",auto_now_add=True)


# 保存前端未处理(is_deal = False)的异常信息
# 处理后：(is_deal = True)
# 其实可以用Redis 存储这些
class ToDoExceptions(models.Model):
    tid = models.AutoField(primary_key=True)
    address = models.CharField(max_length=200)    # 地点名字
    number = models.IntegerField()                            # 视频中有几个人
    name = models.CharField(max_length=60)                    # 安保人员名字
    phone = models.CharField(max_length=20)
    vid = models.IntegerField()
    time = models.DateTimeField("到来时间",auto_now_add=True)
    is_deal = models.BooleanField(default=False)               #
