from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import requests
import csv
import os
from bs4 import BeautifulSoup
import time
import sys
import openpyxl


form_class = uic.loadUiType("main_window.ui")[0]

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.all_email = []
        self.count = 0
        self.setupUi(self)
        self.pushButton0.clicked.connect(self.btn0_clicked)
        self.pushButton1.clicked.connect(self.btn1_clicked)
        self.pushButton2.clicked.connect(self.btn2_clicked)
        self.pushButton3.clicked.connect(self.btn3_clicked)
        self.radio1.setChecked(True)


# What I have to do is first, read txt file and xlsx file
# second, save email in all file at once
# how to save as txt file

# button을 누를 때마다 새로운 instance가 생기는 것이 아님!

    def btn0_clicked(self):
        fname = QFileDialog.getOpenFileName(self)
        try:
            if '.xlsx' in os.path.basename(fname[0]):
                each_list = []
                wb = openpyxl.load_workbook(fname[0])
                ws = wb.active

                for r in ws.rows:
                    each_list.append(r[0].value)
                    self.all_email.append(r[0].value)

                wb.close()
            else:
                with open(fname[0],'r') as f:
                    each_list = []
                    reader = csv.reader(f)
                    for row in reader:
                        each_list += row
                        self.all_email += row

            count_list = len(each_list)
            all_count_list = len(self.all_email) #각각의 개수
            file_name = os.path.basename(fname[0])
            self.count += 1

            self.listWidget.addItem('#{} {} / {}개'.format(self.count, file_name, count_list))
            self.listWidget2.item(1).setText('총 {}개 파일 / 누적 이메일 개수: {}개'.format(self.count, all_count_list))
        except FileNotFoundError:
            return
        except:
            QMessageBox.about(self, "Error", "올바른 파일이 아닙니다.")


    def btn1_clicked(self):

        if not os.path.isdir('email'):
            os.mkdir('email')

        if self.lineEdit.text() == '':
            file_name = 'no_name'
        else:
            file_name = self.lineEdit.text()

        pure_email = list(set(self.all_email))


        if self.radio2.isChecked():
            with open('email/{}.txt'.format(file_name), 'w', newline='', encoding = 'euc-kr') as f:
                writer = csv.writer(f)
                for a in pure_email:
                    writer.writerow([a])
        else:
            with open('email/{}.csv'.format(file_name), 'w', newline='', encoding = 'euc-kr') as f:
                writer = csv.writer(f)
                for a in pure_email:
                    writer.writerow([a])


        self.listWidget2.item(0).setText('[중복 제거 및 저장 완료]')
        QApplication.processEvents()

        self.listWidget2.item(1).setText('기존 이메일 개수 {}개'.format(len(self.all_email)))
        QApplication.processEvents()

        self.listWidget2.item(2).setText('중복 제거 후 이메일 개수 {}개'.format(len(pure_email)))
        QApplication.processEvents()




    def btn2_clicked(self): # 초기화 버튼
        self.lineEdit.setText('')
        self.count = 0
        self.all_email = []

        for i in range(self.listWidget2.count()):
            self.listWidget2.item(i).setText('')

        for i in range(self.listWidget.count()):
           item = self.listWidget.item(0)
           self.listWidget.takeItem(self.listWidget.row(item))


        #listItems=self.listA.selectedItems()
        #if not listItems: return
        #for item in listItems:
        #self.listA.takeItem(self.listA.row(item))



    def btn3_clicked(self):
        sys.exit() # 작업 종료


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()