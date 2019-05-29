
from django.shortcuts import render
from django.shortcuts import HttpResponse
import requests
import re
from lxml import etree


class Pro4:
    header_ai = {'Referer': 'http://www.iqiyi.com/',
                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.17 Safari/537.36'
                 }
    header_you = {'Referer': 'http://list.youku.com/category/video',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    header_xun = {'Referer':'https://v.qq.com/x/list/movie',
                  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
    }
    header_pp = {'Referer': 'http://list.pptv.com/',
                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

    way=False
    def __init__(self):
        pass
    def search_movies_type(self,u_name,u_type,page):  # 两个参数  根据状态输出规则


        dic1 = {'m': 1, 't': 2, 'z': 6, 'd': 4, 'j': 3}
        dic2 = {'m': 96, 't': 97, 'z': 85, 'd': 100, 'j': 84}
        dic3 = {'m': 1, 't': 2, 'z': 4, 'd': 3, 'j': 210548}
        dic4 ={'m': 'movie', 't': 'tv', 'z': 'variety', 'd': 'cartoon', 'j': 'doco'}
        headers={}
        # 爱奇艺 a/电影m:1 t:2 z:6 d:4 j:3  优酷y / m:96 t:97 z:85 d:100 j:84 pptv  p/m:1 t:2 z:4 d:3 j:210548  腾讯 x/
        url,pa_movie_title,pa_movie_url,pa_movie_pic='','','',''
        url_aiqiyi='http://list.iqiyi.com/www/{}/-------------24-{}-1-iqiyi--.html'.format(dic1[u_type],page)
        url_youku = 'https://list.youku.com/category/show/c_{}_s_1_d_1_p_{}.html'.format(dic2[u_type],page)
        # url_pptv='http://list.pptv.com/category/type_{}.html'.format(dic3[u_type],page)
        url_pptv = 'http://list.pptv.com/channel_list.html?page={}&type={}'.format(page, dic3[u_type])
        if page == 1:
            p=0
            url_tengxun = 'http://v.qq.com/x/list/{}?&offset={}'.format(dic4[u_type],p)
        else:
            p=30 * page - 30
            url_tengxun='http://v.qq.com/x/list/{}?&offset={}'.format(dic4[u_type],p)

        pa_ai_movie_title = '//div[@class="qy-mod-link-wrap"]/a[@class="qy-mod-link"]/@title'
        pa_ai_movie_url = '//div[@class="qy-mod-link-wrap"]/a[@class="qy-mod-link"]/@href'
        pa_ai_movie_pic = '//div[@class="qy-mod-link-wrap"]/a[@class="qy-mod-link"]/img/@src'
        pa_ai_movie_pin = '//div[@class="title-wrap "]/p[@class="main"]/span[@class="text-score"]/text()'

        pa_you_movie_title = '//div[@class="p-thumb"]/a/@title'
        pa_you_movie_url = '//div[@class="p-thumb"]/a/@href'
        pa_you_movie_pic = '//div[@class="p-thumb"]/img[@class="quic"]/@src'

        pa_pp_movie_title='//li/a[@class="ui-list-ct"]/@title'
        pa_pp_movie_url='//li/a[@class="ui-list-ct"]/@href'
        pa_pp_movie_pic='//li/a[@class="ui-list-ct"]/p[@class="ui-pic"]/img/@data-src2'

        pa_tx_movie_title='//li[@class="list_item"]/a[@class="figure"]/img/@alt'
        pa_tx_movie_url ='//li[@class="list_item"]/a[@class="figure"]/@href'
        pa_tx_movie_pic ='//li[@class="list_item"]/a[@class="figure"]/img/@r-lazyload'

        if u_name == "a":#如果是爱奇艺
            url = url_aiqiyi
            pa_movie_title = pa_ai_movie_title
            pa_movie_url = pa_ai_movie_url
            pa_movie_pic = pa_ai_movie_pic
            pa_movie_pin = pa_ai_movie_pin
            headers = self.header_ai
        elif u_name=="y":#如果是优酷
            url=url_youku
            pa_movie_title=pa_you_movie_title
            pa_movie_url=pa_you_movie_url
            pa_movie_pic=pa_you_movie_pic
            headers=self.header_you

        elif u_name=="p":#如果是PPTV
            url=url_pptv
            pa_movie_title=pa_pp_movie_title
            pa_movie_url=pa_pp_movie_url
            pa_movie_pic=pa_pp_movie_pic
            headers=self.header_pp
        elif u_name=="x":#如果是腾讯
            url=url_tengxun
            pa_movie_title=pa_tx_movie_title
            pa_movie_url=pa_tx_movie_url
            pa_movie_pic=pa_tx_movie_pic
            headers=self.header_xun
        if u_name == 'a':
            return url,pa_movie_pin,pa_movie_title,pa_movie_url,pa_movie_pic,headers
        else:
            return url,pa_movie_title, pa_movie_url, pa_movie_pic, headers

    def get_movie_res(self,u_name,u_type,page):#输出电影名 链接，图片
        if u_name == 'a':
            url,pa_movie_pin,pa_movie_title, pa_movie_url, pa_movie_pic,headers=self.search_movies_type(u_name,u_type,page)
        else:
            url,pa_movie_title, pa_movie_url, pa_movie_pic, headers = self.search_movies_type(u_name, u_type, page)
        res=requests.get(url=url,headers=headers).content.decode('utf-8')
        #print(res)

        html = etree.HTML(res)
        movie_url = html.xpath(pa_movie_url)
        movie_title = html.xpath(pa_movie_title)
        movie_src_pic = html.xpath(pa_movie_pic)
        if u_name == 'a':
            if(u_type == 'm'):
                movie_pin = html.xpath(pa_movie_pin)
            else:
                movie_pin = 0
        # print(len(movie_pin), movie_pin)
        # print(len(movie_pin1), movie_pin1)
        # print(len(movie_title), movie_title)
        # print(len(movie_url), movie_url)
        # print(len(movie_src_pic), movie_src_pic)
        if u_name == 'a':
            return movie_pin,movie_url,movie_title,movie_src_pic
        else:
            return movie_url, movie_title, movie_src_pic

    def change_urlink(self,lis):
        for i in range(len(lis)):
            if '\\' in lis[i]: #如果字符串有\\就把他替换成空格
                lis[i] = lis[i].replace('\\','')
        # print(lis)
        return lis

    def change_youku_link(self,urls):
        pa_link='//.+[.]html'       #匹配
        if re.match(pa_link,urls): # 在原有的地址上加上http：
            urls='http:'+urls
        return urls

    def get_more_tv_urls(self,url,u_name,u_type): # 获取电视剧分集链接
        tv_dic_new = {}
        if u_name == 'y':
            url = self.change_youku_link(url)
            print(url)
            res = requests.get(url,headers=self.header_you).text.encode(encoding="utf-8").decode('utf-8')# 解码
            html = etree.HTML(res)
            print(res)
            if u_type=="m" or u_type=="t":
                self.tv_more_title = html.xpath('//div[@class="item item-num"]/@title')
                self.tv_more_url = html.xpath('//div[@class="item item-num"]/a[@class="sn"]/@href')
            elif u_type=="d":
                self.tv_more_title = html.xpath('//div[@class="item item-txt"]/@title')
                self.tv_more_url = html.xpath('//div[@class="item item-txt"]/a[@class="sn"]/@href')
            elif u_type=="z":
                self.tv_more_title = html.xpath('//div[@class="item item-cover"]/@title')
                self.tv_more_url = html.xpath('//div[@class="item item-cover"]/a/@href')
            elif u_type == "j":
                self.tv_more_title = html.xpath('//div[@class="item item-cover"]/@title')
                self.tv_more_url = html.xpath('//div[@class="item item-cover"]/a/@href')
        elif u_name == 'a':
            res = requests.get(url,headers=self.header_ai).text.encode(encoding="utf-8").decode('utf-8')
            html = etree.HTML(res)
            #print(res) #打印整个网页
            if u_type=="m" or u_type=="t" or u_type=="d":
                self.tv_more_title = html.xpath(
                    '//ul/li[@data-albumlist-elem="playItem"]/div[@class="site-piclist_pic"]/a[1]/@title')
                self.tv_more_url = html.xpath(
                    '//ul/li[@data-albumlist-elem="playItem"]/div[@class="site-piclist_pic"]/a[1]/@href')
            elif u_type=="z" or u_type=="j":
                self.tv_more_title = html.xpath('//div[@class="recoAlbumTit"]/a[1]/@title')
                self.tv_more_url = html.xpath('//div[@class="recoAlbumTit"]/a[1]/@href')
        elif u_name == 'p':
            res = requests.get(url, headers=self.header_pp).text.encode(encoding='utf-8').decode('utf-8')
            # html = etree.HTML(res)
            self.tv_more_url2 = re.compile('{"url":"(.+?)"').findall(res)
            self.tv_more_url = self.change_urlink(self.tv_more_url2)
            self.tv_more_title = ["第{}集".format(x) for x in range(1, len(self.tv_more_url) + 1)]
        elif u_name == 'x':
            res = requests.get(url,headers=self.header_xun).text.encode(encoding="utf-8").decode('utf-8')
            html = etree.HTML(res)
            print(res)
            if u_type=="m":
                self.tv_more_title = html.xpath('//ul/li[@class="list_item"]/@data-title')
                self.tv_more_url = html.xpath('//ul/li[@class="list_item"]/a[@class="figure"]/@href')
            elif  u_type=="t":
                self.tv_more_url =html.xpath('//div[@class="mod_episode"]/span[@class="item"]/a/@href')
                self.tv_more_title = ["第{}集".format(x) for x in range(1, len(self.tv_more_url) + 1)]
            elif u_type=="z" or u_type=="j":
                self.tv_more_url = html.xpath('//ul/li[@class="list_item"]/a[@class="figure"]/@href')
                self.tv_more_title = ["第{}集".format(x) for x in range(1, len(self.tv_more_url) + 1)]
            elif u_type=="d":
                self.tv_more_url = html.xpath('//div/span[@class="item"]/a/@href')
                self.tv_more_title = ["第{}集".format(x) for x in range(1, len(self.tv_more_url) + 1)]


        # m = 0
        # for i, j in (self.tv_more_title, self.tv_more_url):
        #     tv_dic_new[m] = {'title':i,'href':j}
        #     m=m+1

        # print(len(self.tv_more_title), self.tv_more_title)
        # print(len(self.tv_more_url), self.tv_more_url)
        return self.tv_more_title,self.tv_more_url

# 爱奇艺

aqiyimovieList = []
aqifenji = []
# url = 'http://jx.du2.cc/?url='
url = 'http://mv.688ing.com/player?url='

#########      控制 爱奇艺的   页数
page = 1
page_TV = 1
page_zongyi = 1
page_dongman = 1
page_jilu = 1

def pagejia(page1):
    global page
    page = page1 + 1

def pagejian(page1):
    global page
    if page == 1:
        page = 1
    else:
        page = page1 -1


def pagejia_TV(page1):
    global page_TV
    page_TV = page1 + 1

def pagejian_TV(page1):
    global page_TV
    if page_TV == 1:
        page_TV = 1
    else:
        page_TV = page1 -1


def pagejia_dongman(page1):
    global page_dongman
    page_dongman = page1 + 1

def pagejian_dongman(page1):
    global page_dongman
    if page_dongman == 1:
        page_dongman = 1
    else:
        page_dongman = page1 - 1

def pagejia_zongyi(page1):
    global page_zongyi
    page_zongyi = page1 + 1

def pagejian_zongyi(page1):
    global page_zongyi
    if page_zongyi == 1:
        page_zongyi = 1
    else:
        page_zongyi = page1 - 1

def pagejia_jilu(page1):
    global page_jilu
    page_jilu = page1 + 1

def pagejian_jilu(page1):
    global page_jilu
    if page_jilu == 1:
        page_jilu = 1
    else:
        page_jilu = page1 - 1

def deleat():       #  给数组 清空
    aqiyimovieList.clear()
def fenji_deleat():
    aqifenji.clear()


######################              搜索  ###############################


def sousuo(request):
    page = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
            30]

    q = request.GET.get('keyboard')
    url_SOUSUO = 'https://so.iqiyi.com/so/q_{}'.format(q)
    #print(url_SOUSUO)
    header_ai = {
                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.17 Safari/537.36'
                 }
    ai_title = '//ul[@class="mod_result_list"]/li/a[@class="figure  figure-180236"]/img/@title'
    ai_url = '//ul[@class="mod_result_list"]/li/a[@class="figure  figure-180236"]/@href'
    ai_pic = '//ul[@class="mod_result_list"]/li/a[@class="figure  figure-180236"]/img/@src'

    ai_title1 = '//ul[@class="mod_result_list"]/li/a[@class="figure  figure-180236 "]/img/@title'
    ai_url1 = '//ul[@class="mod_result_list"]/li/a[@class="figure  figure-180236 "]/@href'
    ai_pic1 = '//ul[@class="mod_result_list"]/li/a[@class="figure  figure-180236 "]/img/@src'

    if len(aqiyimovieList) != 0:        #每次调用的时候 都判断一下是否有数据，有就清空
        deleat()
    res = requests.get(url_SOUSUO, headers=header_ai).text.encode(encoding="utf-8").decode('utf-8')  # 解码
    #print(res)

    movie_title = movie_url = movie_src_pic = []
    html = etree.HTML(res)
    suo_title2 = html.xpath(ai_title)
    suo_url2 = html.xpath(ai_url)
    suo_pic2 = html.xpath(ai_pic)

    suo_title1 = html.xpath(ai_title1)
    suo_url1 = html.xpath(ai_url1)
    suo_pic1 = html.xpath(ai_pic1)

    movie_title = suo_title1 + suo_title2
    movie_url = suo_url1 + suo_url2
    movie_src_pic = suo_pic1 + suo_pic2

    # print(movie_title)
    # print(movie_url)
    # print(movie_src_pic)
    for i in range(0,len(movie_title)):
        aqiyimovieLists = {'page':page[i],'movie_url': movie_url[i], 'movie_title': movie_title[i], 'movie_src_pic': movie_src_pic[i]}
        aqiyimovieList.append(aqiyimovieLists)
    #print(aqiyimovieList)
    return render(request,'aqiyi/sousuo.html',{"aqisousuo":aqiyimovieList,"url":url})

def sousuo_fenji(request,aqiyimovieLists):
    header_ai = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.17 Safari/537.36'
    }

    if len(aqifenji) != 0:
        fenji_deleat()
    #print(aqiyimovieLists)
    id = int (aqiyimovieLists)-1

    aqi = aqiyimovieList[id]
    #print(aqi)
    m = 0 #来 计数 有多少集数
    #print(aqi['movie_url'])
    res = requests.get(aqi['movie_url'], headers=header_ai).text.encode(encoding="utf-8").decode('utf-8')
    html = etree.HTML(res)

    tv_movie_url = html.xpath('//ul[@class="site-piclist site-piclist-12068"]/li/div[@class="site-piclist_pic"]/a/@href')
    tv_movie_title = html.xpath('//ul[@class="site-piclist site-piclist-12068"]/li/div[@class="site-piclist_pic"]/a/@title')
    for i in tv_movie_url:
        a ="第{}集 ".format(m+1) + tv_movie_title[m]
        aqifenji1 = {'tv_more_title':a, 'tv_more_url': i}
        aqifenji.append(aqifenji1)
        m = m+1
    #print(aqifenji)
    #print(tv_dic_new)
    return render(request, "aqiyi/aqiyi_fenji.html", {'aqifenji':aqifenji,'aqi':aqi,'url':url})


