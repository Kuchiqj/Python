from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from lxml import etree
import xlwt
import time
#创建chrome浏览器对象
# web = webdriver.Chrome(r'C:\Users\Lenovo\AppData\Local\Google\Chrome\Application\chromedriver_win32\chromedriver.exe')
# url = 'https://www.baidu.com/?tn=15007414_pg'
# web.get(url)
# # 获取当前网页源码
# resp = web.page_source
# print(resp)
#
# # selenium交互动作
# # 放大窗口
# web.maximize_window()
# # 定位搜索框
# search = web.find_element(By.XPATH,'//*[@id="kw"]')
# # 向搜索框中输入内容
# search.send_keys('西南石油大学')
# # search.send_keys(Keys.ENTER)
# baidu = web.find_element(By.XPATH,'//*[@id="su"]')
# # 点击操作
# baidu.click()
# time.sleep(2)
# print(web.page_source)
product_list = []
web = webdriver.Chrome(r'C:\Users\Lenovo\AppData\Local\Google\Chrome\Application\chromedriver_win32\chromedriver.exe')
url = 'https://www.taobao.com/?spm=a2e0b.20350158.1581860521.1.7311468aAX5a9l&pid=mm_26632258_3504122_32538762&union_lens=recoveryid%3A201_33.61.21.33_20212513_1670404099109%3Bprepvid%3A201_33.61.21.33_20212513_1670404099109&clk1=6686974a816478721862d6c89476b9ca?spm=a2e0b.20350158.1581860521.1.7311468aAX5a9l&pid=mm_26632258_3504122_32538762&union_lens=recoveryid%3A201_33.61.21.33_20212513_1670404099109%3Bprepvid%3A201_33.61.21.33_20212513_1670404099109&clk1=6686974a816478721862d6c89476b9ca'
web.get(url)
# 放大窗口
web.maximize_window()
login = web.find_element(By.XPATH,'//*[@id="J_SiteNavLogin"]/div[1]/div[1]/a[1]')
login.click()
code = web.find_element(By.XPATH,'//*[@id="login"]/div[1]/i')
code.click()
time.sleep(10)
search = web.find_element(By.XPATH,'//*[@id="q"]')
search.send_keys('手机')
search.send_keys(Keys.ENTER)
brand = web.find_element(By.XPATH,'//*[@id="J_NavCommonRowItems_0"]/a[5]/span[2]')
brand.click()
# resp = web.page_source
# # print(resp)
# time.sleep(10)
#自动下拉
for i in range(1,61):
    max_y= 5000
    y = 0
    Y = 5000
    min_Y = 0
    while y<=max_y:
        web.execute_script(f'window.scrollTo(0,{y})')
        y += 800
        time.sleep(1)
    resp = web.page_source
    time.sleep(3)
    # # # 点击下一页
    # next_page = web.find_element(By.XPATH,'')

    # 建造树结构
    parser = etree.HTMLParser(encoding='utf-8')
    tree = etree.XML(resp,parser=parser)
    # element_List = tree.xpath('//*[@id="J_Itemlist_TLink_687886522444"]')
    element_List = tree.xpath('//*[@id="mainsrp-itemlist"]/div/div/div[1]/div')
    # print(element_List)
    for element in element_List:
        title1 = element.xpath('./div[2]/div[2]/a/text()')[1].strip()
        title2 = element.xpath('./div[2]/div[2]/a/text()')
        pay_history = element.xpath('./div[2]/div[1]/div[2]/text()')
        price = element.xpath('./div[2]/div[1]/div[1]/strong/text()')
        city = element.xpath('./div[2]/div[3]/div[2]/text()')
        salesmen = element.xpath('./div[2]/div[3]/div[1]/a/span[2]/text()')
        print(title1,title2,pay_history,price,city,salesmen)
        product_list.append([title1,title2,pay_history,price,city,salesmen])
        # # 点击下一页
        # print(len(element_List))
    if i<4 or i>30 and i<34:
        next_page = web.find_element(By.XPATH, '//*[@id="mainsrp-pager"]/div/div/div/ul/li[8]/a')
    elif i == 4 or i == 34:
        next_page = web.find_element(By.XPATH, '//*[@id="mainsrp-pager"]/div/div/div/ul/li[9]/a')
    elif i == 5 or i == 35:
        next_page = web.find_element(By.XPATH,'//*[@id="mainsrp-pager"]/div/div/div/ul/li[10]/a')
    elif i>=6 or i>=36:
        next_page = web.find_element(By.XPATH, '//*[@id="mainsrp-pager"]/div/div/div/ul/li[11]/a')
    next_page.click()
    s = len(element_List)
    print(f'到此为第{i}页的数据，共{s}条')
    if i == 30:
        while Y >= min_Y:
            web.execute_script(f'window.scrollTo(5000,{Y})')
            Y -= 1000
            time.sleep(1)
        brand1 = web.find_element(By.XPATH, '//*[@id="mainsrp-related"]/div/dl/dd/a[10]')
        brand1.click()
        # print('准备开始下一品牌的抓取')
wb = xlwt.Workbook()

sheet = wb.add_sheet('DATA')

titles = ['title1','title2','pay_history','price','city','salesmen']
for index,title in enumerate(titles):
    sheet.write(0,index,title)
for a,item in enumerate(product_list):
    for b,value in enumerate(item):
        sheet.write(a+1,b,value)
wb.save('product_data.xls')



