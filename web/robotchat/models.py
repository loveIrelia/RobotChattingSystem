from django.db import models

# Create your models here.
class user_info(models.Model):
    # userid 是自增主键，django自动创建(key为id)
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=10)
    email = models.CharField(max_length=50)
    briefInfo = models.CharField(max_length=100, null=True)

class message(models.Model):
    # 帖子id为自增主键，django自动创建(key为id)
    user_id = models.ForeignKey(user_info, on_delete=models.PROTECT) #外键
    content = models.CharField(max_length=200) #内容
    tag = models.CharField(max_length=10) #标签
    like = models.IntegerField()  # 点赞
    dislike = models.IntegerField() #点踩
    date = models.CharField(max_length=100) # 时间
    anonymous = models.BooleanField()      #是否匿名

class comment(models.Model):
    # 外键1
    message_id = models.ForeignKey(message, on_delete=models.PROTECT)#定义反向访问
    # 外键2
    user_id = models.ForeignKey(user_info, on_delete=models.PROTECT)
    content = models.CharField(max_length=200) #内容
    anonymous = models.BooleanField() #是否匿名

class preference(models.Model):
    # 外键1
    message_id = models.ForeignKey(message, on_delete=models.PROTECT)
    # 外键2
    user_id = models.ForeignKey(user_info, on_delete=models.PROTECT)
    like_dislike = models.BooleanField() #true为点，false为踩