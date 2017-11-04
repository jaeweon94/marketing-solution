from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import requests
import csv
import os
from bs4 import BeautifulSoup
from time import sleep
import sys


form_class = uic.loadUiType("main_window.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton1.clicked.connect(self.btn1_clicked)
        self.pushButton2.clicked.connect(QCoreApplication.instance().quit)    #self.btn2_clicked)
        self.lineEdit.returnPressed.connect(self.lineEditChanged)

        #self.statusBar = QStatusBar(self)
        #self.setStatusBar(self.statusBar)
        self.radio1.setChecked(True)
        #self.radio1.clicked.connect(self.radioButtonClicked)
        #self.radio2.clicked.connect(self.radioButtonClicked)

        #self.timer = QTimer(self)
        #self.timer.start(1000) # a second
        #self.timer.timeout.connect(self.timeout) # pratice event per a second




    def btn1_clicked(self):

        if not os.path.isdir('../cafe_email'):
            os.mkdir('../cafe_email')

        cafe_name = self.lineEdit.text()  ## lineEdit의  text를 읽는다.
        url = "http://cafe.naver.com/" + cafe_name
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html,'lxml')

        cafe_menu_list = soup.select('.cafe-menu-list li a')

        menu_url = []
        all_email = []
        for each_list in cafe_menu_list:
            url_post_part = each_list['href']
            list_url = url + url_post_part
            menu_url.append(list_url)


        item = self.listWidget.item(0)
        item.setText("{} 분석 진행 중...".format(url))
        QApplication.processEvents()

        for i in range(0, len(menu_url)):   #len(menu_url)):
            sleep(2)
            item = self.listWidget.item(3)
            item.setText("{a}개 항목 중 {b}번째 진행 중...".format(a=len(menu_url),b=i+1))
            QApplication.processEvents()

            item = self.listWidget.item(6)
            item.setText("{b}/{a}".format(a=len(menu_url),b=i+1))
            QApplication.processEvents()


            for j in range(1,1000):  # 1000
                detail_url = menu_url[i] + '&userDisplay=50&search.page={}'.format(j)
                response = requests.get(detail_url)
                html = response.text

                soup2 = BeautifulSoup(html, 'lxml')
                a = soup2.select('.wordbreak')

                pre_len = len(all_email) #중간에 끊기 위함// 이전 리스트 수
                ### 한 페이지의 이메일 긁어오기 ###
                for b in a:
                    c = b['id']
                    d = str(c).split('_')

                    if self.radio2.isChecked():
                        email = d[1] ## 쪽지용은 네이버닷컴 추가 X
                    else:
                        email = d[1]+ '@naver.com'

                    all_email.append(email)
                    pure_email = list(set(all_email))

                    item = self.listWidget.item(4)
                    item.setText("총 추출된 이메일 수 {}개".format(len(all_email)))
                    QApplication.processEvents()

                    item = self.listWidget.item(9)
                    item.setText("중복 이메일 제거 후 {}개 저장 완료".format(len(pure_email)))
                    QApplication.processEvents()

                    ### make a csv file named cafe name ###
                    with open("../cafe_email/cafe_{}.csv".format(cafe_name), "w", newline='', encoding='euc-kr') as f:
                        writer = csv.writer(f)
                        for email in pure_email:
                            writer.writerow([email])

                if(len(all_email) == pre_len): ## 이후 == 이전 같으면 종료
                    break
        ## when we click button, all we have to do is send to line Edit's content. so, we don't need to line edit f


        item = self.listWidget.item(0)
        item.setText("{} 분석 완료".format(url))
        QApplication.processEvents()

        item = self.listWidget.item(3)
        item.setText("이메일 추출이 완료되었습니다.")
        QApplication.processEvents()



    def lineEditChanged(self):
        self.textEdit.setText(self.lineEdit.text())
        #self.statusBar.showMessage(self.lineEdit.text())
        #self.label_4.setText(self.lineEdit.text())

    #def radioButtonClicked(self):
    #    msg = ""



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()