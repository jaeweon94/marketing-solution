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
import openpyxl
import dropbox # dropbox
from uuid import getnode as get_mac # mac address
import json

form_class = uic.loadUiType("login_dialog.ui")[0]
form_class2 = uic.loadUiType("solution.ui")[0]




## 로긴 창 ##

class MyLogin(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.buttonBox.accepted.connect(self.login)
        self.buttonBox.rejected.connect(self.close)

        # self.accept는 QDialog의 함수 진짜 승인 한거임 '1'
        # self.reject는 QDialog의 함수 진짜 거절 한거임 '0' -> 따로 명령없으면 그냥 나가짐

    def login(self):

        serial_number = self.lineEdit.text()

        if serial_number in dic.keys():
            if dic[serial_number] == '0': #진짜 다 문자로 바꿔야한다!
                self.accept

                dic[serial_number] = mac
                personal[serial_number] = mac
                save_note(dic, 'lisence')
                save_note(personal, 'personal')

                dropbox_upload()

                QMessageBox.about(self, '정픔 인증 완료', '정품 인증되었습니다.')

            else:
                print(dic[serial_number])
                QMessageBox.about(self, '정픔 인증 실패', '이미 등록된 시리얼 키입니다.')
                sys.exit()
        else:
            QMessageBox.about(self, '정픔 인증 실패', '시리얼 키가 올바르지 않습니다.')

    def close(self):
        sys.exit()



## window창 ##

class MyWindow(QMainWindow, form_class2):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        ## keyword ##
        self.save_email = []
        self.user_key = ''

        self.pushButton0_1.clicked.connect(self.btn0_1_clicked) #검색1
        self.pushButton0_2.clicked.connect(self.btn0_2_clicked) #검색2
        self.pushButton1_1.clicked.connect(self.btn1_1_clicked) #선택1
        self.pushButton1_2.clicked.connect(self.btn1_2_clicked) #선택2
        self.pushButton1_3.clicked.connect(self.btn1_3_clicked) #선택3
        self.pushButton1_4.clicked.connect(self.btn1_4_clicked)    #수집 시작
        self.pushButton1_5.clicked.connect(self.btn1_5_clicked)    #수집 끝내기
        self.radio1_1.setChecked(True) # 이메일 방식 체크

        ## blog ##
        self.list_dict = {}
        self.pushButton2_1.clicked.connect(self.btn2_1_clicked)    #검색
        self.pushButton2_2.clicked.connect(self.btn2_2_clicked)    #수집 시작
        self.pushButton2_3.clicked.connect(self.btn2_3_clicked)    #수집 끝내기
        self.radio2_1.setChecked(True)


        ## cafe ##
        self.cafe_name = ''
        self.pushButton3_1.clicked.connect(self.btn3_1_clicked)   #검색
        self.pushButton3_2.clicked.connect(self.btn3_2_clicked)   #수집 시작
        self.pushButton3_3.clicked.connect(self.btn3_3_clicked)   #수집 끝내기
        self.radio3_1.setChecked(True)


        ## 중복 제거 ##
        self.all_email = []
        self.count = 0
        self.pushButton4_1.clicked.connect(self.btn4_1_clicked)  # 파일 열기
        self.pushButton4_2.clicked.connect(self.btn4_2_clicked)  # 중복 제거
        self.pushButton4_3.clicked.connect(self.btn4_3_clicked)  # 초기화
        self.pushButton4_4.clicked.connect(self.btn4_4_clicked)  # 끝내기
        self.radio4_1.setChecked(True)



    ## 중복 제거 ##
    def btn4_1_clicked(self):
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

            self.listWidget4_1.addItem('#{} {} / {}개'.format(self.count, file_name, count_list))
            self.listWidget4_2.item(1).setText('총 {}개 파일 / 누적 이메일 개수: {}개'.format(self.count, all_count_list))
        except FileNotFoundError:
            return
        except:
            QMessageBox.about(self, "Error", "올바른 파일이 아닙니다.")


    def btn4_2_clicked(self):

        if not os.path.isdir('pure_email'):
            os.mkdir('pure_email')

        if self.lineEdit4_1.text() == '':
            file_name = 'no_name'
        else:
            file_name = self.lineEdit4_1.text()

        pure_email = list(set(self.all_email))


        if self.radio4_2.isChecked():
            with open('pure_email/{}.txt'.format(file_name), 'w', newline='', encoding = 'euc-kr') as f:
                writer = csv.writer(f)
                for a in pure_email:
                    writer.writerow([a])
        else:
            with open('pure_email/{}.csv'.format(file_name), 'w', newline='', encoding = 'euc-kr') as f:
                writer = csv.writer(f)
                for a in pure_email:
                    writer.writerow([a])


        self.listWidget4_2.item(0).setText('[중복 제거 및 저장 완료]')
        QApplication.processEvents()

        self.listWidget4_2.item(1).setText('기존 이메일 개수 {}개'.format(len(self.all_email)))
        QApplication.processEvents()

        self.listWidget4_2.item(2).setText('중복 제거 후 이메일 개수 {}개'.format(len(pure_email)))
        QApplication.processEvents()



    # 초기화 버튼
    def btn4_3_clicked(self):
        self.lineEdit4_1.setText('')
        self.count = 0
        self.all_email = []

        for i in range(self.listWidget4_2.count()):
            self.listWidget4_2.item(i).setText('')

        for i in range(self.listWidget4_1.count()):
           item = self.listWidget4_1.item(0)
           self.listWidget4_1.takeItem(self.listWidget4_1.row(item))


        #listItems=self.listA.selectedItems()
        #if not listItems: return
        #for item in listItems:
        #self.listA.takeItem(self.listA.row(item))



    def btn4_4_clicked(self):
        sys.exit() # 작업 종료



    ## cafe define ##


    def btn3_1_clicked(self):
        for i in range(self.listWidget3_2.count()):  #검색버튼 누를 때 초기화시키기
           item = self.listWidget3_2.item(0)
           self.listWidget3_2.takeItem(self.listWidget3_2.row(item))

        for i in range(self.listWidget3_1.count()):
            self.listWidget3_1.item(i).setText('')


        self.cafe_name = self.lineEdit3_1.text()  ## lineEdit의  text를 읽는다.
        url = "http://cafe.naver.com/" + self.cafe_name
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html,'lxml')

        cafe_menu_list = soup.select('ul.cafe-menu-list a')
        # 63개


        self.listWidget3_2.addItem("(All)카페 모든 활성유저")
        for i in range(1,len(cafe_menu_list)):
            self.listWidget3_2.addItem(cafe_menu_list[i].get_text())
        QApplication.processEvents()



    def btn3_2_clicked(self):

        list_number = self.listWidget3_2.currentRow()

        if list_number == 0:
            self.ccc(0,self.listWidget3_2.count())
        else:
            self.ccc(list_number, list_number+1)


    def btn3_3_clicked(self):
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


        item = self.listWidget3_1.item(0)
        item.setText("{} 카페 활성유저 파악 중...".format(keyword))
        QApplication.processEvents()

        time.sleep(2)

        item = self.listWidget3_1.item(0)
        item.setText("{} 카페 활성유저 파악 완료/스텝 제거/수집 시작".format(keyword))
        QApplication.processEvents()


        for i in range(number1, number2):   #len(menu_url))= 60개, 1~59까지 59개
            if i ==0:
                continue

            item = self.listWidget3_1.item(2)
            item.setText("{a}개 항목 중 {b}번째 진행 중...".format(a=len(menu_url)-1,b=i))
            QApplication.processEvents()

            item = self.listWidget3_1.item(4)
            item.setText("{b}/{a}".format(a=len(menu_url)-1,b=i))
            QApplication.processEvents()

            last_page = self.lineEdit3_2.text()


            check_email_1 = []
            try:
                for j in (a for a in range(2, int(last_page))): # generator
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

                            if self.radio3_2.isChecked():
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

                            item = self.listWidget3_1.item(3)
                            item.setText("총 수집된 이메일 수 {}개".format(len(all_email)))
                            QApplication.processEvents()

                            item = self.listWidget3_1.item(6)
                            item.setText("중복 이메일 제거 후 {}개 저장 완료".format(len(pure_email)))
                            QApplication.processEvents()

                            ### make a csv file named cafe name ###
                        if self.radio3_2.isChecked():
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
                QMessageBox.about(self, 'Message', '숫자만 입력해주세요.')
                break
        ## when we click button, all we have to do is send to line Edit's content. so, we don't need to line edit


        item = self.listWidget3_1.item(0)
        item.setText("{} 분석 완료".format(url))
        QApplication.processEvents()

        item = self.listWidget3_1.item(3)
        item.setText("이메일 수집이 모두 완료되었습니다.")
        QApplication.processEvents()





    ## blog define ##

    def btn2_1_clicked(self):

        ### 모든 부분 초기화시키기 ###
        for i in range(self.listWidget2_2.count()):  #검색버튼 누를 때 초기화시키기
           item = self.listWidget2_2.item(0)
           self.listWidget2_2.takeItem(self.listWidget2_2.row(item))

        for i in range(self.listWidget2_1.count()):
            self.listWidget2_1.item(i).setText('')

        self.blog_name = self.lineEdit2_1.text()  ## blogname 저장
        self.list_dict = {}
        ### 초기화 작업 끝 ###



        self.listWidget2_2.addItem('[전체] 블로그 전체 수집')
        self.listWidget2_2.addItem('[이웃] 블로그 이웃 수집')
        set_number = self.listWidget2_2.count()


        url_1 = "http://blog.naver.com/PostList.nhn?from=postList&blogId={}&categoryNo=0&currentPage=1".format(self.blog_name)
        soup_1 = self.call_url(url_1)

        blog_all_list = soup_1.select('.border li a')

        c = []
        self.find_char2('category', blog_all_list, c)

        #for blog_list in blog_all_list:
         #   if 'category' in str(blog_list):
          #      c.append(blog_list)
        self.list_dict[0] = 0
        for i in range(len(c)):
            try:
                cat_name = c[i].get_text()
                self.listWidget2_2.addItem('[목록] {}'.format(cat_name))
                cat_number = int(c[i]['class'][2].split('|')[2])
                #self.list_dict[cat_name] = cat_number
                self.list_dict[i+set_number] = cat_number

            except:
                continue


        item = self.listWidget2_1.item(0)
        item.setText("블로그명: {}".format(self.blog_name))
        QApplication.processEvents()

        item = self.listWidget2_1.item(1)
        item.setText("블로그 이웃/목록 검색 완료")
        QApplication.processEvents()

        item = self.listWidget2_1.item(2)
        item.setText("이메일 추출 가능/목록 선택 후 추출 시작")
        QApplication.processEvents()



    ### MAIN ###
    def btn2_2_clicked(self):

        self.save_email = [] #클릭 누를 때마다 초기화





        list_number = self.listWidget2_2.currentRow()

        if list_number == 0:
            self.connect_email('ViewMoreFollowings')
            self.connect_email('ViewMoreFollowers')
            self.comment_email()


        elif list_number == 1:
            self.connect_email('ViewMoreFollowings')
            self.connect_email('ViewMoreFollowers')
        else:
            self.comment_email()



    def btn2_3_clicked(self):
        sys.exit() # 작업 종료



    def comment_email(self):
        try:
            category_n = self.list_dict[self.listWidget2_2.currentRow()]

            url_1 = "http://blog.naver.com/PostList.nhn?from=postList&blogId={}&categoryNo={}&currentPage=1".format(self.blog_name, category_n)
            soup_1 = self.call_url(url_1)
            page_number = int(soup_1.select('strong.itemSubjectBoldfont')[0].get_text()) #int 중요함


            if category_n == 0:
                item = self.listWidget2_1.item(6)
                item.setText("전체 글 {}개 수집 진행 중...".format(page_number))
                QApplication.processEvents()
            else:
                item = self.listWidget2_1.item(6)
                item.setText(" {}의 글 {}개 수집 진행 중...".format(self.listWidget2_2.currentItem().text(), page_number))
                QApplication.processEvents()


            for j in range(1,page_number+1):

                item = self.listWidget2_1.item(9)
                item.setText("{}/{}".format(j, page_number))
                QApplication.processEvents()

                time.sleep(0.5)
                url_2 = "http://blog.naver.com/PostList.nhn?from=postList&blogId={}&categoryNo={}&currentPage={}".format(self.blog_name, category_n, j)
                soup_2 = self.call_url(url_2)
                a = soup_2.select('iframe')

                for b in a:
                    if 'CommentFrm' in str(b):
                        c = b
                #type(c)  bs4.element.Tag라는 type이군. 그래서 None으로 뜨는 듯!

                p = re.compile('\d+') # \D는 숫자 뻬고, \d는 0-9 숫자 +는 1개 이상, *는 0개 이상
                log_number = int(p.findall(c['id'])[0]) #0383496209 이런 거

                url_3 = 'http://blog.naver.com/CommentList.nhn?blogId={}&logNo={}&currentPage=&isMemolog=false&focusingCommentNo=&showLastPage=true&shortestContentAreaWidth=false'.format(self.blog_name,log_number)
                soup_3 = self.call_url(url_3)

                id_list = soup_3.select('.nick')

                for each in id_list:
                    try:
                        a = each['href'].split('/')

                        if self.radio2_2.isChecked():
                            email = a[3]
                        else:
                            email = a[3] + '@naver.com'

                        self.save_email.append(email)


                        item = self.listWidget2_1.item(7)
                        item.setText("총 추출된 이메일 수 {}개".format(len(self.save_email)))
                        QApplication.processEvents()

                        item = self.listWidget2_1.item(11)
                        item.setText("[중복 제거 후]")
                        QApplication.processEvents()

                        item = self.listWidget2_1.item(12)
                        item.setText("총 {}개 저장 완료".format(len(list(set(self.save_email)))))
                        QApplication.processEvents()
                    except:
                        continue
                pure_email = list(set(self.save_email))

                if self.radio2_2.isChecked():
                    self.blog_csv('id', pure_email)
                else:
                    self.blog_csv('email', pure_email)

        except IndexError:
            QMessageBox.about(self, 'Message', '수집할 이메일이 없습니다.')


    def connect_email(self, kind):
        try:
            url_1 = "http://blog.naver.com/PostList.nhn?from=postList&blogId={}&categoryNo=0&currentPage=1".format(self.blog_name)
            soup_1 = self.call_url(url_1)

            buddy = soup_1.select('div#blog_buddyconnect iframe')
            aaa = buddy[0]['src']

            p = re.compile('widgetSeq=\d+')
            bbb = p.findall(aaa)[0]
            q = re.compile('\d+')
            widget_number = int(q.findall(bbb)[0])

            url = 'http://section.blog.naver.com/connect/ViewMoreBuddyPosts.nhn?blogId={}&widgetSeq={}'.format(self.blog_name,widget_number)
            soup_2 = self.call_url(url)

            find_gs = soup_2.select('script')
            ccc = self.find_char('gsBlogNo', find_gs)
            p = re.compile('gsBlogNo\s=\s\D*\d+') #  \D*의 사용으로 중간에 문자가 있든 없든 상관없음
            find_gs2 = p.findall(str(ccc)) #gsBlogNo = '19467274'
            q = re.compile('\d+')
            find_gs3 = q.findall(find_gs2[0]) # ['19467274']
            gs_number = int(find_gs3[0])


            item = self.listWidget2_1.item(6)
            item.setText("블로그 이웃 이메일 수집 진행 중...")
            QApplication.processEvents()

            item = self.listWidget2_1.item(9)
            item.setText("")
            QApplication.processEvents()



            k=1  #프로그램이 작업 중이라 중간에 작업을 끝내려면 X키를 눌러서 종료하셔야합니다. 조금만 기다려주세요!
            while True:
                try:
                    time.sleep(0.5)

                    apple = []
                    follower_url = 'http://section.blog.naver.com/connect/{}.nhn?blogId={}&currentPage={}&targetBlogNo={}'.format(kind,self.blog_name, k, gs_number)

                    c_soup = self.call_url(follower_url)

                    if kind == 'ViewMoreFollowers': # 나를 추가한 이웃
                        one_page_info = c_soup.select('dt.desc a')
                    else: # 내가 추가한 이웃
                        one_page_info = c_soup.select('dd.desc a')



                    for b in one_page_info: # b = each_info 개개인 정보
                        try:
                            if 'http://blog.naver.com/' in str(b):  #이 양식을 따라야 해줌
                                each_id = b['href'].split('/')[3]
                            elif '.blog.me' in str(b):
                                each_id = b['href'].split('.blog.me')[0][7:]
                            else:
                                continue

                            if self.radio2_2.isChecked():
                                email = each_id
                            else:
                                email = each_id + '@naver.com'

                            self.save_email.append(email)
                            apple.append(email)

                            item = self.listWidget2_1.item(7)
                            item.setText("총 추출된 이메일 수 {}개".format(len(self.save_email)))
                            QApplication.processEvents()

                            item = self.listWidget2_1.item(11)
                            item.setText("[중복 제거 후]")
                            QApplication.processEvents()

                            item = self.listWidget2_1.item(12)
                            item.setText("총 {}개 저장 완료".format(len(list(set(self.save_email)))))
                            QApplication.processEvents()

                        except:
                            continue

                    if len(apple) == 0:
                        break
                    k += 1
                    pure_email = list(set(self.save_email))
                    if self.radio2_2.isChecked():
                        self.blog_csv('id', pure_email)
                    else:
                        self.blog_csv('email', pure_email)

                except:
                    continue
        except IndexError:
            QMessageBox.about(self, 'Message', '이웃을 공개하지 않는 블로거입니다.')

    def call_url(self, url): #call url
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, 'lxml')
        return soup

    def find_char(self, char_name, char_list): #특정 단어가 있는 것(하나 있는 경우)
        for i in range(len(char_list)):
            if char_name in str(char_list[i]):
                return char_list[i]
                break


    def find_char2(self, char_name, char_list, c): #특정 단어가 있는 것들 리스트에 저장
        for i in range(len(char_list)):
            if char_name in str(char_list[i]):
                c.append(char_list[i])


    def blog_csv(self, method, email_list):
        with open('{}/blog_{}_{}.csv'.format(method,self.blog_name,self.listWidget2_2.currentRow()+1), 'w', newline='', encoding='euc-kr') as f:
            writer = csv.writer(f)
            for each_email in email_list:
                writer.writerow([each_email])



    ## keyword define ##
    def btn0_1_clicked(self): #검색1
        for i in range(self.listWidget1_2.count()):  #검색버튼 누를 때 연관1 초기화시키기
           item = self.listWidget1_2.item(0)
           self.listWidget1_2.takeItem(self.listWidget1_2.row(item))

        for i in range(self.listWidget1_3.count()):  #검색버튼 누를 때 연관2 초기화시키기
           item = self.listWidget1_3.item(0)
           self.listWidget1_3.takeItem(self.listWidget1_3.row(item))

        self.lineEdit1_2.setText('')



        page_url = 'https://www.naver.com'
        headers = {
            'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'),
            "Accept-Encoding": "gzip, deflate",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            'Referer': page_url,
        }


        user_key = self.lineEdit1_1.text()  ## lineEdit의  text를 읽는다.
        keyword = user_key.replace(' ', '+')
        c_url = 'https://search.naver.com/search.naver?where=nexearch&ie=utf8&query={}&start=1'.format(keyword).encode('utf-8')
        response = requests.get(c_url, headers = headers)
        html = response.text
        c_soup = BeautifulSoup(html, 'lxml')

        relate = c_soup.select('dd.lst_relate li a')

        for relate_key in relate:
            self.listWidget1_2.addItem(relate_key.get_text())



    def btn0_2_clicked(self): #검색2
        for i in range(self.listWidget1_3.count()):  #검색버튼 누를 때 연관2 초기화
           item = self.listWidget1_3.item(0)
           self.listWidget1_3.takeItem(self.listWidget1_3.row(item))


        ## 검색 ##
        page_url = 'https://www.naver.com'
        headers = {
            'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'),
            "Accept-Encoding": "gzip, deflate",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            'Referer': page_url,
        }


        user_key = self.listWidget1_2.currentItem().text()  ## lineEdit의  text를 읽는다.
        keyword = user_key.replace(' ', '+')

        c_url = 'https://search.naver.com/search.naver?where=nexearch&ie=utf8&query={}&start=1'.format(keyword).encode('utf-8')
        response = requests.get(c_url, headers = headers)
        html = response.text
        c_soup = BeautifulSoup(html, 'lxml')

        relate = c_soup.select('dd.lst_relate li a')

        for relate_key in relate:
            self.listWidget1_3.addItem(relate_key.get_text())





    def btn1_1_clicked(self): #선택1
        self.lineEdit1_2.setText(self.lineEdit1_1.text())


    def btn1_2_clicked(self): #선택2
        self.lineEdit1_2.setText(self.listWidget1_2.currentItem().text())


    def btn1_3_clicked(self): #선택3
        self.lineEdit1_2.setText(self.listWidget1_3.currentItem().text())




    def btn1_4_clicked(self): #수집
        ## 초기화 ##
        for i in range(self.listWidget1_1.count()): #작업보드 초기화
            self.listWidget1_1.item(i).setText('')

        self.save_email = []


        self.user_key = self.lineEdit1_2.text()
        keyword = self.user_key.replace(' ', '+')

        item = self.listWidget1_1.item(0)
        item.setText('#{} 키워드 검색'.format(self.user_key))
        QApplication.processEvents()

        item = self.listWidget1_1.item(1)
        item.setText('6개월 내 키워드 포함 블로그/카페 파악 완료')
        QApplication.processEvents()

        item = self.listWidget1_1.item(4)
        item.setText('블로그 활성유저 이메일 수집 중...')
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


        ### 블로그 시작 ###

        for j in range(100):

            item = self.listWidget1_1.item(7)
            item.setText('{}/200페이지'.format(j+1))
            QApplication.processEvents()


            time.sleep(1.5)

            b_page_number = j*10 + 1

            b_url = 'https://search.naver.com/search.naver?where=post&ie=utf8&query={}&start={}&date_option=6'.format(keyword, b_page_number).encode('utf-8')
            response = requests.get(b_url, headers = headers)
            html = response.text
            soup = BeautifulSoup(html, 'lxml')


            for each_content in soup.select('div.thumb-rollover a.sp_thmb'):
                try:
                    each_url = each_content['href']
                    if 'blog.me' in each_url:
                        b_info_3 = each_url
                        b_info = b_info_3.split('.blog.me/')
                        blog_id = b_info[0][7:]
                        log_no = b_info[1]
                        if self.radio1_2.isChecked():
                            b_host_email = blog_id
                        else:
                            b_host_email = blog_id + '@naver.com'
                        self.save_email.append(b_host_email)
                    else:
                        b_info_1 = each_url
                        b_info_2 = b_info_1.split('/')
                        b_info = b_info_2[3].split('?Redirect=Log&logNo=')
                        blog_id = b_info[0]
                        log_no = b_info[1]
                        if self.radio1_2.isChecked():
                            b_host_email = blog_id
                        else:
                            b_host_email = blog_id + '@naver.com'
                        self.save_email.append(b_host_email)

                    time.sleep(0.3)

                    url_3 = 'http://blog.naver.com/CommentList.nhn?blogId={}&logNo={}&currentPage=&isMemolog=false&focusingCommentNo=&showLastPage=true&shortestContentAreaWidth=false'.format(blog_id, log_no)
                    response = requests.get(url_3)
                    html = response.text
                    soup = BeautifulSoup(html, 'lxml')

                    id_list = soup.select('.nick')

                    for each in id_list:
                        try:
                            a = each['href'].split('/')
                            comment_id = a[3]
                            if self.radio1_2.isChecked():
                                b_guest_email = comment_id
                            else:
                                b_guest_email = comment_id + '@naver.com'

                            self.save_email.append(b_guest_email)

                            item = self.listWidget1_1.item(5)
                            item.setText('수집된 이메일 수: {}개'.format(len(self.save_email)))
                            QApplication.processEvents()

                            item = self.listWidget1_1.item(9)
                            item.setText('중복 제거 후 이메일 {}개 저장 완료'.format(len(list(set(self.save_email)))))
                            QApplication.processEvents()

                            pure_email = list(set(self.save_email))

                            if self.radio1_2.isChecked():
                                self.keyword_csv('id', pure_email)
                            else:
                                self.keyword_csv('email', pure_email)

                        except:
                            continue
                except:
                    continue



        item = self.listWidget1_1.item(4)
        item.setText('카페 활성유저 이메일 수집 중...')
        QApplication.processEvents()


        ### 카페 시작 ###

        for k in range(100):
            item = self.listWidget1_1.item(7)
            item.setText('{}/200페이지'.format(k+101))
            QApplication.processEvents()

            time.sleep(1.5)

            c_page_number = k*10 + 1
            c_url = 'https://search.naver.com/search.naver?where=article&ie=utf8&query={}&start={}&date_option=6'.format(keyword, c_page_number).encode('utf-8')
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

                    time.sleep(0.3)

                    url_host = 'http://cafe.naver.com/ArticleRead.nhn?&clubid={}&articleid={}'.format(club_id, article_id)

                    response = requests.get(url_host)
                    html = response.text
                    c_soup2 = BeautifulSoup(html, 'lxml')
                    f_host_id = c_soup2.select('div.other_view a')[0]

                    host_id = f_host_id['href'].split('memberid=')[1]
                    if self.radio1_2.isChecked():
                        host_email = host_id
                    else:
                        host_email = host_id + '@naver.com'
                    self.save_email.append(host_email)
                    #print('h', host_email)

                    ## guest(comment) ID ##
                    url_guest = 'http://cafe.naver.com/CommentView.nhn?search.clubid={}&search.articleid={}&search.page=1'.format(club_id, article_id)
                    response = requests.get(url_guest)
                    html = response.text

                    dict = json.loads(html)

                    for info in dict['result']['list']:
                        guest_id = info['writerid']
                        if self.radio1_2.isChecked():
                            guest_email = guest_id
                        else:
                            guest_email = guest_id + '@naver.com'

                        self.save_email.append(guest_email)

                        item = self.listWidget1_1.item(5)
                        item.setText('수집된 이메일 수: {}개'.format(len(self.save_email)))
                        QApplication.processEvents()

                        item = self.listWidget1_1.item(9)
                        item.setText('중복 제거 후 이메일 {}개 저장 완료'.format(len(list(set(self.save_email)))))
                        QApplication.processEvents()

                        pure_email = list(set(self.save_email))

                        if self.radio1_2.isChecked():
                            self.keyword_csv('id', pure_email)
                        else:
                            self.keyword_csv('email', pure_email)

                except:
                    continue



    def btn1_5_clicked(self): #수집 끝내기
        sys.exit() # 작업 종료


    ## csv 저장 경로 ##
    def keyword_csv(self, method, email_list):
        with open('{}/key_{}.csv'.format(method,self.user_key), 'w', newline='', encoding='euc-kr') as f:
            writer = csv.writer(f)
            for each_email in email_list:
                writer.writerow([each_email])