# Create your views here.


def aqiyi(request):
    if len(aqiyimovieList) != 0:        #每次调用的时候 都判断一下是否有数据，有就清空
        deleat()
    p = Pro4()
    movie_pin,movie_url, movie_title, movie_src_pic, = p.get_movie_res('a', 'm',1)

    for i in range(len(movie_title)):
        aqiyimovieLists = {'movie_url': movie_url[i], 'movie_title': movie_title[i], 'movie_src_pic': movie_src_pic[i],'movie_pin':movie_pin[i]}
        aqiyimovieList.append(aqiyimovieLists)
    #print(aqiyimovieList)
    return render(request,"aqiyi/aqiyi.html",{'aqiyimovieList': aqiyimovieList,'url':url,'page':'1'})

def aqiyi_movie_dianyin(request,page_id):
    global page
    if page_id == '2':
        pagejia(page)
        print(page)
    elif page_id == '1':
        pagejian(page)
        print(page)
    elif page_id == '0':
        page = 1
    p = Pro4()
    movie_pin,movie_url, movie_title, movie_src_pic, = p.get_movie_res('a', 'm', page)
    if len(aqiyimovieList) != 0:
        deleat()
    for i in range(len(movie_title)):
        aqiyimovieLists = {'movie_url': movie_url[i], 'movie_title': movie_title[i], 'movie_src_pic': movie_src_pic[i],'movie_pin':movie_pin[i]}
        aqiyimovieList.append(aqiyimovieLists)
    #print(aqiyimovieList)
    return render(request,"aqiyi/aqiyi.html",{'aqiyimovieList': aqiyimovieList,'url':url,'page':page})

