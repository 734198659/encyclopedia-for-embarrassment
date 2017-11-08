# coding:utf-8
import requests
from lxml import etree
import json
import jsonpath


class QiushiBaike(object):
    count = 1

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
        }
        self.sourceUrl = 'https://www.qiushibaike.com/8hr/page/'

    # 返回糗事百科首页的所有url连接，返回一个 字典
    def __getAllInnerPageUrl(self):
        # 获取糗事百科首页
        formdata = '//div[contains(@class, "article block")]//a[@class="contentHerf"]/@href'
        print(self.sourceUrl + str(QiushiBaike.count) + '/')
        return self.__info(self.__travesePage(self.sourceUrl + str(QiushiBaike.count) + '/'), formdata=formdata)

    # 通过xpath规则获取页面相关信息,返回一个列表
    def __info(self, html, **kwargs):
        tree = etree.HTML(html)
        if kwargs is not None:
            tmpDict = {}
            for key, value in kwargs.items():
                result = tree.xpath(value)
                tmpDict[key] = result
            return tmpDict

    def __searchComplicate(self, dict):
        for key, value in dict.items():
            if value != []:
                dict[key] = value[0].text
            else:
                dict[key] = 0

        return dict

    # 获取每个页面中想要获取的发帖人， 被赞数。。。。
    def __innerPageInfo(self, url):
        html = self.__travesePage(url)
        formData = {
            'username': '//div[@class="author clearfix"]/span/h2[text()]|//div[@class="author clearfix"]/a/h2[text()]',
            'content': '//div[@class="content"][text()]',
            'dianzan': '//div[@id="content"]//div[@class="stats"]//i[@class="number"][text()]',
            'pinglunnumber': '//div[@id="content"]//span[@class="stats-comments"]/i[@class="number"][text()]',
        }
        resultDict = self.__searchComplicate(self.__info(html, **formData))
        # print(resultDict)
        return resultDict

    def __writeInfoByJson(self, url):
        items = self.__innerPageInfo(url)
        with open('./json/qiushi.json', 'a') as f:
            f.write(json.dumps(items, ensure_ascii=False).encode('UTF-8'))

    # 返回一个页面的内容
    def __travesePage(self, url):
        return requests.get(url, headers=self.headers).text

    # 类内部调用
    def main(self):
        while True:
            switch = raw_input("是否爬取？True|False")
            if str(switch).lower() == 'true':
                innerPageUrlDict = self.__getAllInnerPageUrl()
                prefix = 'https://www.qiushibaike.com'
                for value in innerPageUrlDict.values():
                    for item in value:
                        print prefix + item
                        self.__writeInfoByJson(prefix + item)

                QiushiBaike.count += 1


if __name__ == '__main__':
    qiushibaike = QiushiBaike()
    qiushibaike.main()
