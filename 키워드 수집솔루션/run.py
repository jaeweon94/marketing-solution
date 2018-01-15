from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import requests
import csv
import os
from bs4 import BeautifulSoup
import time
import sys
import re
import json
from fake_useragent import UserAgent
import random

form_class = uic.loadUiType("main_window.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.save_id = []
        self.user_key = ''

        self.pushButton0.clicked.connect(self.btn0_clicked) #검색1
        self.pushButton0_1.clicked.connect(self.btn0_1_clicked) #검색2

        self.pushButton1.clicked.connect(self.btn1_clicked) #선택1
        self.pushButton1_1.clicked.connect(self.btn1_1_clicked) #선택2
        self.pushButton1_2.clicked.connect(self.btn1_2_clicked) #선택3


        self.pushButton2.clicked.connect(self.btn2_clicked)    #수집
        self.pushButton3.clicked.connect(self.btn3_clicked)    #수집 끝내기

        self.radio1.setChecked(True)
        #self.statusBar = QStatusBar(self)
        #self.setStatusBar(self.statusBar)

        #self.radio1.clicked.connect(self.radioButtonClicked)
        #self.radio2.clicked.connect(self.radioButtonClicked)

        #self.timer = QTimer(self)
        #self.timer.start(1000) # a second
        #self.timer.timeout.connect(self.timeout) # pratice event per a second



    def btn0_clicked(self): #검색1
        for i in range(self.listWidget2.count()):  #검색버튼 누를 때 연관1 초기화시키기
           item = self.listWidget2.item(0)
           self.listWidget2.takeItem(self.listWidget2.row(item))

        for i in range(self.listWidget3.count()):  #검색버튼 누를 때 연관2 초기화시키기
           item = self.listWidget3.item(0)
           self.listWidget3.takeItem(self.listWidget3.row(item))

        self.lineEdit2.setText('')

        #for i in range(self.listWidget.count()): #작업보드 초기화
        #    self.listWidget.item(i).setText('')


        ## 검색 ##

        page_url = 'https://www.naver.com'
        headers = {
            'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'),
            "Accept-Encoding": "gzip, deflate",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            'Referer': page_url,
        }


        user_key = self.lineEdit.text()  ## lineEdit의  text를 읽는다.
        keyword = user_key.replace(' ', '+')
        c_url = 'https://search.naver.com/search.naver?where=nexearch&ie=utf8&query={}&start=1'.format(keyword).encode('utf-8')
        response = requests.get(c_url, headers = headers)
        html = response.text
        c_soup = BeautifulSoup(html, 'lxml')

        relate = c_soup.select('dd.lst_relate li a')

        for relate_key in relate:
            self.listWidget2.addItem(relate_key.get_text())



    def btn0_1_clicked(self): #검색2
        for i in range(self.listWidget3.count()):  #검색버튼 누를 때 연관2 초기화
           item = self.listWidget3.item(0)
           self.listWidget3.takeItem(self.listWidget3.row(item))


        ## 검색 ##
        page_url = 'https://www.naver.com'
        headers = {
            'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'),
            "Accept-Encoding": "gzip, deflate",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            'Referer': page_url,
        }


        user_key = self.listWidget2.currentItem().text()  ## lineEdit의  text를 읽는다.
        keyword = user_key.replace(' ', '+')

        c_url = 'https://search.naver.com/search.naver?where=nexearch&ie=utf8&query={}&start=1'.format(keyword).encode('utf-8')
        response = requests.get(c_url, headers = headers)
        html = response.text
        c_soup = BeautifulSoup(html, 'lxml')

        relate = c_soup.select('dd.lst_relate li a')

        for relate_key in relate:
            self.listWidget3.addItem(relate_key.get_text())





    def btn1_clicked(self): #선택1
        self.lineEdit2.setText(self.lineEdit.text())


    def btn1_1_clicked(self): #선택2
        self.lineEdit2.setText(self.listWidget2.currentItem().text())


    def btn1_2_clicked(self): #선택3
        self.lineEdit2.setText(self.listWidget3.currentItem().text())




    def btn2_clicked(self): #수집
        ## 초기화 ##
        for i in range(self.listWidget.count()): #작업보드 초기화
            self.listWidget.item(i).setText('')

        self.save_id = []


        self.user_key = self.lineEdit2.text()
        keyword = self.user_key.replace(' ', '+')

        item = self.listWidget.item(0)
        item.setText('#{} 키워드 검색'.format(self.user_key))
        QApplication.processEvents()

        item = self.listWidget.item(1)
        item.setText('6개월 내 키워드 포함 블로그/카페 파악 완료')
        QApplication.processEvents()

        item = self.listWidget.item(4)
        item.setText('블로그/카페 활성유저 이메일 수집 중...')
        QApplication.processEvents()


        ## headers ##
        page_url = 'https://www.naver.com'
        headers = {
            'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'),
            "Accept-Encoding": "gzip, deflate",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            'Referer': page_url,
        }
        test_url = 'https://search.naver.com/search.naver?where=post&ie=utf8&query=test&start=1&date_option=6'
        test_response = requests.get(test_url, headers = headers)
        test_html = test_response.text
        test_soup = BeautifulSoup(test_html, 'lxml')

        if '비정상적인 검색' in str(test_soup):

            ua = UserAgent()
            ua.random

            page_url = 'https://www.naver.com'
            headers = {
                'User-Agent': str(ua.random),
                "Accept-Encoding": "gzip, deflate",
                'Referer': page_url,
            }


        ### 블로그/카페 통합 시작 ###

        for j in range(100):

            if j % 10 == 0: # 20번(네이버 10 + 카페 10) 검색마다 한 번씩
                r_url = 'https://search.naver.com/search.naver?where=post&ie=utf8&query={}&start=1&date_option=6'.format(random.randrange(100)).encode('utf-8')
                r_response = requests.get(r_url, headers = headers)



            item = self.listWidget.item(7)
            item.setText('{}/100페이지'.format(j+1))
            QApplication.processEvents()


            #time.sleep(3)

            page_number = j*10 + 1

            b_url = 'https://search.naver.com/search.naver?where=post&ie=utf8&query={}&start={}&date_option=6'.format(keyword, page_number).encode('utf-8')
            response = requests.get(b_url, headers = headers)
            html = response.text
            soup = BeautifulSoup(html, 'lxml')

            if '비정상적인 검색' in str(soup):
                QMessageBox.about(self, 'Message', '아이피가 일시적으로 차단되었습니다. 몇 시간 쉬었다 진행해보세요.')
                break


            for each_content in soup.select('div.thumb-rollover a.sp_thmb'):
                try:
                    each_url = each_content['href']
                    #print(each_url)
                    if 'blog.me' in each_url:
                        b_info_3 = each_url
                        b_info = b_info_3.split('.blog.me/')
                        blog_id = b_info[0][7:]
                        log_no = b_info[1]
                        if self.radio2.isChecked():
                            b_host_email = blog_id
                        else:
                            b_host_email = blog_id + '@naver.com'
                        self.save_id.append(b_host_email)
                    else:
                        b_info_1 = each_url
                        b_info_2 = b_info_1.split('/')
                        b_info = b_info_2[3].split('?Redirect=Log&logNo=')
                        blog_id = b_info[0]
                        log_no = b_info[1]
                        if self.radio2.isChecked():
                            b_host_email = blog_id
                        else:
                            b_host_email = blog_id + '@naver.com'
                        self.save_id.append(b_host_email)

                    #time.sleep(1)



                    b_url2 = 'https://blog.naver.com/PostView.nhn?blogId={}&logNo={}'.format(blog_id, log_no)
                    response = requests.get(b_url2)
                    html = response.text
                    b_soup = BeautifulSoup(html, 'lxml')

                    zzz = str(b_soup).split('var')

                    for i in range(len(zzz)):
                        if 'blogNo' in zzz[i]:
                            yyy = zzz[i]

                    p = re.compile('blogNo\D*\d+')
                    xxx = p.findall(yyy)
                    q = re.compile('\d+')
                    blog_no = int(q.findall(xxx[0])[0])


                    header_2 = {
                    'Referer':'https://blog.naver.com/PostList.nhn?blogId=&widgetTypeCall=true&directAccess=true'
                    }

                    res2 = requests.get('https://apis.naver.com/commentBox/cbox/web_naver_list_jsonp.json?ticket=blog&pool=cbox9&lang=ko&objectId={a}_201_{b}&groupId={a}'.format(a=blog_no, b= log_no), headers=header_2)

                    json_data = res2.text.replace("_callback(","")
                    json_data = json_data.replace(");","")

                    js = json.loads(json_data) #str -> python으로 바꾼 것. 근데 본래 python dic 타입이였으므로 가능한 것임.


                    for commentList in js['result']['commentList']:
                        try:
                            if self.radio2.isChecked():
                                b_guest_email = commentList['profileUserId']
                            else:
                                b_guest_email = commentList['profileUserId']+'@naver.com'

                            self.save_id.append(b_guest_email)

                            item = self.listWidget.item(5)
                            item.setText('수집된 이메일 수: {}개'.format(len(self.save_id)))
                            QApplication.processEvents()

                            item = self.listWidget.item(9)
                            item.setText('중복 제거 후 이메일 {}개 저장 완료'.format(len(list(set(self.save_id)))))
                            QApplication.processEvents()
                            pure_email = list(set(self.save_id))

                        except:
                            continue
                except:
                    continue