def aqi_movie_TV(request,page_id):
    page = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
            30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48]
    global page_TV
    if page_id == '2':
        pagejia_TV(page_TV)
        #print(page_MV)
    elif page_id == '1':
        pagejian_TV(page_TV)
       # print(page_MV)
    elif page_id == '0':
        page_TV = 1

    if len(aqiyimovieList) != 0:
        deleat()
    p = Pro4()
    movie_pin, movie_url, movie_title, movie_src_pic, = p.get_movie_res('a', 't', page_TV)
    for i in range(len(movie_title)):
        aqiyimovieLists = {'page':page[i],'movie_url': movie_url[i], 'movie_title': movie_title[i], 'movie_src_pic': movie_src_pic[i]}
        aqiyimovieList.append(aqiyimovieLists)
   # print(aqiyimovieList)
    return render(request, "aqiyi/aqiyi_TV.html", {'aqiyimovieList': aqiyimovieList,'f':'t','url':url,'page_TV':page_TV})

def aqi_movie_zongyi(request,page_id):
    page = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
            30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48]

    global page_zongyi
    if page_id == '2':
        pagejia_zongyi(page_zongyi)

    elif page_id == '1':
        pagejian_zongyi(page_zongyi)

    elif page_id == '0':
        page_zongyi = 1

    if len(aqiyimovieList) != 0:
        deleat()
    p = Pro4()
    movie_pin, movie_url, movie_title, movie_src_pic, = p.get_movie_res('a', 'z', page_zongyi)

    for i in range(len(movie_title)):
        aqiyimovieLists = {'page':page[i],'movie_url': movie_url[i], 'movie_title': movie_title[i], 'movie_src_pic': movie_src_pic[i]}
        aqiyimovieList.append(aqiyimovieLists)
   # print(aqiyimovieList)
    return render(request, "aqiyi/aqiyi_zongyi.html", {'aqiyimovieList': aqiyimovieList,'f':'z','url':url,'page_zongyi':page_zongyi})

