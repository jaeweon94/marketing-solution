from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import requests
import csv
import os
from bs4 import BeautifulSoup
import time
import sys


form_class = uic.loadUiType("main_window.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()

        self.cafe_name = ''

        self.setupUi(self)
        self.pushButton0.clicked.connect(self.btn0_clicked)
        self.pushButton1.clicked.connect(self.btn1_clicked)
        self.pushButton2.clicked.connect(self.btn2_clicked)    #self.btn2_clicked)
        self.radio1.setChecked(True)
        #self.statusBar = QStatusBar(self)
        #self.setStatusBar(self.statusBar)

        #self.radio1.clicked.connect(self.radioButtonClicked)
        #self.radio2.clicked.connect(self.radioButtonClicked)

        #self.timer = QTimer(self)
        #self.timer.start(1000) # a second
        #self.timer.timeout.connect(self.timeout) # pratice event per a second


    def btn0_clicked(self):
        for i in range(self.listWidget2.count()):  #검색버튼 누를 때 초기화시키기
           item = self.listWidget2.item(0)
           self.listWidget2.takeItem(self.listWidget2.row(item))

        for i in range(self.listWidget.count()):
            self.listWidget.item(i).setText('')


        self.cafe_name = self.lineEdit.text()  ## lineEdit의  text를 읽는다.
        url = "http://cafe.naver.com/" + self.cafe_name
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html,'lxml')

        cafe_menu_list = soup.select('ul.cafe-menu-list a')
        # 63개


        self.listWidget2.addItem("(All)카페 모든 활성유저")
        for i in range(1,len(cafe_menu_list)):
            self.listWidget2.addItem(cafe_menu_list[i].get_text())
        QApplication.processEvents()



    def btn1_clicked(self):

        list_number = self.listWidget2.currentRow()

        if list_number == 0:
            self.ccc(0,self.listWidget2.count())
        else:
            self.ccc(list_number, list_number+1)


    def btn2_clicked(self):
        sys.exit() # 작업 종료


    def ccc(self, number1, number2):
        keyword = self.cafe_name
        url = "http://cafe.naver.com/" + keyword
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html,'lxml')

        cafe_menu_list = soup.select('.cafe-menu-list li a')

        menu_url = []
        pure_email = []
        all_email = []
        for each_list in cafe_menu_list:
            url_post_part = each_list['href']
            list_url = url + url_post_part
            menu_url.append(list_url)


        item = self.listWidget.item(0)
        item.setText("{} 카페 활성유저 파악 중...".format(keyword))
        QApplication.processEvents()

        time.sleep(2)

        item = self.listWidget.item(0)
        item.setText("{} 카페 활성유저 파악 완료/스텝 제거/수집 시작".format(keyword))
        QApplication.processEvents()


        for i in range(number1, number2):   #len(menu_url))= 60개, 1~59까지 59개
            if i ==0:
                continue

            item = self.listWidget.item(2)
            item.setText("{a}개 항목 중 {b}번째 진행 중...".format(a=len(menu_url)-1,b=i))
            QApplication.processEvents()

            item = self.listWidget.item(4)
            item.setText("{b}/{a}".format(a=len(menu_url)-1,b=i))
            QApplication.processEvents()

            last_page = self.lineEdit2.text()


            check_email_1 = []
            try:
                for j in (a for a in range(2, int(last_page)+1)): # generator
                    try:
                        detail_url = menu_url[i] + '&userDisplay=50&search.page={}'.format(j)
                        response = requests.get(detail_url)
                        html = response.text

                        soup2 = BeautifulSoup(html, 'lxml')
                        a = soup2.select('.wordbreak')

                        check_email_2 = []
                        apple = [] #중간에 끊기 위함// 이전 리스트 수
                        ### 한 페이지의 이메일 긁어오기 ###
                        for b in a:
                            c = b['id']
                            d = str(c).split('_')

                            if self.radio2.isChecked():
                                email = d[1] ## 쪽지용은 네이버닷컴 추가 X
                            else:
                                email = d[1]+ '@naver.com'


                            if j <= 5:
                                check_email_1.append(email)
                            if j > 5:
                                check_email_2.append(email)


                            all_email.append(email)
                            pure_email = list(set(all_email))
                            apple.append(email)

                            item = self.listWidget.item(3)
                            item.setText("총 수집된 이메일 수 {}개".format(len(all_email)))
                            QApplication.processEvents()

                            item = self.listWidget.item(6)
                            item.setText("중복 이메일 제거 후 {}개 저장 완료".format(len(pure_email)))
                            QApplication.processEvents()

                            ### make a csv file named cafe name ###
                        if self.radio2.isChecked():
                            with open("id/cafe_{}_{}.csv".format(keyword, number1), "w", newline='', encoding='euc-kr') as f:
                                writer = csv.writer(f)
                                for email in pure_email:
                                    writer.writerow([email])

                        else:
                            with open("email/cafe_{}_{}.csv".format(keyword, number1), "w", newline='', encoding='euc-kr') as f:
                                writer = csv.writer(f)
                                for email in pure_email:
                                    writer.writerow([email])


                        pure_check_1 = list(set(check_email_1))
                        pure_check_2 = list(set(check_email_2))
                        if len(pure_check_1) == len(pure_check_2):
                            break

                        if len(apple) == 0: ## 이후 == 이전 같으면 종료
                            break
                    except:
                        continue
            except ValueError:
                QMessageBox.about(self, 'Message', '숫자를 입력해주세요.')
                break
        ## when we click button, all we have to do is send to line Edit's content. so, we don't need to line edit f


        item = self.listWidget.item(0)
        item.setText("{} 분석 완료".format(url))
        QApplication.processEvents()

        item = self.listWidget.item(3)
        item.setText("이메일 수집이 모두 완료되었습니다.")
        QApplication.processEvents()



if __name__ == "__main__":

    if not os.path.isdir('email'):
        os.mkdir('email')

    if not os.path.isdir('id'):
        os.mkdir('id')

    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()