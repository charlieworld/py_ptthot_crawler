#coding=UTF-8
import requests
from bs4 import BeautifulSoup
import csv

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
siteUrl = 'https://disp.cc/b/'
url = siteUrl + 'PttHot'

# 抓取數值
def find_item(className,item):
  temp = item.find('span', class_=className)
  if (temp is None):
    return 'No Item'
  else:
    return temp.getText()

#  抓取時間
def get_date(item):
  return(item.find('span', class_='L12').get('title'))

# 抓取推文數
def get_push(item):
  temp = item.find('span', class_='L9').getText()

  if (len(temp) > 0) :
    temp = int(temp)
  else:
    temp = 0

  return temp

def get_title_and_link(item):
  temp = item.find('span', class_='listTitle')

  link = siteUrl + temp.find('a').get('href')
  title = temp.getText()

  return title,link

def get_count(item):
  temp = item.find('span', class_='R0').getText()
  temp = temp.split('/',1)[1]
  return temp

# 儲存資料至csv
def save_data(data):
  with open('get_pttHot.csv', 'w') as csvfile:
    #設定欄位名稱
    fieldnames = ['number','push','date','auther','title','link','count']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for item in data:
      #逐行寫入
      writer.writerow(item)

  print("Writing csv complete")

# #########################
# STEP 0. |主程式開始 拿取整個HTML + 找出每個貼文
# #########################
r = requests.get(url, headers=headers)
soup = BeautifulSoup(r.text, 'lxml')
posts = soup.find_all('div',class_='row2')

#拿掉最後一列 (不是我們要的)
del posts[-1]

#主資料
mainData = []

# #########################
# STEP 1. 從每一篇貼文中取出資料
# #########################

for item in posts:

  title,link = get_title_and_link(item)

  #建立結構化資料
  itemObj = {
    'number': find_item('list-num',item),
    'push': get_push(item),
    'date': get_date(item),
    'auther': find_item('L18',item),
    'title': title.encode('utf-8'),
    'link': link,
    'count': get_count(item)
  }
  print itemObj
  print '------'

  #加入到主資料中
  mainData.append(itemObj)

# #########################
# STEP 2. 資料儲存到CSV檔案
# #########################
save_data(mainData)