def aqi_movie_dongman(request,page_id):
    page = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
            30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48]

    global page_dongman
    if page_id == '2':
        pagejia_dongman(page_dongman)

    elif page_id == '1':
        pagejian_dongman(page_dongman)

    elif page_id == '0':
        page_dongman = 1

    if len(aqiyimovieList) != 0:
        deleat()
    p = Pro4()
    movie_pin, movie_url, movie_title, movie_src_pic, = p.get_movie_res('a', 'd', page_dongman)

    for i in range(len(movie_title)):
        aqiyimovieLists = {'page':page[i],'movie_url': movie_url[i], 'movie_title': movie_title[i], 'movie_src_pic': movie_src_pic[i]}
        aqiyimovieList.append(aqiyimovieLists)
   # print(aqiyimovieList)
    return render(request, "aqiyi/aqiyi_dongman.html", {'aqiyimovieList': aqiyimovieList, 'page_dongman': page_dongman,'f':'d','url':url})

def aqi_movie_jilu(request,page_id):
    page = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
            30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48]

    global page_jilu
    if page_id == '2':
        pagejia_jilu(page_jilu)

    elif page_id == '1':
        pagejian_jilu(page_jilu)

    elif page_id == '0':
        page_jilu = 1


    if len(aqiyimovieList) != 0:
        deleat()
    p = Pro4()
    movie_pin, movie_url, movie_title, movie_src_pic, = p.get_movie_res('a', 'j', page_jilu)

    for i in range(len(movie_title)):
        aqiyimovieLists = {'page':page[i],'movie_url': movie_url[i], 'movie_title': movie_title[i], 'movie_src_pic': movie_src_pic[i]}
        aqiyimovieList.append(aqiyimovieLists)
   # print(aqiyimovieList)
    return render(request, "aqiyi/aqiyi_jilu.html", {'aqiyimovieList': aqiyimovieList, 'page_jilu': page_jilu,'f':'j','url':url})

