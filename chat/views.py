# coding:utf-8
from django.shortcuts import render,HttpResponse

# Create your views here.
import requests
import re
import time
import json
import threading

Qcode = None
Ctime = None
TIP = 1
ticket_dict ={}
USER_INIT_DICT={}
ALL_COOKIE_DICT = {}

def login(request):
    '''
    获取二维码 ， 在老子的网站显示
    :param request:
    :return:
    '''
    global Ctime
    Ctime = time.time()
    response = requests.get('https://login.wx.qq.com/jslogin?appid=wx782c26e4c19acffb&fun=new&lang=zh_CN&_=%s' % Ctime)
    v =re.findall('uuid = "(.*?)";',response.text)
    # print(v)
    global Qcode
    Qcode = v[0]

    return render(request, 'weixin/login.html', {'qcode':Qcode})
def check_login(request):
    '''
    监听用户是否扫码  扫码就出头像

    监听用户是否已经点击确认登入
    :param request:
    :return:
    '''
    global TIP
    ret = {'code':408,'data':None}
    r1 = requests.get(
        url='https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid=%s&tip=%s&r=95982085&_=%s'%(Qcode,TIP,Ctime)
    )
    #print(r1.text)
    if 'window.code=408' in r1.text:
        print("无人扫码")
        return HttpResponse(json.dumps(ret))
    elif 'window.code=201' in r1.text:
        ret['code'] = 201
        avater = re.findall("window.userAvatar = '(.*)';", r1.text)[0]
        ret['data'] = avater
        TIP = 0
        return HttpResponse(json.dumps(ret))
    elif 'window.code=200' in r1.text:
        # 用户点击确认登录
        """  
        window.code=200;
        window.redirect_uri="https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxnewloginpage?ticket=AYKeKS9YQnNcteZCfLeTlzv7@qrticket_0&uuid=QZA2_kDzdw==&lang=zh_CN&scan=1494553432";
        window.redirect_uri="https://wx2.qq.com/cgi-bin/mmwebwx-bin/webwxnewloginpage?ticket=AYKeKS9YQnNcteZCfLeTlzv7@qrticket_0&uuid=QZA2_kDzdw==&lang=zh_CN&scan=1494553432";
       
        """
        #print(r1.text)
        redirect_uri = re.findall('window.redirect_uri="(.*)";',r1.text)[0]
        redirect_uri = redirect_uri + "&fun=new&version=v2"
        ALL_COOKIE_DICT.update(r1.cookies.get_dict())

        # 获取凭证

        r2 = requests.get(url=redirect_uri)
        from bs4 import BeautifulSoup
        suop = BeautifulSoup(r2.text,'html.parser')
        for tag in suop.find('error').children:
            ticket_dict[tag.name] = tag.get_text()
        #print(ticket_dict)

        ALL_COOKIE_DICT.update(r2.cookies.get_dict())




        ret['code'] = 200

        return HttpResponse(json.dumps(ret))

def chat(request):
    '''
    个人主页显示
    :param request:
    :return:
    '''

    # 获取用户信息
    # https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxinit?r=1249373791&lang=zh_CN&pass_ticket=Ugf%252BqGi%252F4c7HYBEXYNgYuZjGmlE47m6hoz6GWyIO%252BR2peDJIZgCWXqGBCpR8dFKz

    get_user_info_data = {
        'BaseRequest': {
            'DeviceID': "e402310790089148",
            'Sid':ticket_dict['wxsid'],
            'Uin':ticket_dict['wxuin'],
            'Skey':ticket_dict['skey'],
        }
    }

    get_user_info_url =  "https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxinit?r=88828930&lang=zh_CN&pass_ticket=" + ticket_dict['pass_ticket']
    r3 = requests.post(
        url=get_user_info_url,
        json=get_user_info_data,
        cookies=ALL_COOKIE_DICT,
    )
    r3.encoding = 'utf-8'
    ALL_COOKIE_DICT.update(r3.cookies.get_dict())
    user_init_dict = json.loads(r3.text)
    #print(user_init_dict)
    USER_INIT_DICT.update(user_init_dict)


    # for k,v in user_init_dict.items():
    #     print(k,v)
    # 最近联系人
    contact_list = user_init_dict
    # for item in contact_list['ContactList']:
    #     print(item['HeadImgUrl'])
    # for item in contact_list['MPSubscribeMsgList']:
    #     print(item['NickName'])
    #     for msg in item['MPArticleList']:
    #         print(msg)
    # ppp = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxgetcontact?lang=zh_CN&r=%s&seq=0&skey=%s' % (str(time.time()),ticket_dict['skey'])
    # rep = requests.get(url=ppp,cookies=ALL_COOKIE_DICT)
    # rep.encoding = 'uft-8'
    # repp = json.loads(rep.text)
    # print(repp)

    return render(request, 'weixin/chat.html', {'contact_list':contact_list})


