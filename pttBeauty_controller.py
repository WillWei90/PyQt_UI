from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
from pttBeauty_UI import Ui_MainWindow
import requests
import os
from bs4 import BeautifulSoup
import re
import cv2

# last_img_index = 0 #紀錄最後顯示圖片的索引值
# picsList = list() #儲存圖片連結的list
# file_extension = ''

class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
		# in python3, super(Class, self).xxx = super().xxx
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setup_control()
        self.picsList = list() #儲存圖片連結的list
        self.last_img_index = 0 #紀錄最後顯示圖片的索引值

    def setup_control(self):
        # TODO
        self.setWindowTitle('PTT圖片搜尋應用程式') #設定視窗title
        self.ui.url_title.setText('輸入下載圖片的ptt版網址')
        self.ui.keyword_title.setText('輸入查詢的關鍵字')
        self.ui.num_title.setText('輸入查詢圖片的數量')
        self.ui.result_label.setText('下載結果提示區塊')
        self.ui.pic_label.setText('圖片預覽區塊')
        self.ui.search_btn.setText('查詢')
        
        #按下search_btn時呼叫搜尋的函數
        self.ui.search_btn.clicked.connect(self.search_display)
        
        self.ui.pre_btn.setText('上一張')
        self.ui.pre_btn.clicked.connect(self.pre_btnClicked)
        self.ui.next_btn.setText('下一張')
        self.ui.next_btn.clicked.connect(self.next_btnClicked)
        self.ui.result_label2.setText('圖片顯示結果提示區塊')
    
    def search_display(self):
        self.ui.result_label.setText('搜尋圖片下載中\n請您耐心等候謝謝')
        self.search_btnClicked()
    
    def search_btnClicked(self):
        
        #輸入的內容儲存在變數裡
        self.last_img_index = 0 #因為重新搜尋,將紀錄最後顯示圖片的索引值歸零
        self.picsList = list() #因為重新搜尋,將儲存圖片連結的list初始化為空list
        url = self.ui.url_entry.text() #設定要抓取的網址,哪個版的主頁
        keyword = self.ui.keyword_entry.text()
        img_num = int(self.ui.num_entry.text())
        
        My_data = {'from':'/bbs/Beauty/index.html',
                   'yes':'yes'}
        sess = requests.Session()
        sess.post('https://www.ptt.cc/ask/over18', data = My_data)
        
        count = 0 #下載圖片數量計數用
        os.makedirs(keyword,exist_ok=True)
        
        while True:
            titleList = list()
            titleUrlList = list()
            response = sess.get(url)
            
            if(response.status_code == requests.codes.ok):
                result = response.text.split('<div class="r-list-sep">')[0] #ptt底部底線切割,索引0取上半部
                soup = BeautifulSoup(result,'html.parser')
                nextUrl = 'https://www.ptt.cc'+soup.select('a.btn.wide')[1].get('href') #設定抓取上一頁的網址
                titleTags = soup.select('div.title a')
                
                #篩選標題
                for title in reversed(titleTags): #使用reversed()取資料，代表每一頁倒著取資料
                    if(keyword in title.text):
                        titleList.append(title.text) #篩出的標題加入title串列
                        titleUrlList.append(title.get("href")) #篩出的標題連結加入titleUrl串列
                        
                        # print('標題:',title.text)
                        # print('連結:','https://www.ptt.cc'+title.get('href'))
                
                #進入文章抓內文
                for i in titleUrlList:
                    response2 = sess.get('https://www.ptt.cc' + i)
                    if(response2.status_code == requests.codes.ok):
                        soup2 = BeautifulSoup(response2.text,'html.parser')
                        imgTags = soup2.select('a') #抓所有內文節點 a
                        
                        #遍歷所有抓到的a節點
                        for Tag in imgTags:
                            
                            # 正規表達式 ^(?!.*\bimgur\b).* 指不要取有imgur單字, 因為imgur網站response3.status_code是429
                            #正規表達式 \.(jpg|jpeg|png|gif)$ 指結尾要是這些, 不要有gif原因是pyQt介面用cvs.imread()時gif不能讀
                            if(re.findall(r'^(?!.*\bimgur\b).*\.(jpg|jpeg|png)$', Tag.get('href'))):
                                imgUrl = Tag.get('href') #抓所有內文節點 a 的圖片連結
                                self.picsList.append(imgUrl) #將圖片連結加入pics串列
                            
                                response3 = sess.get(imgUrl) #發送請求進入圖片連結
                                print('第{}張response3.status_code:{}'.format(count, response3.status_code))
                                if(response3.status_code == requests.codes.ok):
                                    
                                    file_extension = os.path.splitext(imgUrl)[1]  # 得到包含點號的副檔名，如 .jpg、.jpeg
                                    with open(keyword + '/' + str(count) + file_extension, 'wb') as imgFile:
                                        for chunk in response3:
                                            imgFile.write(chunk)
                                            # print(imgUrl)
                                        count += 1 #計數加一
            
                                        if(count == img_num):
                                            #將result_title顯示文字更新
                                            self.ui.result_label.setText('{}圖片下載完成,\n下載圖片數量已達{}張'.format(keyword,count))
                                            print('{}圖片下載完成,\n下載圖片數量已達{}張'.format(keyword,count))
                                            print('self.picsList:',self.picsList)
                                            print('-'*30)
                                            previous_dir = os.getcwd()
                                            os.chdir(keyword)
                                            print('os.getcwd():',os.getcwd())
                                            
                                            # 得到包含點號的副檔名，如 .jpg、.jpeg
                                            file_extension = os.path.splitext(self.picsList[0])[1]
                                            self.img_path = '0'+file_extension
                                            print('self.img_path:',self.img_path)
                                            self.img = cv2.imread(self.img_path)
                                            
                                            # 根據 pic_label 大小調整
                                            # 設定 pic_label 大小
                                            label_width = self.ui.pic_label.width()
                                            label_height = self.ui.pic_label.height()
                                            self.img = cv2.resize(self.img, (label_width, label_height))
                                            
                                            height, width, channel = self.img.shape
                                            bytesPerline = 3 * width
                                            self.qimg = QImage(self.img, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
                                            
                                            # 設定 pic_label 大小
                                            label_width = self.ui.pic_label.width()
                                            label_height = self.ui.pic_label.height()
                                            
                                            # # 根據 pic_label 的大小縮放圖片, 保持圖片寬高比
                                            # pixmap = QPixmap.fromImage(self.qimg).scaled(label_width, label_height, Qt.KeepAspectRatio)
                                            
                                            # self.ui.pic_label.setPixmap(pixmap)
                                            self.ui.pic_label.setPixmap(QPixmap.fromImage(self.qimg))
                                            self.ui.pic_label.adjustSize()
                                            self.last_img_index = 0
                                            self.ui.result_label2.setText('{}的第{}張圖片'.format(keyword, self.last_img_index +1))
                                            # self.ui.pic_label.setPixmap(QPixmap.fromImage(self.qimg))
                                            # self.ui.pic_label.adjustSize()
                                            os.chdir(previous_dir)
                                            print('-'*30)
                                            return

                url = nextUrl

    def pre_btnClicked(self):
        keyword = self.ui.keyword_entry.text()
        if(self.last_img_index == 0):
            self.ui.result_label2.setText('{}的第{}張圖片\n沒有更前面的圖片'.format(keyword, self.last_img_index +1))
            return
        else:
            #因cv2.imread()讀取的路徑不能有中文，所以用程式控制進入下個目錄，做完事情最後再返回當前目錄
            #記錄當前目錄，並進入下個目錄準備讀取圖片(下個目錄是關鍵字建立的資料夾)
            previous_dir = os.getcwd()
            os.chdir(keyword)
            print('os.getcwd():',os.getcwd())
            
            # 得到包含點號的副檔名，如 .jpg、.jpeg
            file_extension = os.path.splitext(self.picsList[self.last_img_index - 1])[1]
            self.img_path = str(self.last_img_index - 1)+file_extension
            print('self.img_path:',self.img_path)
            self.img = cv2.imread(self.img_path)
            
            # 根據 pic_label 大小調整
            # 設定 pic_label 大小
            label_width = self.ui.pic_label.width()
            label_height = self.ui.pic_label.height()
            self.img = cv2.resize(self.img, (label_width, label_height))
            
            height, width, channel = self.img.shape
            bytesPerline = 3 * width
            self.qimg = QImage(self.img, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
            
            # # 根據 pic_label 的大小縮放圖片, 保持圖片寬高比
            # pixmap = QPixmap.fromImage(self.qimg).scaled(label_width, label_height, Qt.KeepAspectRatio)
            
            # self.ui.pic_label.setPixmap(pixmap)
            self.ui.pic_label.setPixmap(QPixmap.fromImage(self.qimg))
            self.ui.pic_label.adjustSize()
            self.last_img_index -= 1
            self.ui.result_label2.setText('{}的第{}張圖片'.format(keyword, self.last_img_index +1))
            # self.ui.pic_label.setPixmap(QPixmap.fromImage(self.qimg))
            # self.ui.pic_label.adjustSize()
            os.chdir(previous_dir)
            print('-'*30)
            return
    
    def next_btnClicked(self):
        keyword = self.ui.keyword_entry.text()
        if(self.last_img_index +1 == len(self.picsList)):
            self.ui.result_label2.setText('{}的第{}張圖片\n這是最後一張圖片\n沒有更後面的圖片'.format(keyword, self.last_img_index +1))
            return
        else:
            #因cv2.imread()讀取的路徑不能有中文，所以用程式控制進入下個目錄，做完事情最後再返回當前目錄
            #記錄當前目錄，並進入下個目錄準備讀取圖片(下個目錄是關鍵字建立的資料夾)
            previous_dir = os.getcwd()
            os.chdir(keyword)
            print('os.getcwd():',os.getcwd())
            
            # 得到包含點號的副檔名，如 .jpg、.jpeg
            file_extension = os.path.splitext(self.picsList[self.last_img_index + 1])[1]
            self.img_path = str(self.last_img_index + 1)+file_extension
            print('self.img_path:',self.img_path)
            self.img = cv2.imread(self.img_path)
            
            # 根據 pic_label 大小調整
            # 設定 pic_label 大小
            label_width = self.ui.pic_label.width()
            label_height = self.ui.pic_label.height()
            self.img = cv2.resize(self.img, (label_width, label_height))
            
            height, width, channel = self.img.shape
            bytesPerline = 3 * width
            self.qimg = QImage(self.img, width, height, bytesPerline, QImage.Format_RGB888).rgbSwapped()
            
            # # 根據 pic_label 的大小縮放圖片, 保持圖片寬高比
            # pixmap = QPixmap.fromImage(self.qimg).scaled(label_width, label_height, Qt.KeepAspectRatio)
            
            # self.ui.pic_label.setPixmap(pixmap)
            self.ui.pic_label.setPixmap(QPixmap.fromImage(self.qimg))
            self.ui.pic_label.adjustSize()
            self.last_img_index += 1
            self.ui.result_label2.setText('{}的第{}張圖片'.format(keyword, self.last_img_index +1))

            os.chdir(previous_dir)
            print('-'*30)
            return
    

    

        
        
        
        
        
        
        
        