def aqi_movie_fenji_jilu(request,aqiyimovieLists):   #aqiyimovieLists 传过来的 ID
    if len(aqifenji) != 0:
        fenji_deleat()
   # print(aqiyimovieLists)
    id = int (aqiyimovieLists)-1

    aqi = aqiyimovieList[id]

    m = 0 #来 计数 有多少集数
    p = Pro4()
    tv_more_title,tv_more_url = p.get_more_tv_urls(aqi['movie_url'],'a','j')

    for i in tv_more_url:
        a ="第{}集 ".format(m+1) + tv_more_title[m]
        aqifenji1 = {'tv_more_title':a, 'tv_more_url': i}
        aqifenji.append(aqifenji1)
        m = m+1
   # print(aqifenji)
    #print(tv_dic_new)
    return render(request, "aqiyi/aqiyi_fenji.html", {'aqifenji':aqifenji,'aqi':aqi,'url':url})

def aqi_movie_fenji_TV(request,aqiyimovieLists):   #aqiyimovieLists 传过来的 ID
    if len(aqifenji) != 0:
        fenji_deleat()
    #print(aqiyimovieLists)
    id = int (aqiyimovieLists)-1

    aqi = aqiyimovieList[id]

    m = 0 #来 计数 有多少集数
    p = Pro4()
    tv_more_title,tv_more_url = p.get_more_tv_urls(aqi['movie_url'],'a','t')

    for i in tv_more_url:
        a ="第{}集 ".format(m+1) + tv_more_title[m]
        aqifenji1 = {'tv_more_title':a, 'tv_more_url': i}
        aqifenji.append(aqifenji1)
        m = m+1
   # print(aqifenji)
    #print(tv_dic_new)
    return render(request, "aqiyi/aqiyi_fenji.html", {'aqifenji':aqifenji,'aqi':aqi,'url':url})

def aqi_movie_fenji_zongyi(request,aqiyimovieLists):   #aqiyimovieLists 传过来的 ID
    if len(aqifenji) != 0:
        fenji_deleat()
   # print(aqiyimovieLists)
    id = int (aqiyimovieLists)-1

    aqi = aqiyimovieList[id]

    m = 0 #来 计数 有多少集数
    p = Pro4()
    tv_more_title,tv_more_url = p.get_more_tv_urls(aqi['movie_url'],'a','z')

    for i in tv_more_url:
        aqifenji1 = {'tv_more_title':tv_more_title[m], 'tv_more_url': i}
        aqifenji.append(aqifenji1)
        m = m+1
  #  print(aqifenji)
    #print(tv_dic_new)
    return render(request, "aqiyi/aqiyi_fenji.html", {'aqifenji':aqifenji,'aqi':aqi,'url':url})

def aqi_movie_fenji_dongman(request,aqiyimovieLists):   #aqiyimovieLists 传过来的 ID
    if len(aqifenji) != 0:
        fenji_deleat()
  #  print(aqiyimovieLists)
    id = int (aqiyimovieLists)-1

    aqi = aqiyimovieList[id]

    m = 0 #来 计数 有多少集数
    p = Pro4()
    tv_more_title,tv_more_url = p.get_more_tv_urls(aqi['movie_url'],'a','d')

    for i in tv_more_url:
        aqifenji1 = {'tv_more_title':tv_more_title[m], 'tv_more_url': i}
        aqifenji.append(aqifenji1)
        m = m+1
  #  print(aqifenji)
    #print(tv_dic_new)
    return render(request, "aqiyi/aqiyi_fenji.html", {'aqifenji':aqifenji,'aqi':aqi,'url':url})







####             优    酷

def youku(request):
    if len(aqiyimovieList) != 0:        #每次调用的时候 都判断一下是否有数据，有就清空
        deleat()
    p = Pro4()
    movie_url, movie_title, movie_src_pic, = p.get_movie_res('y', 'm',1)

    for i in range(0,30):
        aqiyimovieLists = {'movie_url': movie_url[i], 'movie_title': movie_title[i], 'movie_src_pic': movie_src_pic[i]}
        aqiyimovieList.append(aqiyimovieLists)
   # print(aqiyimovieList)
    return render(request, "youku/youku.html", {'aqiyimovieList': aqiyimovieList, 'url':url, 'page': '1'})


def you_movie_dianyin(request,page_id):
    global page
    if page_id == '2':
        pagejia(page)
        print(page)
    elif page_id == '1':
        pagejian(page)
        print(page)
    elif page_id == '0':
        page = 1
    p = Pro4()
    movie_url, movie_title, movie_src_pic, = p.get_movie_res('y', 'm', page)
    if len(aqiyimovieList) != 0:
        deleat()
    for i in range(0, 30):
        aqiyimovieLists = {'movie_url': movie_url[i], 'movie_title': movie_title[i], 'movie_src_pic': movie_src_pic[i]}
        aqiyimovieList.append(aqiyimovieLists)
  #  print(aqiyimovieList)
    return render(request, "youku/youku.html", {'aqiyimovieList': aqiyimovieList, 'url': url, 'page': page})