## dropbox ##

def save_note(dic_name, file_name):

    with open('C:/lisence/{}.txt'.format(file_name), 'w') as f: # lisence.txt 읽은 후 dic에 저장
        for i in dic_name.keys():
            f.write('{} {}'.format(i, dic_name[i]) + '\n')
        f.close()


def save_dic(dic_name, file_name):
    try:
        with open('C:/lisence/{}.txt'.format(file_name), 'r') as f: # lisence.txt 읽은 후 dic에 저장
            lines = f.readlines()
            for line in lines:
                b= line.split()
                dic_name[b[0]] = b[1]
            f.close()
    except:
        myLogin.accept


def dropbox_download():

    if not os.path.isdir('C:/lisence'):
        os.mkdir('C:/lisence')

    metadata, f = dbx.files_download('/lisence.txt') # download
    with open('C:/lisence/lisence.txt', 'wb') as a: # lisence.txt 만들어서 거기에 복사
        a.write(f.content)
        a.close()

    save_dic(dic, 'lisence') #lisence.txt의 정보 dic에 저장


def dropbox_upload():

    dbx.files_delete('/lisence.txt') # 드랍박스 안의 메모장 삭제 후

    with open("C:/lisence/lisence.txt", "rb") as f:
        dbx.files_upload(f.read(), '/lisence.txt', mute = True)

    os.remove('C:/lisence/lisence.txt')  # lisence.txt 삭제




## main ##

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myLogin = MyLogin()

    # 전역변수 선언
    mac = get_mac()
    dbx = dropbox.Dropbox("Fy-Abh9C9uAAAAAAAAAADZJzmKaLWXXF1R2UJoZT6WcAhiC_kHYgKPdNWarMJpuc")
    dic = {}
    personal = {}


    ## 폴더 생성 ##
    if not os.path.isdir('email'):
        os.mkdir('email')

    if not os.path.isdir('id'):
        os.mkdir('id')

    if not os.path.isdir('C:/lisence'):
        os.mkdir('C:/lisence')

    # lisence.txt 다운로드 받고, dic에 저장한 후 바로 삭제
    dropbox_download()
    os.remove('C:/lisence/lisence.txt')  # lisence.txt 삭제
    save_dic(personal, 'personal')


    if str(mac) in dic.values() or str(mac) in personal.values(): # mac은 int이기 때문에, str(mac)으로!
        myWindow = MyWindow()
        myWindow.show()
        app.exec_()
    else:
        if myLogin.exec_() == QDialog.Accepted:
            Mywindow = MyWindow()
            Mywindow.show()
            sys.exit(app.exec_())