def contact_list(request):
    '''
    # 获取更多的联系人   ，  并在页面中显示
    :param request:
    :return:
    '''
    # https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxgetcontact?pass_ticket=J6GLa%252FBobIDCebI4llpykyMrbHPm86KGMDqE4jUS20OCwWhkK%252BF6uiJpLM%252BO5PoU&r=1494811126614&seq=0&skey=@crypt_d83b5b90_eb1965b01a3bc3f4d7a4bdc846b77a19

    cimte = str(time.time())
    url = "https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxgetcontact?pass_ticket=%s&r=%s&seq=0&skey=%s" % (ticket_dict['pass_ticket'],cimte,ticket_dict['skey'])
    response = requests.get(url=url,cookies=ALL_COOKIE_DICT)
    response.encoding = 'utf-8'
    contact_list_dict = json.loads(response.text)
    #print(contact_list_dict.items())
    # for item in contact_list_dict['MemberList']:
    #     print(item['NickName'],item['UserName'])
    return render(request, 'weixin/contact_list.html', {'contact_list_dict':contact_list_dict})

def send_msg(request):
    '''
    # 发送消息
    :param request:
    :return:
    '''
    i = 0
    id = request.GET.get("id")
    while(i<int(id)):
        to_user = request.GET.get("toUser")
        msg = request.GET.get('msg')
        url = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxsendmsg?lang=zh_CN&pass_ticket=%s' %(ticket_dict['pass_ticket'])
        ctime = str(int(time.time()*1000))
        post_dict = {
            'BaseRequest': {
                'DeviceID': "e402310790089148",
                'Sid': ticket_dict['wxsid'],
                'Uin': ticket_dict['wxuin'],
                'Skey': ticket_dict['skey'],
            },
            "Msg": {
                'ClientMsgId': ctime,
                'Content': msg,
                'FromUserName': USER_INIT_DICT['User']['UserName'],
                'LocalID': ctime,
                'ToUserName': to_user.strip(),
                'Type': 1
            },
            'Scene': 0
        }
        time.sleep(0.5)
        # response = requests.post(url=url,json=post_dict,cookies=ALL_COOKIE_DICT)
        response = requests.post(url=url,data=bytes(json.dumps(post_dict,ensure_ascii=False),encoding='utf-8'))
        print(response.text)
        i += 1
    return HttpResponse('轰炸完毕')

def get_msg(request):
    '''
    获取消息
    :param request:
    :return:
    '''
    # 1. 检查是否有消息到来,synckey(出初始化信息中获取)
    # 2. 如果 window.synccheck={retcode:"0",selector:"2"}，有消息到来
    #       ：https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxsync?sid=WFKXEGSyWEgY8eN3&skey=@crypt_d83b5b90_e4138fcba710f4c7d3da566a64d73f40&lang=zh_CN&pass_ticket=MIHBwaa%252BZqty5E5e1l8UkaAEc48bqCP6Km7WxPAP0txDEdDdWC%252BPE8zfHOXg3ywr
    #       获取消息
    #       获取synckey

    print('start....')
    synckey_list = USER_INIT_DICT['SyncKey']['List']
    sync_list = []
    for item in synckey_list:
        temp = "%s_%s" % (item['Key'],item['Val'])
        sync_list.append(temp)
    synckey = "|".join(sync_list)

    r1 = requests.get(
        url = "https://webpush.wx.qq.com/cgi-bin/mmwebwx-bin/synccheck",
        params={
            'r':time.time(),
            'skey':ticket_dict['skey'],
            'sid':ticket_dict['wxsid'],
            'uin':ticket_dict['wxuin'],
            'deviceid':"e402310790089148",
            'synckey':synckey
        },
        cookies = ALL_COOKIE_DICT  # 加入cookies  和 腾讯等待(peding)的时间一样
    )
    if 'retcode:"0",selector:"2"' in r1.text:
        post_list = {
            'BaseRequest': {
                'DeviceID': "e402310790089148",
                'Sid': ticket_dict['wxsid'],
                'Uin': ticket_dict['wxuin'],
                'Skey': ticket_dict['skey'],
            },
            "SyncKey": USER_INIT_DICT['SyncKey'],
            'rr': 1
        }

        r2 = requests.post(
            url='https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxsync',
            params={
                'skey': ticket_dict['skey'],
                'sid': ticket_dict['wxsid'],
                'pass_ticket': ticket_dict['pass_ticket'],
                'lang': 'zh_CN'
            },
            json=post_list
        )
        r2.encoding = 'utf-8'
        msg_dict = json.loads(r2.text)
        for msg_info in msg_dict['AddMsgList']:
            ppp = msg_info['Content']
            print(msg_info['Content'])
        USER_INIT_DICT['SyncKey'] = msg_dict['SyncKey']

    #print(r1.text)
    print('end...')



LIAOTIAN=[]
I = 0
def liaotian(request):
    r1 = request.GET.get('date')
    #print(r1)
    if(len(LIAOTIAN)==12):
        LIAOTIAN.clear()
    LIAOTIAN.append(r1)
    return HttpResponse(json.dumps(r1))

def xianshi(request):
    global LIAOTIAN,I
    # if(I<len(LIAOTIAN)):
    #     I = len(LIAOTIAN)
    #     return HttpResponse(json.dumps(LIAOTIAN))
    # time.sleep(1)
    #print(LIAOTIAN)
    # return HttpResponse(1)
    time.sleep(1)
    return HttpResponse(json.dumps(LIAOTIAN))
import webbrowser
def baidu(request):
    r = request.GET.get('keyinput')
    print(r)
    url = 'https://www.baidu.com/s?ie=UTF-8&wd=%s'%(r)
    #webbrowser.open(url)
    print(url)
    return render(request,'index.html')