def you_movie_TV(request,page_id):
    page = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
            30]
    global page_TV
    if page_id == '2':
        pagejia_TV(page_TV)
        # print(page_MV)
    elif page_id == '1':
        pagejian_TV(page_TV)
    # print(page_MV)
    elif page_id == '0':
        page_TV = 1

    if len(aqiyimovieList) != 0:
        deleat()
    p = Pro4()
    movie_url, movie_title, movie_src_pic, = p.get_movie_res('y', 't', page_TV)

    for i in range(0, 30):
        aqiyimovieLists = {'page': page[i], 'movie_url': movie_url[i], 'movie_title': movie_title[i],
                           'movie_src_pic': movie_src_pic[i]}
        aqiyimovieList.append(aqiyimovieLists)
  #  print(aqiyimovieList)
    return render(request, "youku/youku_TV.html",{'aqiyimovieList': aqiyimovieList, 'f': 't', 'url': url, 'page_TV': page_TV})
def you_movie_zongyi(request,page_id):
    page = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
            30]

    global page_zongyi
    if page_id == '2':
        pagejia_zongyi(page_zongyi)

    elif page_id == '1':
        pagejian_zongyi(page_zongyi)

    elif page_id == '0':
        page_zongyi = 1

    if len(aqiyimovieList) != 0:
        deleat()
    p = Pro4()
    movie_url, movie_title, movie_src_pic, = p.get_movie_res('y', 'z', page_zongyi)

    for i in range(0, 30):
        aqiyimovieLists = {'page': page[i], 'movie_url': movie_url[i], 'movie_title': movie_title[i],
                           'movie_src_pic': movie_src_pic[i]}
        aqiyimovieList.append(aqiyimovieLists)
  #  print(aqiyimovieList)
    return render(request, "youku/youku_zongyi.html",{'aqiyimovieList': aqiyimovieList, 'f': 'z', 'url': url, 'page_zongyi': page_zongyi})

def you_movie_dongman(request,page_id):
    page = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
            30]

    global page_dongman
    if page_id == '2':
        pagejia_dongman(page_dongman)

    elif page_id == '1':
        pagejian_dongman(page_dongman)

    elif page_id == '0':
        page_dongman = 1

    if len(aqiyimovieList) != 0:
        deleat()
    p = Pro4()
    movie_url, movie_title, movie_src_pic, = p.get_movie_res('y', 'd', page_dongman)

    for i in range(0, 30):
        aqiyimovieLists = {'page': page[i], 'movie_url': movie_url[i], 'movie_title': movie_title[i],
                           'movie_src_pic': movie_src_pic[i]}
        aqiyimovieList.append(aqiyimovieLists)
  #  print(aqiyimovieList)
    return render(request, "youku/youku_dongman.html",{'aqiyimovieList': aqiyimovieList, 'page_dongman': page_dongman, 'f': 'd', 'url': url})

def you_movie_jilu(request,page_id):
    page = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
            30]

    global page_jilu
    if page_id == '2':
        pagejia_jilu(page_jilu)

    elif page_id == '1':
        pagejian_jilu(page_jilu)

    elif page_id == '0':
        page_jilu = 1

    if len(aqiyimovieList) != 0:
        deleat()
    p = Pro4()
    movie_url, movie_title, movie_src_pic, = p.get_movie_res('y', 'j', page_jilu)

    for i in range(0, 30):
        aqiyimovieLists = {'page': page[i], 'movie_url': movie_url[i], 'movie_title': movie_title[i],
                           'movie_src_pic': movie_src_pic[i]}
        aqiyimovieList.append(aqiyimovieLists)
  #  print(aqiyimovieList)
    return render(request, "youku/youku_jilu.html",{'aqiyimovieList': aqiyimovieList, 'page_jilu': page_jilu, 'f': 'j', 'url': url})


def you_movie_fenji_jilu(request,aqiyimovieLists):   #aqiyimovieLists 传过来的 ID
    if len(aqifenji) != 0:
        fenji_deleat()
  #  print(aqiyimovieLists)
    id = int (aqiyimovieLists)-1

    aqi = aqiyimovieList[id]

    m = 0 #来 计数 有多少集数
    p = Pro4()
    tv_more_title,tv_more_url = p.get_more_tv_urls(aqi['movie_url'],'y','j')

    for i in tv_more_url:
        a ="第{}集 ".format(m+1) + tv_more_title[m]
        aqifenji1 = {'tv_more_title':a, 'tv_more_url': i}
        aqifenji.append(aqifenji1)
        m = m+1
  # print(aqifenji)
    #print(tv_dic_new)
    return render(request, "youku/you_fenji.html", {'aqifenji':aqifenji,'aqi':aqi,'url':url})


def you_movie_fenji_TV(request,aqiyimovieLists):   #aqiyimovieLists 传过来的 ID
    if len(aqifenji) != 0:
        fenji_deleat()
   # print(aqiyimovieLists)
    id = int (aqiyimovieLists)-1
   # print(id)
    aqi = aqiyimovieList[id]

    m = 0 #来 计数 有多少集数
    p = Pro4()
    tv_more_title,tv_more_url = p.get_more_tv_urls(aqi['movie_url'],'y','t')

    for i in tv_more_url:
        a ="第{}集 ".format(m+1) + tv_more_title[m]
        aqifenji1 = {'tv_more_title':a, 'tv_more_url': i}
        aqifenji.append(aqifenji1)
        m = m+1
   # print(aqifenji)
    #print(tv_dic_new)
    return render(request, "youku/you_fenji.html", {'aqifenji':aqifenji,'aqi':aqi,'url':url})

