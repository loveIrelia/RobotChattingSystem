# Create your views here.
from django.http import HttpResponse
import random
import json
from django.views.decorators.csrf import csrf_exempt
from robotchat.models import user_info, message, comment, preference
from django.core.mail import send_mail
import time
@csrf_exempt
def email_check(request):
  resData = {'isOk': False, 'errmsg': '未知错误'}
  # print(request.POST)
  if request.method == 'POST':
    email = request.POST.get("email")
    if user_info.objects.filter(email=email):
      resData['errmsg'] = '该邮箱已注册'
    else:
      number = str(random.randrange(1000, 9999))
      send_mail('树洞聊天机器人', '您的验证码为'+number+'，若非本人请忽略。', 'shuaipoem@163.com',
                [email], fail_silently=False)
      resData['number'] = number
      resData['isOk'] = True
    jsonData = json.dumps(resData)
    return HttpResponse(jsonData, content_type="application/json")

@csrf_exempt
def SignUp(request):
    resData = {'isOk': False, 'errmsg': '未知错误'}
    if request.method =='POST':
        username = request.POST.get("name")
        password = request.POST.get("psw")
        email = request.POST.get("email")
        print(username)
        if user_info.objects.filter(username=username):
            resData['errmsg'] = '用户名已存在!'
        else:
            resData['isOk'] = True
            user_info.objects.create(username=username, password=password, email=email)
        jsonData = json.dumps(resData)
        return HttpResponse(jsonData, content_type="application/json")

@csrf_exempt
def SignIn(request):
    resData = {'isOk': False, 'errmsg': '未知错误'}
    if request.method =='POST':
        username = request.POST.get("name")
        password = request.POST.get("psw")
        print(username)
        print(password)
        # 对username去查在数据库中是否存在于username字段或者email字段
        res1 = user_info.objects.filter(email=username, password=password)
        res2 = user_info.objects.filter(username=username, password=password)
        # if res1 or res2:
        #     resData['isOk'] = True
        if res1:
            resData['isOk'] = True
            resData['user_id'] = res1[0].id
        elif res2:
            resData['isOk'] = True
            resData['user_id'] = res2[0].id
        else:
            resData['errmsg'] = '用户名或密码错误'
        jsonData = json.dumps(resData)
        return HttpResponse(jsonData, content_type="application/json")

#用户发帖
@csrf_exempt
def toPost(request):
    resData = {'isOk': False, 'errmsg': '未知错误'}
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        content = request.POST.get('content')
        label = request.POST.get('label')
        isAnonymity = request.POST.get('isAnonymity')
        resData['isOk'] = True
        ID = user_info.objects.get(id=int(user_id))
        Time = time.strftime('%Y.%m.%d %H:%M', time.localtime(time.time()))
        message.objects.create(user_id=ID, tag=label, like=0, dislike=0, content=content, anonymous=isAnonymity, date=Time)
        jsonData = json.dumps(resData)
        return HttpResponse(jsonData, content_type="application/json")

#查看所有帖
@csrf_exempt
def Posts(request):
    resData = {'isOk': False, 'errmsg': '未知错误'}
    #列表存放所有帖子信息
    L = []
    if request.method == 'GET':
        res = message.objects.all()
        for i in res:
            dic = {}
            if i.anonymous == True:
                dic['name'] = i.user_id.username
            else:
                dic['name'] = '匿名'
            dic['category'] = i.tag
            dic['date'] = i.date
            dic['like'] = i.like
            dic['dislike'] = i.dislike
            dic['content'] = i.content
            dic['user_id'] = i.user_id.id #通过外键找到表user_info里的id
            dic['pk'] = i.id
            L.append(dic)
        resData['isOk'] = True
        resData['Posts'] = L
        jsonData = json.dumps(resData)
        return HttpResponse(jsonData, content_type="application/json")

