import requests
import re
import os
import time

class myImageCrawler():
    '''
    百度图片爬虫程序
    '''

    def __init__(self, keyword, number, path):
        self.keyword = keyword              # 图片关键词
        self.number = number                # 需要下载的数量
        self.path = path                    # 保存路径
        self.progress = 0                   # 当前已经下载的数量


    def get_parse_url(self, pn):
        ''' 获取页号为 pn 的图片链接 '''

        # 百度图片首页 URL + 搜索关键词 + 下载页号
        url = 'https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word=%s&pn=%d' % (self.keyword, pn * 20)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                                 'AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/53.0.2785.104 '
                                 'Safari/537.36 Core/1.53.4843.400 '
                                 'QQBrowser/9.7.13021.400'}

        # 发送请求，获取响应
        response = requests.get(url, headers=headers)
        html = response.content.decode()

        # 正则表达式解析网页
        # "objURL":"http://n.sinaimg.cn/sports/transform/20170406/dHEk-fycxmks5842687.jpg"
        img_list = re.findall('"objURL":"(.*?)",', html)  # 返回一个列表

        return img_list


    def download(self):
        ''' 下载指定数目的图片 '''

        if not os.path.exists(self.path):
            os.makedirs(self.path)

        pn = 0
        while True:
            img_list = self.get_parse_url(pn)
            for img in img_list:
                try:
                    pic = requests.get(img, timeout=5)
                except:
                    # 下载失败
                    continue

                # 把图片保存到文件夹
                full_path = self.path + '/' + str(self.progress) + '.jpg'
                with open(full_path, 'wb') as f:
                    f.write(pic.content)
                # 可能的异常图片
                if os.stat(full_path).st_size < 1024:
                    os.remove(full_path)
                else:
                    self.progress += 1

                if self.progress >= self.number:
                    break

            if self.progress >= self.number:
                break
            else:
                pn += 1