def you_movie_fenji_zongyi(request,aqiyimovieLists):   #aqiyimovieLists 传过来的 ID
    if len(aqifenji) != 0:
        fenji_deleat()
   # print(aqiyimovieLists)
    id = int (aqiyimovieLists)-1

    aqi = aqiyimovieList[id]

    m = 0 #来 计数 有多少集数
    p = Pro4()
    tv_more_title,tv_more_url = p.get_more_tv_urls(aqi['movie_url'],'y','z')

    for i in tv_more_url:
        aqifenji1 = {'tv_more_title':tv_more_title[m], 'tv_more_url': i}
        aqifenji.append(aqifenji1)
        m = m+1
   # print(aqifenji)
    #print(tv_dic_new)
    return render(request, "youku/you_fenji.html", {'aqifenji':aqifenji,'aqi':aqi,'url':url})

def you_movie_fenji_dongman(request,aqiyimovieLists):   #aqiyimovieLists 传过来的 ID
    if len(aqifenji) != 0:
        fenji_deleat()
   # print(aqiyimovieLists)
    id = int (aqiyimovieLists)-1

    aqi = aqiyimovieList[id]

    m = 0 #来 计数 有多少集数
    p = Pro4()
    tv_more_title,tv_more_url = p.get_more_tv_urls(aqi['movie_url'],'y','d')

    for i in tv_more_url:
        aqifenji1 = {'tv_more_title':tv_more_title[m], 'tv_more_url': i}
        aqifenji.append(aqifenji1)
        m = m+1
   # print(aqifenji)
    #print(tv_dic_new)
    return render(request, "youku/you_fenji.html", {'aqifenji':aqifenji,'aqi':aqi,'url':url})











###              腾讯
def teng(request):
    if len(aqiyimovieList) != 0:        #每次调用的时候 都判断一下是否有数据，有就清空
        deleat()
    p = Pro4()
    movie_url, movie_title, movie_src_pic, = p.get_movie_res('x', 'm',1)

    for i in range(0,30):
        aqiyimovieLists = {'movie_url': movie_url[i], 'movie_title': movie_title[i], 'movie_src_pic': movie_src_pic[i]}
        aqiyimovieList.append(aqiyimovieLists)
   # print(aqiyimovieList)
    return render(request, "tengxun/tengxun.html", {'aqiyimovieList': aqiyimovieList, 'url':url, 'page': '1'})

def teng_movie_dianyin(request,page_id):
    global page
    if page_id == '2':
        pagejia(page)
        print(page)
    elif page_id == '1':
        pagejian(page)
        print(page)
    elif page_id == '0':
        page = 1
    p = Pro4()
    movie_url, movie_title, movie_src_pic, = p.get_movie_res('x', 'm', page)
    if len(aqiyimovieList) != 0:
        deleat()
    for i in range(0, 30):
        aqiyimovieLists = {'movie_url': movie_url[i], 'movie_title': movie_title[i], 'movie_src_pic': movie_src_pic[i]}
        aqiyimovieList.append(aqiyimovieLists)
   # print(aqiyimovieList)
    return render(request, "tengxun/tengxun.html", {'aqiyimovieList': aqiyimovieList, 'url': url, 'page': page})

def teng_movie_TV(request,page_id):
    page = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
            30]
    global page_TV
    if page_id == '2':
        pagejia_TV(page_TV)
        # print(page_MV)
    elif page_id == '1':
        pagejian_TV(page_TV)
    # print(page_MV)
    elif page_id == '0':
        page_TV = 1

    if len(aqiyimovieList) != 0:
        deleat()
    p = Pro4()
    movie_url, movie_title, movie_src_pic, = p.get_movie_res('x', 't', page_TV)

    for i in range(0, 30):
        aqiyimovieLists = {'page': page[i], 'movie_url': movie_url[i], 'movie_title': movie_title[i],
                           'movie_src_pic': movie_src_pic[i]}
        aqiyimovieList.append(aqiyimovieLists)
  #  print(aqiyimovieList)
    return render(request, "tengxun/teng_TV.html",{'aqiyimovieList': aqiyimovieList, 'f': 't', 'url': url, 'page_TV': page_TV})
def teng_movie_zongyi(request,page_id):
    page = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
            30]

    global page_zongyi
    if page_id == '2':
        pagejia_zongyi(page_zongyi)

    elif page_id == '1':
        pagejian_zongyi(page_zongyi)

    elif page_id == '0':
        page_zongyi = 1

    if len(aqiyimovieList) != 0:
        deleat()
    p = Pro4()
    movie_url, movie_title, movie_src_pic, = p.get_movie_res('x', 'z', page_zongyi)

    for i in range(0, 30):
        aqiyimovieLists = {'page': page[i], 'movie_url': movie_url[i], 'movie_title': movie_title[i],
                           'movie_src_pic': movie_src_pic[i]}
        aqiyimovieList.append(aqiyimovieLists)
   # print(aqiyimovieList)
    return render(request, "tengxun/teng_zongyi.html",{'aqiyimovieList': aqiyimovieList, 'f': 'z', 'url': url, 'page_zongyi': page_zongyi})

