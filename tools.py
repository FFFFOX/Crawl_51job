from lxml import etree
from urllib import request
import re
import numpy as np
import matplotlib.pyplot as plt
from urllib import parse
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']

def get_html(url):
    """
    通过url获取一个页面的数据
    :param url: 访问的网页
    :return: 返回值就是该网页html文件的字符串
    """

    req = request.Request(url)
    res = request.urlopen(req)
    return  res.read()

def get_X_Y(keyin, start_pagein, end_pagein):
    '''
    实现一个网页中带有子网页数据爬虫
    :param url:
    :return:
    '''

    plt.style.use("seaborn-dark")

    key = keyin
    kw = parse.urlencode({"kw": key})
    keyword = kw[3:]
    start_page = int(start_pagein)
    end_page = int(end_pagein)
    moneyY = []
    fuliX = []
    for page in range(start_page, end_page + 1):
        url = "https://search.51job.com/list/020000,000000,0000,00,9,99,{},2,{}.htm" \
              "l?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&" \
              "jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_" \
              "field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=".format(keyword,
                                                                                                               page)
        html_str = get_html(url)
        html = etree.HTML(html_str)

        # 将html文档结构，转化成元素树模式
        # 转化成元素树，为了使用xpath语法
        eleTree = etree.ElementTree(html)

        # 使用 xpath
        # 使用xpath解析  结果会保存在列表中
        els = eleTree.xpath("//div[@id='resultList']/div[@class='el']")

        # 遍历els  来解析出我们想要的数据
        moneyList = [0,0]
        for tmp in els:
            # 将子元素树
            el = etree.ElementTree(tmp)
            # 子元素树 根节点就是 div[@class='el']
            # 职位   获取 a 下面的title 的值  返回值 是一个列表
            position = el.xpath('/div/p/span/a/@title')
            position = position[0] if position else None
            # if position:
            #     position = position[0]
            # else:
            #     None

            # 职位的子网页
            child_page = el.xpath('/div/p/span/a/@href')
            child_page = child_page[0] if child_page else None

            # 薪资待遇
            money = el.xpath('/div/span[@class="t4"]/text()')
            money = money[0] if money else None

            # 获取子网页的信息
            child_page_str = get_html(child_page)
            child_page_html = etree.HTML(child_page_str)
            child_page_eleTree = etree.ElementTree(child_page_html)

            fuli_str = '//div[@class="jtag"]/div[@class="t1"]/span/text()'


            # 使用_把字符串连接到一起

            fuli = child_page_eleTree.xpath(fuli_str)  # 把所有满足xpath条件的数据 保存到fuli  列表
            fuli = "_".join(fuli)
            print(money,fuli)
            moneyString = str(money)

            if moneyString == "None":
                moneyY.append(None)
            else:
                if "千" in moneyString:
                    moneyList = re.findall(r"\d+\.?\d*", moneyString)

                    print("jieguo")
                    print(moneyList[0])
                    if len(moneyList) == 1 :
                        moneyList[0] = (eval(moneyList[0])) / 10
                    else:
                        moneyList[0] = (eval(moneyList[0])) / 10
                        moneyList[1] = (eval(moneyList[1])) / 10
                    moneyY.append(np.mean(moneyList))
                elif "天" in moneyString:
                    moneyList = re.findall(r"\d+\.?\d*", moneyString)
                    if len(moneyList) == 1 :
                        moneyList[0] = eval(moneyList[0]) * 30 / 10000
                    else:
                        moneyList[0] = eval(moneyList[0]) * 30 / 10000
                        moneyList[1] = eval(moneyList[1]) * 30 / 10000
                    moneyY.append(np.mean(moneyList))
                elif "年" in moneyString:
                    moneyList = re.findall(r"\d+\.?\d*", moneyString)
                    if len(moneyList) == 1 :
                        moneyList[0] = eval(moneyList[0]) / 12
                    else:
                        moneyList[0] = eval(moneyList[0]) / 12
                        moneyList[1] = eval(moneyList[1]) / 12
                    moneyY.append(np.mean(moneyList))
                else:
                    moneyList = re.findall(r"\d+\.?\d*", moneyString)
                    if len(moneyList) == 1 :
                        moneyList[0] = eval(moneyList[0])
                    else:
                        moneyList[0] = eval(moneyList[0])
                        moneyList[1] = eval(moneyList[1])
                    moneyY.append(np.mean(moneyList))

            fuliX.append(len(fuli.split("_")))

    plt.grid(linestyle="--", alpha=0.5)
    print("X轴")
    print(fuliX)
    print("Y轴")
    print(moneyY)
    plt.xlabel('Welfare')
    plt.ylabel('Money')
    plt.scatter(fuliX, moneyY, s=50, c='b', alpha=1, marker="1")
    plt.show()



