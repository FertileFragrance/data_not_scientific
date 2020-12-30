import datetime

import pymongo
import requests

# import pymongo

jsonURL = 'https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2510&etime={}&stime={}&ctime={}&date={}2&k=&num=50&page={}'
myclient = pymongo.MongoClient(host="124.70.84.12", port=27017)
mydb = myclient["dataScience"]  # 创建数据库
mycol = mydb["stage1"]  # 创建一个集合
mycol2 = mydb["stage2"]
mycol3 = mydb["stage3"]
mycol4 = mydb["stage4"]


def generateUrl(date, page):
    # print(datetime.timestamp(date))
    stamp = int(date.timestamp())
    return jsonURL.format(stamp, stamp + 86400, stamp + 86400, date.strftime('%Y-%m-%d'), page)


def isMatch(title):
    if (title.find('肺炎') != -1 or title.find('新冠') != -1 or title.find('新型冠状病毒') != -1 or title.find('疫苗') != -1
        or title.find('发热') != -1 or title.find('疫情') != -1 or title.find('封城') != -1 or title.find('隔离') != -1
        or title.find('患者') != -1 or title.find('COVID-19') != -1 or title.find('防疫') != -1 or title.find(
                '复工') != -1 or title.find('钟南山') != -1 or title.find('李兰娟') != -1 or title.find('抗疫') != -1) \
            or title.find('确诊') != -1 or title.find('新增') != -1 or title.find('防控') != -1:
        return True
    return False


def getUrl(startDate, endDate):
    targetDate = startDate
    # days=0;
    while (targetDate <= endDate):
        newsNum = 0
        validNews = 0
        target = targetDate.strftime('%Y-%m-%d')

        # days=days+1
        fileName = './' + r"request" + target + r'URLList.txt'
        with open(fileName, mode='w', encoding='utf-8') as f:
            for i in range(1, 100):
                trueURL = generateUrl(targetDate, i)
                try:
                    r = requests.get(trueURL)
                    r.raise_for_status()
                    r.encoding = r.apparent_encoding
                    if (not r.json()['result']['data']):
                        break
                    list = r.json()['result']['data']
                    newsNum = newsNum + len(list)
                    for i in list:
                        title = i["title"]
                        if (not isMatch(title)):
                            continue
                        validNews = validNews + 1
                        f.write(i["url"] + " " + i["title"] + '\n')
                except:
                    print("爬取失败")
            f.write(str(validNews) + '(' + str(newsNum) + ')')
            print(target + "成功")
        offset = datetime.timedelta(days=1)
        targetDate = targetDate + offset


import requests
from bs4 import BeautifulSoup
from datetime import datetime
import datetime


def getHTMLText(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


def getNewsDetail(newsurl, stage):  # 新闻具体内容
    results = []
    res = getHTMLText(newsurl)
    soup = BeautifulSoup(res, 'html.parser')
    if (soup.select(".main-title") != ''):
        # results.append(soup.select(".main-title")[0].text) 标题
        title = soup.select(".main-title")[0].text
    source = soup.select(".source")[0].text  # 新闻来源
    timesource = soup.select(".date")[0].text  # 日期
    if len(timesource) == 17:
        time = str((datetime.datetime.strptime(timesource, '%Y年%m月%d日 %H:%M')))
    else:
        time = 'null'
    content = ''.join([p.text.strip() for p in soup.select("#article p")[:-1]])  # 具体内容
    info = {
        'title': title,
        'source': source,
        'time': time,
        'content': content,
    }
    stage.insert_one(info)
    print("已生成数据" + time)
    # return results


def writeIntoDatabase(startTime, endTime, stage):
    times = startTime
    num = 1
    while times != endTime:
        file_name = './' + r"request" + times.__str__() + r'URLList.txt'
        file = open(file_name, encoding='utf-8')
        lines = file.readlines()
        file.close()

        result = []
        lens = len(lines) - 1  # 一天的新闻数量

        if lens != 0:
            for i in range(lens):
                mid = lines[i].split(' ')
                result.append(mid[0])  # 每条新闻的链接

            for j in range(len(result)):
                url = result[j]
                getNewsDetail(url, stage)

        delta = datetime.timedelta(days=1)
        times = times + delta

    return


def main():
    date1 = datetime.date(2019, 12, 8)
    date2 = datetime.date(2020, 1, 22)
    date3 = datetime.date(2020, 2, 7)
    date4 = datetime.date(2020, 3, 10)
    date5 = datetime.date(2020, 6, 10)
    # getUrl(date1,date5) 只需一次
    # # 阶段一
    #
    # writeIntoDatabase( date1, date2,mycol)
    # # # 阶段二
    # writeIntoDatabase( date2, date3,mycol2)
    # 阶段三
    # writeIntoDatabase(date3, date4, mycol3)
    # # 阶段四
    writeIntoDatabase(date4, date5, mycol4)
    return


if __name__ == "__main__":
    main()