def teng_movie_dongman(request,page_id):
    page = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
            30]

    global page_dongman
    if page_id == '2':
        pagejia_dongman(page_dongman)

    elif page_id == '1':
        pagejian_dongman(page_dongman)

    elif page_id == '0':
        page_dongman = 1

    if len(aqiyimovieList) != 0:
        deleat()
    p = Pro4()
    movie_url, movie_title, movie_src_pic, = p.get_movie_res('x', 'd', page_dongman)

    for i in range(0, 30):
        aqiyimovieLists = {'page': page[i], 'movie_url': movie_url[i], 'movie_title': movie_title[i],
                           'movie_src_pic': movie_src_pic[i]}
        aqiyimovieList.append(aqiyimovieLists)
   # print(aqiyimovieList)
    return render(request, "tengxun/teng_dongman.html",{'aqiyimovieList': aqiyimovieList, 'page_dongman': page_dongman, 'f': 'd', 'url': url})

def teng_movie_jilu(request,page_id):
    page = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
            30]

    global page_jilu
    if page_id == '2':
        pagejia_jilu(page_jilu)

    elif page_id == '1':
        pagejian_jilu(page_jilu)

    elif page_id == '0':
        page_jilu = 1

    if len(aqiyimovieList) != 0:
        deleat()
    p = Pro4()
    movie_url, movie_title, movie_src_pic, = p.get_movie_res('x', 'j', page_jilu)

    for i in range(0, 30):
        aqiyimovieLists = {'page': page[i], 'movie_url': movie_url[i], 'movie_title': movie_title[i],
                           'movie_src_pic': movie_src_pic[i]}
        aqiyimovieList.append(aqiyimovieLists)
   # print(aqiyimovieList)
    return render(request, "tengxun/teng_jilu.html",{'aqiyimovieList': aqiyimovieList, 'page_jilu': page_jilu, 'f': 'j', 'url': url})


def teng_movie_fenji_jilu(request,aqiyimovieLists):   #aqiyimovieLists 传过来的 ID
    if len(aqifenji) != 0:
        fenji_deleat()
   # print(aqiyimovieLists)
    id = int (aqiyimovieLists)-1

    aqi = aqiyimovieList[id]

    m = 0 #来 计数 有多少集数
    p = Pro4()
    tv_more_title,tv_more_url = p.get_more_tv_urls(aqi['movie_url'],'x','j')

    for i in tv_more_url:

        aqifenji1 = {'tv_more_title':tv_more_title[m], 'tv_more_url': 'http:v.qq.com'+i}
        aqifenji.append(aqifenji1)
        m = m+1
   # print(aqifenji)
    #print(tv_dic_new)
    return render(request, "youku/you_fenji.html", {'aqifenji':aqifenji,'aqi':aqi,'url':url})


def teng_movie_fenji_TV(request,aqiyimovieLists):   #aqiyimovieLists 传过来的 ID
    if len(aqifenji) != 0:
        fenji_deleat()
   # print(aqiyimovieLists)
    id = int (aqiyimovieLists)-1
   # print(id)
    aqi = aqiyimovieList[id]

    m = 0 #来 计数 有多少集数
    p = Pro4()
    tv_more_title,tv_more_url = p.get_more_tv_urls(aqi['movie_url'],'x','t')

    for i in tv_more_url:

        aqifenji1 = {'tv_more_title':tv_more_title[m], 'tv_more_url': 'http:v.qq.com'+i}
        aqifenji.append(aqifenji1)
        m = m+1
   # print(aqifenji)
    #print(tv_dic_new)
    return render(request, "youku/you_fenji.html", {'aqifenji':aqifenji,'aqi':aqi,'url':url})

def teng_movie_fenji_zongyi(request,aqiyimovieLists):   #aqiyimovieLists 传过来的 ID
    if len(aqifenji) != 0:
        fenji_deleat()
   # print(aqiyimovieLists)
    id = int (aqiyimovieLists)-1

    aqi = aqiyimovieList[id]

    m = 0 #来 计数 有多少集数
    p = Pro4()
    tv_more_title,tv_more_url = p.get_more_tv_urls(aqi['movie_url'],'x','z')

    for i in tv_more_url:
        aqifenji1 = {'tv_more_title':tv_more_title[m], 'tv_more_url': 'http:v.qq.com'+i}
        aqifenji.append(aqifenji1)
        m = m+1
   # print(aqifenji)
    #print(tv_dic_new)
    return render(request, "youku/you_fenji.html", {'aqifenji':aqifenji,'aqi':aqi,'url':url})

def teng_movie_fenji_dongman(request,aqiyimovieLists):   #aqiyimovieLists 传过来的 ID
    if len(aqifenji) != 0:
        fenji_deleat()
   # print(aqiyimovieLists)
    id = int (aqiyimovieLists)-1

    aqi = aqiyimovieList[id]

    m = 0 #来 计数 有多少集数
    p = Pro4()
    tv_more_title,tv_more_url = p.get_more_tv_urls(aqi['movie_url'],'x','d')

    for i in tv_more_url:
        aqifenji1 = {'tv_more_title':tv_more_title[m], 'tv_more_url': 'http:v.qq.com'+i}
        aqifenji.append(aqifenji1)
        m = m+1
   # print(aqifenji)
    #print(tv_dic_new)
    return render(request, "youku/you_fenji.html", {'aqifenji':aqifenji,'aqi':aqi,'url':url})




def main(request):
    return render(request,'index.html')
def siga(request):
    return render(request,'index1.html')