#        item = self.listWidget.item(4)
#        item.setText('카페 활성유저 이메일 수집 중...')
#        QApplication.processEvents()

        ### 카페 시작 ###

#        for k in range(100):
#            item = self.listWidget.item(7)
#            item.setText('{}/200페이지'.format(k+101))
#            QApplication.processEvents()

            #time.sleep(1.5)


            c_url = 'https://search.naver.com/search.naver?where=article&ie=utf8&query={}&start={}&date_option=6'.format(keyword, page_number).encode('utf-8')
            response = requests.get(c_url, headers = headers)
            html = response.text
            c_soup = BeautifulSoup(html, 'lxml')

            apple = [] # 각각의 url 저장
            for each_content in c_soup.select('div.thumb-rollover a.sp_thmb'):
                each_url = each_content['href']
                apple.append(each_url)


            for cafe_url in apple:
                try:
                    response = requests.get(cafe_url)
                    html = response.text
                    c_soup2 = BeautifulSoup(html, 'lxml')

                    ## club id ##
                    aaa = str(c_soup2).split('var') # var로 쪼개기
                    #scripts = soup.select('script')
                    for i in range(len(aaa)):
                        if 'ClubId' in aaa[i]: # ClubId 있는 부분 찾기
                            bbb = aaa[i]

                    p = re.compile('g_sClubId\D*\d+')
                    ccc = p.findall(bbb)
                    q = re.compile('\d+')
                    club_id = int(q.findall(ccc[0])[0])
                    ## article id ##
                    aa = cafe_url.split('/')
                    article_id = aa[-1]
                    ## host ID ##

                    #time.sleep(0.3)

                    url_host = 'http://cafe.naver.com/ArticleRead.nhn?&clubid={}&articleid={}'.format(club_id, article_id)

                    response = requests.get(url_host)
                    html = response.text
                    c_soup2 = BeautifulSoup(html, 'lxml')
                    f_host_id = c_soup2.select('div.other_view a')[0]

                    host_id = f_host_id['href'].split('memberid=')[1]
                    if self.radio2.isChecked():
                        host_email = host_id
                    else:
                        host_email = host_id + '@naver.com'
                    self.save_id.append(host_email)
                    #print('h', host_email)

                    ## guest(comment) ID ##
                    url_guest = 'http://cafe.naver.com/CommentView.nhn?search.clubid={}&search.articleid={}&search.page=1'.format(club_id, article_id)
                    response = requests.get(url_guest)
                    html = response.text

                    dict = json.loads(html)

                    for info in dict['result']['list']:
                        guest_id = info['writerid']
                        if self.radio2.isChecked():
                            guest_email = guest_id
                        else:
                            guest_email = guest_id + '@naver.com'

                        self.save_id.append(guest_email)

                        item = self.listWidget.item(5)
                        item.setText('수집된 이메일 수: {}개'.format(len(self.save_id)))
                        QApplication.processEvents()

                        item = self.listWidget.item(9)
                        item.setText('중복 제거 후 이메일 {}개 저장 완료'.format(len(list(set(self.save_id)))))
                        QApplication.processEvents()

                        pure_email = list(set(self.save_id))

                        if self.radio2.isChecked():
                            self.keyword_csv('id', pure_email)
                        else:
                            self.keyword_csv('email', pure_email)
                        #print('g', guest_email)
                except:
                    continue

        item = self.listWidget.item(4)
        item.setText('블로그/카페 활성유저 이메일 수집 완료')
        QApplication.processEvents()




    def btn3_clicked(self): #수집 끝내기

        sys.exit() # 작업 종료
        #메세지 띄우고 break 걸었음.

    def keyword_csv(self, method, email_list):
        with open('{}/key_{}.csv'.format(method,self.user_key), 'w', newline='', encoding='euc-kr') as f:
            writer = csv.writer(f)
            for each_email in email_list:
                writer.writerow([each_email])





if __name__ == "__main__":

    if not os.path.isdir('email'):
        os.mkdir('email')

    if not os.path.isdir('id'):
        os.mkdir('id')

    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()