#查看某个帖
@csrf_exempt
def list_message(request):
    resData={'isOk': False, 'errmsg': '未知错误'}
    if request.method=='POST':
        pk = request.POST.get("pk")
        if message.objects.filter(id=int(pk)):
            mes = message.objects.get(id=int(pk))
            resData['name'] = mes.user_id.username#发贴人用户名
            resData['category'] = mes.tag#标签
            resData['date'] = mes.date#日期
            resData['content'] = mes.content#内容
            resData['like'] = mes.like#喜欢人数，默认为字符串类型
            resData['dislike'] = mes.dislike#不喜欢人数默认同上
            coment = mes.comment_set.all()#反向查询，coment是一个queryset对象，可以通过遍历得到对象
            com_list = {}
            count = 1
            for i in coment:
                if i.anonymous==False:
                    com_list[i.user_id.username] = i.content#得到comment表的许多条纪录
                else:
                    tmp_name = '匿名{name}'.format(name=count)
                    count += 1
                    com_list[tmp_name] = i.content
            resData['comments'] = com_list
            resData['isOK'] = True
        else:
            resData['errmsg'] = '找不到该帖子！'
        jsonData = json.dumps(resData)
        return HttpResponse(jsonData, content_type="application/json")

# 在帖中发表评论
@csrf_exempt
def speak(request):
    resData = {'isOk': False, 'errmsg': '未知错误'}
    if request.method == 'POST':
        pk = request.POST.get("pk")#帖子id
        comt=request.POST.get("comment")#评论内容
        isAnonymity=request.POST.get("isAnonymity")
        user_id=request.POST.get("user_id")#评论人的id
        resData['isOk'] = True
        # resData['mes_id']=message.objects.get(id=int(pk)).id
        # resData['usr_id']=user_info.objects.get(id=1).id
        # resData['id']=comment.objects.get(id=1)
        comment.objects.create(content=comt, anonymous=isAnonymity, message_id=message.objects.get(id=int(pk)), user_id=user_info.objects.get(id=int(user_id)))
        jsonData = json.dumps(resData)
        return HttpResponse(jsonData, content_type="application/json")

@csrf_exempt
def getinfo(request):
    resData = {'isOk': False, 'errmsg': '未知错误'}
    if request.method =='POST':
        user_id = request.POST.get('user_id')
        res = user_info.objects.filter(id=int(user_id))
        if res:
            resData['isOk'] = True
            resData['isOk'] = True
            resData['name'] = res[0].username
            resData['briefInfo'] = res[0].briefInfo
        else:
            resData['errmsg'] = '获取信息失败！'
        jsonData = json.dumps(resData)
        return HttpResponse(jsonData, content_type="application/json")

@csrf_exempt
def modifyInfo(request):
    resData = {'isOk': False, 'errmsg': '未知错误'}
    if request.method =='POST':
        user_id = request.POST.get('user_id')
        name = request.POST.get('name')
        briefInfo = request.POST.get('briefInfo')
        has_name = user_info.objects.filter(username=name)
        # 判断用户名是否已经存在
        if has_name:
            resData['errmsg'] = '用户名已经存在!'
        else:
            res = user_info.objects.filter(id=int(user_id))
            if res:
                resData['isOk'] = True
                user_info.objects.filter(id=int(user_id)).update(username=name, briefInfo=briefInfo)
            else:
                resData['errmsg'] = '修改失败!'
        jsonData = json.dumps(resData)
        return HttpResponse(jsonData, content_type="application/json")

@csrf_exempt
def like(request):
    resData = {'isOk': False, 'errmsg': '未知错误'}

    if request.method=='POST':
        pk = request.POST.get("pk") # 帖子id
        user_id = request.POST.get("user_id") # 评论人的id
        islike = request.POST.get("like_dislke")
        resData['isOk'] = True
        message_id_object = message.objects.get(id=int(pk))
        user_id_object = user_info.objects.get(id=int(user_id))
        if(int(islike)==1):#修改message点踩数
            message_id_object.like = message_id_object.like+1
            message.objects.filter(id=int(pk)).update(like=message_id_object.like)
        else:
            message_id_object.dislike = message_id_object.dislike+1
            message.objects.filter(id=int(pk)).update(dislike=message_id_object.dislike)
        ##像偏好表增加记录
        preference.objects.create(user_id=user_id_object, message_id=message_id_object, like_dislike=bool(islike))
        resData['like'] = message_id_object.like
        resData['dislike'] = message_id_object.dislike
        jsonData = json.dumps(resData)
        return HttpResponse(jsonData, content_type="application/json")