'''
Copyright (c) 2019.11.23 陈良辉 All rights reserved
本爬虫程序能实现的功能:
1.爬取苹果官网中国店的网页源码，并且解析
2.绘制中国各城市苹果店个数的条形图
3.保存中国所有苹果店的店面图
4.支持城市-具体地址、号码及图片的显示
'''
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import os
import matplotlib.image as mpimg
#get_html(url)获取网址源码，并且解析
def get_html(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text,"lxml")
    return soup
#get_adress(html)将城市为key，地区和网址存为value
def get_adress(html):
    adr = {}
    for country in html.find('div',id = 'cnstores').find_all(attrs={'class':'toggle-section'}):
        value = []
        for city in country.find('h3'):
            key = city
        for adress in country.find_all('a'):
            a = []
            a.append(adress.string)
            a.append(adress.get('href'))
            value.append(a)
        adr[key] = value
    return adr
#get_chart(data)将获取的数据绘制成条形图
def get_chart(data):
    data1 = []
    data2 = []
    for k,v in data.items():
        data1.append(k)
        data2.append(len(v))
    plt.rcParams['font.sans-serif']=['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.bar(data1,data2,color = 'g',align = 'center')
    plt.title('苹果官方店中国各城市个数统计图')
    plt.ylabel('个数（单位：个)')
    plt.xlabel('城市')
    plt.show()
#爬取具体页面的地址信息   
def get_detail(url):
    soup = get_html(url) 
    print('具体地址及电话:')
    for adress in soup.find('div',attrs = {'class':'column large-12 medium-6 small-12 address-store-details'}).find_all(attrs={'class':'hcard-address'}):
        print(adress.string)
#选择查询功能
def get_choice(data):
    city = input('请输入一个上方统计图中存在的城市名:')
    dict = {}
    for area in data[city]:
        dict[area[0]] = area[1]
        print(area[0])
    choice = input('请从上方选择一个地区:')
    show(choice)
    get_detail(dict[choice])
#图片显示          
def show(choice):
    pic = mpimg.imread('D:\\apple\\'+choice+'.jpg')
    plt.imshow(pic)
    plt.axis('off')
#下载图片   
def get_pic(data):
    os.makedirs('D:\\apple')
    for k,v in data.items():
        for area in data[k]:
            url = area[1] + 'images/hero_thumb.jpg'
            name = area[0]
            r = requests.get(url, stream=True)
            open('D:\\apple\\'+name+'.jpg', 'wb').write(r.content)
            del r
    print('所有图片下载完成，保存在D盘的apple文件内')
                
def main():
    url = 'https://www.apple.com.cn/cn/retail/storelist/'
    html = get_html(url)
    data = get_adress(html)
    get_chart(data)
    get_pic(data)
    get_choice(data)
    
if __name__ == '__main__':
    main()