def get_Histogram(keyin, start_pagein, end_pagein):

    plt.style.use("seaborn-dark")

    key = keyin
    kw = parse.urlencode({"kw": key})
    keyword = kw[3:]
    start_page = int(start_pagein)
    end_page = int(end_pagein)
    moneyY = []
    for page in range(start_page, end_page + 1):
        url = "https://search.51job.com/list/020000,000000,0000,00,9,99,{},2,{}.htm" \
              "l?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&" \
              "jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_" \
              "field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=".format(keyword,
                                                                                                               page)
        html_str = get_html(url)
        html = etree.HTML(html_str)
        eleTree = etree.ElementTree(html)
        els = eleTree.xpath("//div[@id='resultList']/div[@class='el']")

        for tmp in els:
            el = etree.ElementTree(tmp)

            position = el.xpath('/div/p/span/a/@title')
            position = position[0] if position else None

            child_page = el.xpath('/div/p/span/a/@href')
            child_page = child_page[0] if child_page else None

            money = el.xpath('/div/span[@class="t4"]/text()')
            money = money[0] if money else None

            moneyString = str(money)
            if moneyString == "None":
                moneyY.append("0")
            else:
                if "千" in moneyString:
                    moneyList = re.findall(r"\d+\.?\d*", moneyString)

                    print("jieguo")
                    print(moneyList[0])
                    if len(moneyList) == 1:
                        moneyList[0] = (eval(moneyList[0])) / 10
                    else:
                        moneyList[0] = (eval(moneyList[0])) / 10
                        moneyList[1] = (eval(moneyList[1])) / 10
                    moneyY.append(np.mean(moneyList))
                elif "天" in moneyString:
                    moneyList = re.findall(r"\d+\.?\d*", moneyString)
                    if len(moneyList) == 1:
                        moneyList[0] = eval(moneyList[0]) * 30 / 10000
                    else:
                        moneyList[0] = eval(moneyList[0]) * 30 / 10000
                        moneyList[1] = eval(moneyList[1]) * 30 / 10000
                    moneyY.append(np.mean(moneyList))
                elif "年" in moneyString:
                    moneyList = re.findall(r"\d+\.?\d*", moneyString)
                    if len(moneyList) == 1:
                        moneyList[0] = eval(moneyList[0]) / 12
                    else:
                        moneyList[0] = eval(moneyList[0]) / 12
                        moneyList[1] = eval(moneyList[1]) / 12
                    moneyY.append(np.mean(moneyList))
                else:
                    moneyList = re.findall(r"\d+\.?\d*", moneyString)
                    if len(moneyList) == 1:
                        moneyList[0] = eval(moneyList[0])
                    else:
                        moneyList[0] = eval(moneyList[0])
                        moneyList[1] = eval(moneyList[1])
                    moneyY.append(np.mean(moneyList))
    print(moneyY)
    moneyY = np.array(moneyY)
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
    print(moneyY)
    # bins 指定区间范围  默认的区间 10个
    bins = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5]
    # rwidth  设置宽度

    plt.hist(moneyY, bins=bins, color="b", alpha=0.5, rwidth=0.5)
    plt.xlabel('Money')
    plt.ylabel('Numbers')
    plt.show()

