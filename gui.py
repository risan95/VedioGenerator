from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

from spider import VGSpider
from paint import VGPaint

class mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # 生成spider和paint类
        self.spider = VGSpider()
        self.paint = VGPaint()

        uic.loadUi("VG_UI/mainwindow.ui", self)
        self.set_actions()

    def set_actions(self):
        # 主界面
        # 定义导航按钮组
        self.nav_buttons = [
            self.B1, self.B2, self.B3
        ]
        self.current_button = self.B1
        self.current_button.setEnabled(False)
        # 换页事件
        for button in self.nav_buttons:
            button.clicked.connect(self.change_page)
        
        # 各分页事件
        self.set_actions_page1()
        self.set_actions_page2()

    def change_page(self):
        # QMessageBox.about(self, "click", "yes")
        button_page = self.sender().property("page_num")
        self.stackedWidget.setCurrentIndex(button_page - 1)
        # 按钮状态变换
        self.current_button.setEnabled(True)
        self.current_button = self.sender()
        self.current_button.setEnabled(False)

    ##### page1 #####
    def set_actions_page1(self):
        self.category = "world"
        for category_tuple in self.spider.category_list:
            self.P1_CB_CAT.addItem(category_tuple[0], category_tuple[1])
        self.P1_CB_CAT.currentIndexChanged.connect(self.page1_CB_CAT_changed)
        self.P1_B_SELECT.clicked.connect(self.page1_B_SELECT_clicked)

        self.page1_LW_NEWS_update() # 默认执行一次采集

    def page1_CB_CAT_changed(self):
        self.P1_LW_NEWS.clear()
        self.category = self.sender().currentData()
        self.page1_LW_NEWS_update()
    
    def page1_LW_NEWS_update(self):
        self.news_list = self.spider.scrape_news_topics(self.category)
        for news_tuple in self.news_list:
            self.P1_LW_NEWS.addItem(news_tuple[0])

    def page1_B_SELECT_clicked(self):
        row = self.P1_LW_NEWS.currentRow()
        if row != -1:
            self.news_title = self.news_list[row][0]
            self.pickup_url = self.news_list[row][1]
            # 页面2读取新闻封面
            self.P2_WEV.load(QUrl(self.pickup_url))
            # 将标题传给页面2的Line Edit
            self.P2_LE_TITLE.setText(self.news_title)
            self.P2_L_TITLE.setText(self.news_title)
            # 页面1 -> 页面2
            self.stackedWidget.setCurrentIndex(1)
            self.B1.setEnabled(True)
            self.B2.setEnabled(False)

    ##### page2 #####
    def set_actions_page2(self):
        # 生成WebEngineView及Mask
        self.P2_WEV = QWebEngineView(self.page_2)
        self.P2_WEV.setGeometry(QtCore.QRect(0, 30, 640, 270))
        self.P2_WEV.hide() 
        self.P2_WEV_MASK = QWidget(self.page_2)
        self.P2_WEV_MASK.setGeometry(QtCore.QRect(0, 30, 640, 270))
        self.P2_WEV.loadFinished.connect(self.page2_WEV_load_finished)
        # 生成标题label
        self.P2_LE_TITLE = QtWidgets.QLineEdit(self.page_2)
        self.P2_LE_TITLE.setGeometry(QtCore.QRect(0, 350, 641, 41))
        self.P2_LE_TITLE.setObjectName("P2_LE_TITLE")
        self.P2_LE_TITLE.textChanged.connect(lambda: self.P2_L_TITLE.setText(self.sender().text()))
        self.label_5 = QtWidgets.QLabel(self.page_2)
        self.label_5.setGeometry(QtCore.QRect(0, 65, 625, 90))
        self.label_5.setStyleSheet( "font: 28pt \"Noto Sans Mono CJK\";\n"
                                    "color:white;\n"
                                    "background-color: rgba(0,0,0,0.5);")
        self.label_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.label_5.setText("  日网评论：")
        self.P2_L_TITLE = QtWidgets.QLabel(self.page_2)
        self.P2_L_TITLE.setGeometry(QtCore.QRect(0, 155, 625, 90))
        self.P2_L_TITLE.setStyleSheet(  "font: 28pt \"Noto Sans Mono CJK\";\n"
                                        "color:white;\n"
                                        "background-color: rgba(0,0,0,0.5);")
        self.P2_L_TITLE.setAlignment(QtCore.Qt.AlignCenter)
        self.P2_L_TITLE.setObjectName("P2_L_TITLE")
        

    def page2_WEV_load_finished(self):
        self.P2_WEV.page().runJavaScript("window.scrollTo(0,215);")
        self.P2_WEV.show()
        self.P2_B_PRINT.setText("打印")
        self.P2_B_PRINT.setEnabled(True)