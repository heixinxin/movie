from django.shortcuts import render,HttpResponse
# Create your views here.
import requests
from lxml import etree
import json

href_mu =[]
def xiaoshuo(request):
    global href_mu
    xiaosuo = []
    r = request.GET.get('xiaoshuo_text')
    url = 'https://www.qidian.com/search?kw=%s'%(r)
    response = requests.get(url).text
    #print(response)
    html = etree.HTML(response)
    title1 = html.xpath('//ul/li[@class="res-book-item"]/div[@class="book-mid-info"]/h4/a/cite[@class="red-kw"]/text()')
    title2 = html.xpath('//ul/li[@class="res-book-item"]/div[@class="book-mid-info"]/h4/a/text()')
    if len(title1)==0:
        title = title2
    else:
        title = title1
    # for j in range(len(title2)):
    #     title = title1+title2
    text = html.xpath('//ul/li[@class="res-book-item"]/div[@class="book-mid-info"]/p[@class="intro"]/text()')
    href = html.xpath('//ul/li[@class="res-book-item"]/div[@class="book-img-box"]/a/@href')
    if(len(href_mu)!=0):
        href_mu.clear()     # 清空
    for i in href:
        href_mu.append('https:'+i+'#Catalog')

    src = html.xpath('//ul/li[@class="res-book-item"]/div[@class="book-img-box"]/a/img/@src')
    p1 = html.xpath('//ul/li[@class="res-book-item"]/div[@class="book-right-info"]/div[@class="total"]/p[1]/span/text()')
    p2 = html.xpath('//ul/li[@class="res-book-item"]/div[@class="book-right-info"]/div[@class="total"]/p[2]/span/text()')
    p3 = html.xpath('//ul/li[@class="res-book-item"]/div[@class="book-right-info"]/div[@class="total"]/p[3]/span/text()')
    #print(title1)
    #print(title2)
    # print(title)
    # print(text)
    # print(href)
    # print(src)
    # print(p1)
    # print(p2)
    # print(p3)
    for i in range(len(title)):
        xiaoshuo1 = {'title':title[i],'text':text[i],'src':src[i],'p1':p1[i],'p2':p2[i],'p3':p3[i],'id':i}
        xiaosuo.append(xiaoshuo1)
    return render(request,'xiaoshuo/xiao_html.html',{'xiaosuo':xiaosuo})

def xiaoshuoMu(request,id):
    mep = []
    # print(href_mu)
    # print(id)
    i = int(id)+1
    r1 = href_mu[i]
    #print(r1)
    text = requests.get(r1).text
    html = etree.HTML(text)
    href = html.xpath('//div[@class="volume"]/ul/li/a/@href')
    title = html.xpath('//div[@class="volume"]/ul/li/a/text()')
    #print(href)
    #print(title)
    for i in range(len(title)):
        mep.append({'title':title[i],'href':href[i]})

    #print(mep)
    return render(request,'xiaoshuo/xiao_mu.html',{'mep':mep})