def get_bar(keyin, start_pagein, end_pagein):

    plt.style.use("seaborn-dark")
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']

    key = keyin
    kw = parse.urlencode({"kw": key})
    keyword = kw[3:]
    start_page = int(start_pagein)
    end_page = int(end_pagein)

    sumDict = {'黄浦区': 0, '徐汇区': 0, '长宁区': 0, '静安区': 0, '普陀区': 0, '虹口区': 0, '杨浦区': 0, '闵行区': 0, '宝山区': 0, '嘉定区': 0, '金山区': 0,
     '松江区': 0, '青浦区': 0, '奉贤区': 0, '崇明区': 0, '浦东新区': 0}
    for page in range(start_page, end_page + 1):
        url = "https://search.51job.com/list/020000,000000,0000,00,9,99,{},2,{}.htm" \
              "l?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&" \
              "jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_" \
              "field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=".format(keyword,
                                                                                                               page)
        html_str = get_html(url)
        html = etree.HTML(html_str)
        eleTree = etree.ElementTree(html)
        els = eleTree.xpath("//div[@id='resultList']/div[@class='el']")

        for tmp in els:
            el = etree.ElementTree(tmp)

            position = el.xpath('/div/p/span/a/@title')
            position = position[0] if position else None

            child_page = el.xpath('/div/p/span/a/@href')
            child_page = child_page[0] if child_page else None

            # 办公地点
            addr = el.xpath('/div/span[@class="t3"]/text()')
            addr = addr[0] if addr else None

            addrStr = str(addr)
            for i in sumDict:
                if i in addrStr:
                    sumDict[i] += 1

    y = list(sumDict.values())
    x = ['黄浦区', '徐汇区', '长宁区', '静安区', '普陀区', '虹口区', '杨浦区', '闵行区', '宝山区', '嘉定区', '金山区', '松江区', '青浦区', '奉贤区', '崇明区',
         '浦东新区']
    plt.figure(figsize=(10, 10))
    plt.bar(x, y, width=0.5, color=['b', 'r', 'g'])
    plt.show()


def get_Pie(keyin, start_pagein, end_pagein):
    key = keyin
    kw = parse.urlencode({"kw": key})
    keyword = kw[3:]
    start_page = int(start_pagein)
    end_page = int(end_pagein)
    moneyY = []
    for page in range(start_page, end_page + 1):
        url = "https://search.51job.com/list/020000,000000,0000,00,9,99,{},2,{}.htm" \
              "l?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&" \
              "jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_" \
              "field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=".format(keyword,
                                                                                                               page)
        html_str = get_html(url)
        html = etree.HTML(html_str)
        eleTree = etree.ElementTree(html)
        els = eleTree.xpath("//div[@id='resultList']/div[@class='el']")
        a = 0
        b = 0
        c = 0
        d = 0
        e = 0
        f = 0
        for tmp in els:
            el = etree.ElementTree(tmp)

            position = el.xpath('/div/p/span/a/@title')
            position = position[0] if position else None

            child_page = el.xpath('/div/p/span/a/@href')
            child_page = child_page[0] if child_page else None

            money = el.xpath('/div/span[@class="t4"]/text()')
            money = money[0] if money else None

            moneyString = str(money)
            if moneyString == "None":
                moneyY = 0
            else:
                if "千" in moneyString:
                    moneyList = re.findall(r"\d+\.?\d*", moneyString)

                    print("jieguo")
                    print(moneyList[0])
                    if len(moneyList) == 1:
                        moneyList[0] = (eval(moneyList[0])) / 10
                    else:
                        moneyList[0] = (eval(moneyList[0])) / 10
                        moneyList[1] = (eval(moneyList[1])) / 10
                    moneyY = np.mean(moneyList)
                elif "天" in moneyString:
                    moneyList = re.findall(r"\d+\.?\d*", moneyString)
                    if len(moneyList) == 1:
                        moneyList[0] = eval(moneyList[0]) * 30 / 10000
                    else:
                        moneyList[0] = eval(moneyList[0]) * 30 / 10000
                        moneyList[1] = eval(moneyList[1]) * 30 / 10000
                    moneyY = np.mean(moneyList)
                elif "年" in moneyString:
                    moneyList = re.findall(r"\d+\.?\d*", moneyString)
                    if len(moneyList) == 1:
                        moneyList[0] = eval(moneyList[0]) / 12
                    else:
                        moneyList[0] = eval(moneyList[0]) / 12
                        moneyList[1] = eval(moneyList[1]) / 12
                    moneyY = np.mean(moneyList)
                else:
                    moneyList = re.findall(r"\d+\.?\d*", moneyString)
                    if len(moneyList) == 1:
                        moneyList[0] = eval(moneyList[0])
                    else:
                        moneyList[0] = eval(moneyList[0])
                        moneyList[1] = eval(moneyList[1])
                    moneyY = np.mean(moneyList)

            if 0 <= moneyY < 0.5:
                a += 1
            elif 0.5 <= moneyY < 1:
                b += 1
            elif 1 <= moneyY < 1.5:
                c += 1
            elif 2 <= moneyY < 2.5:
                d += 1
            elif 2.5 <= moneyY < 3:
                e += 1
            elif 3 <= moneyY < 5:
                f += 1
    nums = [a,b,c,d,e,f]
    labels = ["0-0.5万", "0.5-1万", "1.5-2万", "2-2.5万", "2.5-3万", ">3万"]
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
    plt.pie(x=nums, labels=labels)
    plt.show()

