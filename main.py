try:
    import requests
    from signal import signal
    from time import sleep
    from selenium import webdriver
    #import undetected_chromedriver.v2 as webdriver
    from pywinauto import Application
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.service import Service as ChromeService
    from random import randint
    from subprocess import CREATE_NO_WINDOW
    import requests,random,os,sys,xlsxwriter,json
    from PyQt5.QtWidgets import QApplication,QMainWindow,QTableWidgetItem,QMessageBox,QMenu,QFileDialog,QTableWidget,QWidget,QAbstractItemView
    from PyQt5.QtCore import pyqtSignal,QThread,QEvent,QSettings,QCoreApplication,Qt
    from PyQt5 import QtGui
    from ui import Ui_toolfb
except:
    import os
    from time import sleep
    os.system("pip install selenium")
    os.system("pip install xlsxwriter")
    os.system("pip install PyQt5")
    os.system("pip install requests")
    os.system("pip install pywinauto")
    os.system("pip install undetected_chromedriver")
    print("__________Vui lòng chạy lại tool__________")
    sleep(2)
    quit()
class loadprofile(QThread):
    sign3=pyqtSignal(str,int,int)
    def __init__(self,txt=0):
        super().__init__()
        self.txt=txt
        #self.api=api
        #print(self.web,self.api) 
        self.k=0  
    def checkprofile(self,r):
        try:
            headers = {
                'accept': 'application/json',
            }
            getprofile = requests.get(f'http://localhost:35353/profiles/{r}', headers=headers).json()
        except:pass
    def run(self):
        n=[]
        headers = {
            'accept': 'application/json',
        }


        params = {
            'sort': 'name',
            'sort_type': 'desc',
        }
        get_all_profile = requests.get('http://localhost:35353/profiles', params=params, headers=headers).json()
        list_profile=get_all_profile['docs']
        #print(list_profile)
        try:
            for pro in range(len(list_profile)):
                if list_profile[pro]['group']['name']==self.txt:
                    self.sign3.emit(list_profile[pro]['name'],list_profile[pro]['id'],self.k)
                    self.k+=1
                try:
                    if list_profile[pro]['id']==int(self.txt):
                        self.sign3.emit(list_profile[pro]['name'],list_profile[pro]['id'],self.k)
                        self.k+=1
                except:
                    pass
        except:
            self.sign3.emit('none','none',0)
            
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic = Ui_toolfb()
        self.uic.setupUi(self)
        self.uic.btnload.clicked.connect(self.loadprofiles)
        self.uic.btnstart.clicked.connect(self.startthread)
        self.uic.tbtfileclone.clicked.connect(self.fileclone)
        self.uic.tbtprofilepage.clicked.connect(self.profilepag)
        self.uic.tbttitile.clicked.connect(self.titlefile)
        self.uic.tbtnfoldervideo.clicked.connect(self.foldrvideo)
        self.uic.viewaccount.installEventFilter(self)
        self.thread={}
        self.k=self.clicklo=self.checkselectall=self.check=self.l2=self.count=self.stopth=0
        self.checktxt=''
    def profilepag(self):
        linkpro=os.path.join(os.getcwd(), 'data','profileaccount')
        os.startfile(linkpro)
    def titlefile(self):
        linkpro=os.path.join(os.getcwd(), 'data','title.txt')
        os.startfile(linkpro)
    def foldrvideo(self):
        linkpro=os.path.join(os.getcwd(), 'video_data')
        os.startfile(linkpro)
    def fileclone(self):
        if self.uic.login.isChecked():
            linkpro=os.path.join(os.getcwd(), 'data','clone','logincookie.txt')
        elif self.uic.nologin.isChecked:
            linkpro=os.path.join(os.getcwd(), 'data','clone','loginuserpass.txt')
        os.startfile(linkpro)
    def loadprofiles(self):
        txt=self.uic.txtgroups.text()
        #self.uic.viewaccount.clearMask()
        #print(txt)
        if txt!=self.checktxt:
            self.checktxt=txt
            self.thread[0]=loadprofile(txt)
            self.thread[0].start()
            self.thread[0].sign3.connect(self.loadpro)
    def messagebox2(self,title,text):
        msg=QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(title)
        #msg.setInformativeText("Hãy nhập thêm sproxy")
        msg.setText(text)
        msg.exec_()
    def loadpro(self,namepro,idpro,k):
        #print(idpro)
        if namepro=='none' and idpro== 'none' and k ==0:
            self.messagebox2('Thông báo','Sai thông tin kiểm tra lại')
        else:
            self.uic.viewaccount.insertRow(k)
            self.uic.viewaccount.setItem(k,0,QTableWidgetItem(str(idpro)))
            self.uic.viewaccount.setItem(k,1,QTableWidgetItem(str(namepro)))
            self.uic.viewaccount.sortItems(0)
        #self.uic.viewaccount.setSortingEnabled(True)
    def startthread(self):
        thread=int(self.uic.Thread.text())
        threadpage=int(self.uic.repageThread.text())
        regpage=self.uic.chbreg.isChecked()
        #login=self.uic.login.isChecked()
        threadvideo=int(self.uic.threadvideo.text())
        upreeels=self.uic.groupBox_3.isChecked()
        if self.uic.rdbcmt.isChecked():
            cmtup=True
        elif self.uic.rdbnocmt.isChecked():
            cmtup=False
        if self.uic.login.isChecked():
            login=True
        elif self.uic.nologin.isChecked():
            login=False
        if thread < self.uic.viewaccount.rowCount():
            self.i=thread
        else:
            self.i=self.uic.viewaccount.rowCount()
        if self.l2 ==0:
            for i in range(self.i):
                idprofile=self.uic.viewaccount.item(i,0).text()
                self.thread[i]=runtool(threadpage,upreeels,cmtup,regpage,threadvideo,idprofile,login,i)
                self.thread[i].start()
                self.thread[i].sign.connect(self.textstatus)
                self.thread[i].sign2.connect(self.done)
                self.k+=1
        else:
            idprofile=self.uic.viewaccount.item(self.k,0).text()
            self.thread[self.k]=runtool(threadpage,upreeels,cmtup,regpage,threadvideo,idprofile,login,self.k)
            self.thread[self.k].start()
            self.thread[self.k].sign.connect(self.textstatus)
            self.thread[self.k].sign2.connect(self.done)
            self.k+=1
    def stop(self):
        self.k=self.clicklo=self.checkselectall=self.check=self.l2=self.count=self.stopth=0
    def done(self,suc,l2,r):
        rowCount=self.uic.viewaccount.rowCount()
        self.l2=l2
        if self.count==self.i:
            self.count=0
        if suc==1:
            self.thread[r].stop()
            self.check+=1
            self.count+=1
        if self.stopth==0:
            if(rowCount-self.k>=self.i):
                self.startthread()
            elif rowCount-self.k>0:
                self.startthread()
            elif self.check==self.k:
                self.stopth=1
                self.stop()
        else:
            self.stop()

    def textstatus(self,msg,r,thread):
        try:
            self.uic.viewaccount.setItem(thread,r,QTableWidgetItem(str(msg)))
        except:pass
    def eventFilter(self, source, event):
        if event.type()==QEvent.ContextMenu and source is self.uic.viewaccount:
            contextMenu=QMenu()
            start=contextMenu.addAction('Chọn tất cả')
            deleted=contextMenu.addAction('Xoá')
            action=contextMenu.exec_(event.globalPos())
            if action == deleted:
                if self.checkselectall==1:
                    #print(1)
                    self.checktxt=''
                    self.checkselectall=0
                indexes = self.uic.viewaccount.selectionModel().selectedRows()
                k=[]
                for index in indexes:
                    k.append(index.row())
                k.sort(reverse=True)
                for i in k:
                    self.uic.viewaccount.removeRow(i)
            elif action == start:
                self.checkselectall=1
                self.uic.viewaccount.selectAll()
        return super().eventFilter(source, event)
class runtool(QThread):
    sign2=pyqtSignal(int,int,int)
    sign=pyqtSignal(str,int,int)
    def __init__(self,threadpage=0,upreeels=0,cmtup=0,regpage=0,threadvideo=0,profile_id=0,loged=0,r=0):
        super().__init__()
        self.r=r
        self.threadpage=threadpage
        self.regpage=regpage
        self.profile_id = profile_id
        self.loged=loged
        self.upreeels=upreeels
        self.cmtup=cmtup
        self.threadvideo=threadvideo
        self.pro=''
        self.link=''
    def closechrome(self):
        headers = {
            'accept': 'application/json',
        }
        response = requests.get(f'http://localhost:35353/stop/{self.profile_id}', headers=headers)
    def GetNameUs(self):
        name = requests.get('https://api.namefake.com/').json()['name']
        return name
    def GetEmail(self):
        mail = requests.get('https://api.namefake.com/').json()['email_u']
        return mail+'@gmail.com'
    def GetPhone(self):
        return f'+1{randint(111111111,999999999)}'
    def OpenChrome(self,profile_id):
        try:
            headers = {
                'accept': 'application/json',
            }
            params = {
                'profile_id': int(profile_id),
                #'remote_debug_port': port,
            }
            response = requests.get('http://localhost:35353/open', params=params, headers=headers).json()
            #print(response)
            return response
        except:
            return False
    def GetAuthencation(self,authencation):
        headers = {
            'authority': '2fa.live',
            'accept': '*/*',
            'accept-language': 'vi,en;q=0.9,vi-VN;q=0.8,fr-FR;q=0.7,fr;q=0.6,en-US;q=0.5',
            'referer': 'https://2fa.live/',
            'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }
        if ' ' in authencation:
            authencation = authencation.replace(' ','')
        response = requests.get(f'https://2fa.live/tok/{authencation}',headers=headers).json()
        return response['token']
    def checkurl(self):
        self.sign.emit('CHECK URL',2,self.r)
        self.driver.get('https://mbasic.facebook.com/')
        while True:
            try:
                if self.driver.find_element(By.ID,'email'):
                    return 'nologin'
            except:pass
            try:
                if self.driver.find_element('xpath','/html/body/div[1]/div/div[2]/div/div[1]/div[2]/div/a'):
                    return True
                #if self.driver.find_element('xpath','/html/body/div[1]/div/div[2]/div/div[1]/div[2]/div/a')
            except:pass
            try:
                if 'https://mbasic.facebook.com/login.php?next=https%3A%2F%2Fmbasic.facebook.com%2F&refsrc=deprecated&_rdr' in self.driver.current_url:
                    return 'block'
            except:pass
            try:#u_0_1_KP
                if 'forced_account_switch' in self.driver.current_url:
                    if self.driver.find_element('xpath','/html/body/div[1]/div[2]/div[1]/form/div/div[3]/div/div[1]/label/input'):
                        sleep(2)
                        self.driver.find_element('xpath','/html/body/div[1]/div[2]/div[1]/form/div/div[3]/div/div[1]/label/input').click()
                        sleep(2)
                        return True
            except:pass
            try:#u_0_1_KP
                if 'forced_account_switch' in self.driver.current_url:
                    if self.driver.find_element(By.ID,'u_0_1_KP'):
                        self.driver.find_element(By.ID,'u_0_1_KP').click()
                        sleep(2)
                        return True
            except:pass
            try:
                if 'forced_account_switch' in self.driver.current_url:
                    if self.driver.find_element(By.ID,'u_0_0_SI'):
                        self.driver.find_element(By.ID,'u_0_0_SI').click()
                        sleep(2)
                        return True
            except:pass
            try:
                if 'forced_account_switch' in self.driver.current_url:
                    if self.driver.find_element(By.ID,'u_0_1_4N'):
                        self.driver.find_element(By.ID,'u_0_1_4N').click()
                        sleep(2)
                        break
            except:pass
            try:
                if 'cookie/consent_prompt' in self.driver.current_url:
                    try:
                        self.driver.find_element('xpath','/html/body/div/div/div/div/table/tbody/tr/td/div/div[4]/form/div/button[2]').click()
                    except:
                        pass
            except:
                pass
            try:
                if self.driver.find_element('xpath','/html/body/div[1]/div/div[2]/div/div[1]/div[2]/div/a'):
                    return True
            except:pass
            if 'checkpoint' in self.driver.current_url:
                return 'checkpoint'
            if 'gettingstarted' in self.driver.current_url:
                self.sign.emit('LOOP NEXT',2,self.r)
                try:
                    self.driver.find_element('xpath','/html/body/div/div/div/div/div[1]/table/tbody/tr/td[3]/a').click()
                except:pass
                try:
                    self.driver.find_element('xpath','/html/body/div/div/div/div/div[2]/table/tbody/tr/td[3]/a').click()
                except:pass
                try:
                    self.driver.find_element('xpath','/html/body/div/div/div/div/div[1]/table/tbody/tr/td[3]').click()
                except:
                    try:
                        self.driver.find_element('xpath','/html/body/div/div/div/div/div[1]/table/tbody/tr/td[3]/a').click()
                    except:
                        pass
            try:
                if self.driver.find_element('xpath','/html/body/div/div/div[1]/div/form/table/tbody/tr/td[2]/input'):
                    return True
            except:pass
            try:
                if self.driver.find_element(By.ID,'m_login_email'):
                    return 'nologin'
            except:pass
    def checkprofile(self,r):
        try:
            headers = {
                'accept': 'application/json',
            }
            getprofile = requests.get(f'http://localhost:35353/profiles/{r}', headers=headers).json()['embedded_proxy']
            self.proxies = {'https':f"http://{getprofile['user_name']}:{getprofile['password']}@{getprofile['host']}:{getprofile['port']}"}
            self.sign.emit(f'{self.proxies}',2,self.r)
        except:pass
    def addproxies(self):
        try:
            self.sign.emit('Add proxy',2,self.r)
            #listpro=open(os.path.join(os.getcwd(),'data', 'proxies.txt')).read().split('\n')
            headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            }
            json_data = {
            'proxy': {
            'name': str(self.pro.split(':')[2]+':'+self.pro.split(':')[3]),
            'proxy_type': 'HTTPS',
            'host': self.pro.split(':')[0],
            'port': int(self.pro.split(':')[1]),
            'user_name': self.pro.split(':')[2],
            'password': self.pro.split(':')[3],
            },
            'profileIds': [
            f'{self.profile_id}',
            ],
            }
            self.proxies = {'https':f"http://{self.pro.split(':')[2]}:{self.pro.split(':')[3]}@{self.pro.split(':')[0]}:{self.pro.split(':')[1]}"}
            r = requests.put('http://localhost:35353/profiles/embedded-proxy', headers=headers, json=json_data).json()
            #print(r)
            try:
                if r['error']==True:
                    self.sign.emit('Proxy lỗi',2,self.r)
                    self.sign2.emit(1,1,self.r)
                    return
            except:pass
        except:pass
    def profile_picture_set(self,path):
        try:
            headerspro5={

            }
            existing_photo_id=json.loads(requests.post(F'https://www.facebook.com/profile/picture/upload/?profile_id={self.userid}&photo_source=57&av={self.userid}&__user={self.pageid}&__a=1&fb_dtsg={self.fb_dtsg}&jazoest={self.jazoest}&lsd={self.lsd}',
            files={'file': open(path, 'rb')},
            headers=headerspro5).text.replace('for (;;);', ''))['payload']['fbid']
            data={'av': self.userid,
            '__user': self.pageid,
            '__a': '1',
            'fb_dtsg': self.fb_dtsg,
            'jazoest': self.jazoest,
            'lsd': self.lsd,
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'ProfileCometProfilePictureSetMutation',
            'variables': '{"input":{"caption":"","existing_photo_id":"'+existing_photo_id+
            '","expiration_time":null,"profile_id":"'+self.userid+
            '","profile_pic_method":"EXISTING","profile_pic_source":"TIMELINE","scaled_crop_rect":{"height":1,"width":1,"x":0,"y":0},"skip_cropping":true,"actor_id":"'+self.userid+
            '","client_mutation_id":"1"},"isPage":false,"isProfile":true,"scale":1}',
            'server_timestamps': 'true',
            'doc_id': '5561533613964118',
            }
            response=requests.post(F'https://www.facebook.com/api/graphql/', headers=headerspro5)
            if 'profilePhoto' in json.loads(response.text.splitlines()[0])['data']['profile_picture_set']['profile']:
                return True
            else:
                return False
        except:
            return False
    def run(self):
        self.checkprofile(self.profile_id)
        sleep(0.5)
        options = webdriver.ChromeOptions()
        #port = randint(3000, 5000)
        self.sign.emit('Bật chrome',2,self.r)
        res = self.OpenChrome(self.profile_id)
        #print(res)
        if res == False:
            self.sign.emit('ko mo duoc chrome',2,self.r)
            try:
                self.closechrome()
                sleep(2)
            except:pass
            self.sign2.emit(1,1,self.r)
            return
        else:
            try:
                options.binary_location = res['browser_location']
                options.debugger_address = res['remote_debug_address']
            except:
                self.sign.emit('ko mo duoc chrome',2,self.r)
                try:
                    self.closechrome()
                    sleep(2)
                except:pass
                self.sign2.emit(1,1,self.r)
                return
        chrome_service = ChromeService()
        chrome_service.creationflags = CREATE_NO_WINDOW
        self.driver = webdriver.Chrome(service=chrome_service,options=options)
        self.user_agent = self.driver.execute_script('return navigator.userAgent')
        sleep(1)
        try:
            self.driver.set_window_size(1000, 1000)
        except:pass
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.get('https://www.facebook.com/')
        checklogin=self.checkurl()
        if checklogin==False:
            self.sign.emit('Tài khoản checkpoint',2,self.r)
            self.closechrome()
            sleep(2)
            self.sign2.emit(1,1,self.r)
            return
        elif checklogin=='checkpoint':
            self.sign.emit('Tài khoản checkpoint',2,self.r)
            self.closechrome()
            sleep(2)
            self.sign2.emit(1,1,self.r)
            return
        elif checklogin=='block':
            self.sign.emit('Tài khoản bị block',2,self.r)
            self.closechrome()
            sleep(2)
            self.sign2.emit(1,1,self.r)
            return
        elif checklogin=='nologin':
            self.sign.emit('Tài khoản chưa đăng nhập',2,self.r)
            if self.loged:
                k=self.loginwithck()
            else:
                k=self.loginwithpass()
            if k==True:
                self.startmisson()
            elif k=='block':
                self.sign.emit('Tài khoản bị block',2,self.r)
                self.closechrome()
                sleep(2)
                self.sign2.emit(1,1,self.r)
                return
            elif k=='checkpoint':
                self.sign.emit('Tài khoản bị checkpoint',2,self.r)
                self.closechrome()
                sleep(2)
                self.sign2.emit(1,1,self.r)
                return
        elif checklogin==True:
            #self.checkprofile(self.profile_id)
            self.startmisson()
    def startmisson(self):
        self.driver.get('https://mbasic.facebook.com/')
        sleep(2)
        cookies_list=self.driver.get_cookies()
        cookieString=''
        for cookie in cookies_list[:-1]:
            cookieString = cookieString + cookie["name"] + "="+cookie["value"]+"; "
        self.cookie = cookieString
        html = self.driver.page_source
        #print(html)
        self.userid = html.split('<input type="hidden" name="target" value="')[1].split('"')[0]
        self.fb_dtsg = html.split('<input type="hidden" name="fb_dtsg" value="')[1].split('"')[0]
        self.jazoest = html.split('<input type="hidden" name="jazoest" value="')[1].split('"')[0]
        #print(self.driver.page_source)
        sleep(2)
        if self.upreeels and self.regpage:
            checkregpage=self.RegPage()
            if checkregpage==False:
                self.sign.emit('Không tạo được page',2,self.r)
                self.closechrome()
                sleep(2)
                self.sign2.emit(1,1,self.r)
                return
            elif checkregpage=='checkpoint':
                self.sign.emit('Tài khoản checkpoint',2,self.r)
                self.closechrome()
                sleep(2)
                self.sign2.emit(1,1,self.r)
                return
            elif checkregpage=='cantreg':
                self.sign.emit('Không reg được page',2,self.r)
                self.closechrome()
                sleep(2)
                self.sign2.emit(1,1,self.r)
                return
            elif checkregpage=='toomany':
                self.sign.emit('Vượt quá số page tạo 1 days',2,self.r)
                self.closechrome()
                sleep(2)
                self.sign2.emit(1,1,self.r)
                return 
            elif checkregpage==True:
                self.sign.emit('Hoàn thành',2,self.r)
                self.UpReels()
                #return
        elif self.regpage:
            checkregpage=self.RegPage()
            if checkregpage==False:
                self.sign.emit('Không tạo được page',2,self.r)
                self.closechrome()
                sleep(2)
                self.sign2.emit(1,1,self.r)
                return
            elif checkregpage=='checkpoint':
                self.sign.emit('Tài khoản checkpoint',2,self.r)
                self.closechrome()
                sleep(2)
                self.sign2.emit(1,1,self.r)
                return
            elif checkregpage=='cantreg':
                self.sign.emit('Không reg được page',2,self.r)
                self.closechrome()
                sleep(2)
                self.sign2.emit(1,1,self.r)
                return
            elif checkregpage=='toomany':
                self.sign.emit('Vượt quá số page tạo 1 days',2,self.r)
                self.closechrome()
                sleep(2)
                self.sign2.emit(1,1,self.r)
                return 
            elif checkregpage==True:
                self.sign.emit('Hoàn thành',2,self.r)
                self.closechrome()
                sleep(2)
                self.sign2.emit(1,1,self.r)
                return
        elif self.upreeels:
            self.UpReels()

    def stop(self):
        try:
            self.driver.quit()
            #sleep(2)
        except:pass
        try:
            self.closechrome()
            #sleep(2)
        except:pass
        try:
            self.terminate()
            #sleep(2)
        except:pass
    def loginwithck(self):
        listget_account=open(os.path.join(os.getcwd(), 'data','clone','logincookie.txt')).read().split('\n')
        get_account=listget_account[0]
        listget_account.remove(get_account)
        open(os.path.join(os.getcwd(), 'data','clone','logincookieuser.txt'),'a+').write("%s\n"%(get_account))
        with open(os.path.join(os.getcwd(), 'data','clone','logincookie.txt'),'w') as fp:
            for i in listget_account:
                if i !='':
                    fp.write(i+'\n')
            fp.close()
        user=get_account.split('|')[0]
        passw=get_account.split('|')[1]
        token=get_account.split('|')[2]
        cookie=get_account.split('|')[3]
        #pro=get_account.split('|')[4]
        c = cookie.replace(" ","").split(";")
        for i in c:
            if i !="":
                ck = i.split("=")
                dict_ck = {"name":ck[0],"value":ck[1],"domain":".facebook.com"}
                self.driver.add_cookie(dict_ck)
        self.driver.refresh()
        sleep(1)
        checkurllogin=self.checkurl()
        return checkurllogin
    def loginwithpass(self):
        listget_account=open(os.path.join(os.getcwd(), 'data','clone','loginuserpass.txt')).read().split('\n')
        get_account=listget_account[0]
        listget_account.remove(get_account)
        open(os.path.join(os.getcwd(), 'data','clone','loginuserpassuser.txt'),'a+').write("%s\n"%(get_account))
        with open(os.path.join(os.getcwd(), 'data','clone','loginuserpass.txt'),'w') as fp:
            for i in listget_account:
                if i !='':
                    fp.write(i+'\n')
            fp.close()
        user_name=get_account.split('|')[0]
        password=get_account.split('|')[1]
        t2fa=get_account.split('|')[2]
        #self.pro=get_account.split('|')[3]
        self.driver.get('https://mbasic.facebook.com/')
        for checklog in range(20):
            try:
                if self.driver.find_element('xpath','/html/body/div/div/div[2]/div/table/tbody/tr/td/div[2]/div/div[2]/form/ul/li[1]/input'):
                    self.sign.emit('Nhập tài khoản',2,self.r)
                    for i in user_name:
                        self.driver.find_element('xpath','/html/body/div/div/div[2]/div/table/tbody/tr/td/div[2]/div/div[2]/form/ul/li[1]/input').send_keys(i)
                        sleep(0.1)
                    sleep(0.5)
                    self.sign.emit('Nhập mật khẩu',2,self.r)
                    for i in password:
                        self.driver.find_element('xpath','/html/body/div/div/div[2]/div/table/tbody/tr/td/div[2]/div/div[2]/form/ul/li[2]/section/input').send_keys(i)
                        sleep(0.1)
                    sleep(1)
                    self.driver.find_element('xpath','/html/body/div/div/div[2]/div/table/tbody/tr/td/div[2]/div/div[2]/form/ul/li[3]/input').click()
                    sleep(2)
                    while True:
                        try:
                            if 'Blocked' in self.driver.page_source:
                                return 'block'
                        except:pass
                        try:
                            if self.driver.find_element(By.ID,'m_login_email'):
                                self.sign.emit('ko login',2,self.r)
                                return 'nologin'
                        except:pass
                        try:
                            if self.driver.find_element('xpath','/html/body/div/div/div[2]/div/form/div[1]/article/section/section[2]/div[2]/div/input'):
                                break
                        except:pass
                    try:
                        code = self.GetAuthencation(t2fa)
                        self.sign.emit('Nhập 2FA',2,self.r)
                        for i in code:
                            self.driver.find_element('xpath','/html/body/div/div/div[2]/div/form/div[1]/article/section/section[2]/div[2]/div/input').send_keys(i)
                            sleep(0.1)
                        sleep(0.5)
                        break
                    #print('INPUT AUTHENCATION CODE')
                        # try:
                        #     self.driver.find_element('xpath','/html/body/div/div/div[2]/div/form/div[1]/article/div[1]/table/tbody/tr/td/input').click()
                        #     #print('CLICK CONTINUE')
                        #     sleep(0.5)
                        #     self.driver.find_element('xpath','/html/body/div/div/div[2]/div/form/div[1]/article/div[1]/table/tbody/tr/td/input').click()
                        # except:pass
                    except:
                        pass
                    sleep(4)
            except:pass
            sleep(1)
        checkurllogin=self.checkurl()
        return checkurllogin
            # try:
            #     if self.driver.find_element('xpath','/html/body/div/div/div[2]/div/div[2]/div/div/form/table/tbody/tr/td[1]/input'):
            #         #print('go to mbasic2')
            #         break
            # except:pass
            
    def Reg(self,categories,name):
        headers = {
            'authority': 'www.facebook.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': self.cookie,
            'origin': 'https://www.facebook.com',
            'referer': 'https://www.facebook.com/pages/creation/?ref_type=launch_point',
            'sec-ch-prefers-color-scheme': 'dark',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.user_agent,
            'viewport-width': '1127',
            'x-fb-friendly-name': 'AdditionalProfilePlusCreationMutation',
            # 'x-fb-lsd': '2a1idzeftf-oCsLPBKMmO6',
        }

        data = {
            'av': self.userid,
            '__user': self.userid,
            '__a': '1',
            '__ccg': 'EXCELLENT',
            '__comet_req': '15',
            'fb_dtsg': self.fb_dtsg,
            'jazoest': self.jazoest,
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'AdditionalProfilePlusCreationMutation',
            'variables': '{"input":{"bio":"","categories":["'+categories+'"],"creation_source":"comet","name":"'+name+'","page_referrer":"launch_point","actor_id":"'+self.userid+'","client_mutation_id":"'+str(3*(random.randint(1,4)))+'"}}',
            'server_timestamps': 'true',
            'doc_id': '5903223909690825',
        }
        try:
            reg = requests.post('https://www.facebook.com/api/graphql/',headers=headers, data=data,proxies=self.proxies).json()
            print(categories,name,reg)
            try:
                self.pageid = reg['data']['additional_profile_plus_create']['additional_profile']['id']
                return self.pageid
            except:
                try:
                    t = reg['data']['additional_profile_plus_create']['error_message']
                    return t#reg['data']['additional_profile_plus_create']['error_message']
                except:
                    return reg['errors'][0]['message']
        except:
            pass
    def Regwithselenium(self,name):
        self.driver.get('https://www.facebook.com/pages/creation/?ref_type=launch_point')
        sleep(5)
        # NHAP TEN
        while True:
            self.sign.emit(f'NamePage: {name}',2,self.r)
            try:
                self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div[1]/div/label/div/div/input').send_keys(name)
                break
            except:
                pass
            try:
                self.driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div[5]/div/div/div[3]/div[2]/div[1]/div/div[3]/div[1]/div[2]/div/div/div/div[1]/div/label/div/div/input').send_keys(name)
                break
            except:
                pass
            try:
                self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div[1]/div/label/div/div/input').send_keys(name)
                break
            except:
                pass
        #
        #NHAP CATORY
        while True:
            #self.sign.emit('Tiếp tục',2,self.r)
            try:
                self.driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div[5]/div/div/div[3]/div[2]/div[1]/div/div[3]/div[1]/div[2]/div/div/div/div[3]/div/div/div/div/label/div/div/div/input').send_keys('A')
                sleep(0.5)
                self.driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div[5]/div/div/div[4]/div/div/div[1]/div[1]/div/div[1]/div/ul/li[1]/div/div[1]/div').click()
                break
            except:
                pass
            try:
                self.driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div[5]/div/div/div[3]/div[2]/div[1]/div/div[3]/div[1]/div[2]/div/div/div/div[3]/div/div/div/div/label/div/div/div/input').send_keys('A')
                sleep(0.5)
                self.driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div[5]/div/div/div[4]/div/div/div[1]/div[1]/div/div[1]/div/ul/li[1]/div/div[1]').click()
                break
            except:
                pass
            try:
                self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div[3]/div/div/div/div/label/div/div/div/input').send_keys('A')
                sleep(0.5)
                self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[1]/div/div[1]/div/ul/li[1]/div/div[1]').click()
                break
            except:
                pass#
            try:
                self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div[3]/div/div/div/div/label/div/div/div/input').send_keys('A')
                sleep(0.5)
                self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[2]/div/div/div[1]/div[1]/div/div[1]/div/ul/li[1]/div/div[1]/div/div/div/div/span').click()
                break
            except:
                pass
        #CONTINUE
        while True:
            self.sign.emit('Tiếp tục',2,self.r)
            try:
                self.driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div[5]/div/div/div[3]/div[2]/div[1]/div/div[4]/div[1]/div/div').click()
                sleep(1.5)
                #print('ctn 1')
                break
            except:
                pass
            try:
                self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[1]/div/div[3]/div[1]/div/div').click()
                sleep(1.5)
                #print('ctn 1')
                break
            except:
                pass
            try:
                self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[1]/div/div[3]/div[2]/div[2]/div').click()
                sleep(1.5)
                #print('ctn 1')
                break
            except:
                pass#
            try:
                self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div[1]/div/div[3]/div[1]/div/div').click()
                sleep(1.5)
                #print('ctn 1')
                break
            except:
                pass#
        #CONTINUE 2
        while True:
            self.sign.emit('Tiếp tục',2,self.r)
            try:
                if self.driver.find_element('xpath','/html/body/div[4]/ul/li/div[1]/div/div[2]/span/span'):
                    return 'toomany'
            except:pass
            try:
                self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[1]/div/div[4]/div[2]/div[2]/div').click()
                sleep(1.5)
                #print('ctn 2')
                break
            except:
                pass
            try:
                self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[1]/div/div[3]/div[2]/div[2]/div').click()
                sleep(1.5)
                #print('ctn 2')
                break
            except:
                pass
            try:
                self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div[1]/div/div[3]/div[2]/div[2]/div').click()
                sleep(1.5)
                #print('ctn 2')
                break
            except:
                pass
        
        #CONTINUE 3
        while True:
            self.sign.emit('Tiếp tục',2,self.r)
            try:
                self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[1]/div/div[3]/div[2]/div[2]/div').click()
                sleep(1.5)
                #print('ctn 3')
                break
            except:
                pass
            try:
                self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div[1]/div/div[3]/div[2]/div[2]/div').click()
                sleep(1.5)
                #print('ctn 3')
                break
            except:
                pass
        #CONTINUE 4
        while True:
            self.sign.emit('Tiếp tục',2,self.r)
            try:
                self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[1]/div/div[3]/div[2]/div[2]/div').click()
                sleep(1.5)
                #print('ctn 4')
                break
            except:
                pass
            try:
                self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div[1]/div/div[3]/div[2]/div[2]/div').click()
                sleep(1.5)
                #print('ctn 4')
                break
            except:
                pass

        #CONTINUE 5
        while True:
            self.sign.emit('Tiếp tục',2,self.r)
            try:
                self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[1]/div/div[3]/div[2]/div[2]/div').click()
                sleep(1.5)
                #print('ctn 5')
                break
            except:
                pass
            try:
                self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div[1]/div/div[3]/div[2]/div[2]/div').click()
                sleep(1.5)
                #print('ctn 5')
                break
            except:
                pass
        
        #CONTINUE 6
        while True:
            self.sign.emit('Tiếp tục',2,self.r)
            try:
                self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[1]/div/div[3]/div[2]/div[2]/div').click()
                sleep(1.5)
                #print('ctn 6')
                break
            except:
                pass
            try:
                self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div[1]/div/div[3]/div[2]/div[2]/div').click()
                sleep(1.5)
                ##print('ctn 5')
                break
            except:
                pass
        while True:
            try:
                if 'profile.php?id=' in self.driver.current_url:
                    self.sign.emit('Tạo page thành công',2,self.r)
                    self.pageid = self.driver.current_url.split('profile.php?id=')[1]
                    return self.pageid
            except:pass
    def changephone(self,phone,collectionToken,sectionToken):
        self.sign.emit('Cập nhật số điện thoại!', 2, self.r)
        headers = {
            'authority': 'www.facebook.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': self.cookie_pro5,
            'origin': 'https://www.facebook.com',
            'referer': f'https://www.facebook.com/profile.php?id={self.pageid}&sk=about_contact_and_basic_info',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.user_agent,
            'viewport-width': '1127',
            'x-fb-friendly-name': 'ProfileCometPublicPhoneNumberProfileFieldSaveMutation',
        }
        data = {
            'av': self.pageid,
            '__user': self.pageid,
            'fb_dtsg': self.fb_dtsg,
            'jazoest': self.jazoest,
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'ProfileCometPublicPhoneNumberProfileFieldSaveMutation',
            'variables': '{"collectionToken":"'+collectionToken+'","input":{"phone_number":"tel:'+phone+'","actor_id":"'+self.pageid+'","client_mutation_id":"4"},"scale":1,"sectionToken":"'+sectionToken+'"}',
            'server_timestamps': 'true',
            'doc_id': '5969514689761163',
        }
        setphone = requests.post('https://www.facebook.com/api/graphql/', headers=headers, data=data,proxies=self.proxies)
        #print(setphone.text)
        
    def changeaddress(self,address,zipcode,list_city_id,collectionToken,sectionToken):
        self.sign.emit('Cập nhật địa chỉ!', 2, self.r)
        headers2 = {
            'authority': 'www.facebook.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': self.cookie_pro5,
            'origin': 'https://www.facebook.com',
            'referer': f'https://www.facebook.com/profile.php?id={self.pageid}&sk=about_contact_and_basic_info',
            'sec-ch-prefers-color-scheme': 'light',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.user_agent,#'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.4958.1 Safari/537.36',
            'viewport-width': '1127',
            'x-fb-friendly-name': 'ProfileCometAddressSaveMutation',
        }
        dataaddress = {
            'av': self.pageid,
            '__user': self.pageid,
            '__a': '1',
            '__comet_req': '15',
            'fb_dtsg': self.fb_dtsg,
            'jazoest': self.jazoest,
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'ProfileCometAddressSaveMutation',
            'variables': '{"collectionToken":"'+collectionToken+'","input":{"city_id":"'+random.choice(list_city_id)+'","neighborhood":"","privacy":{"allow":[],"base_state":"EVERYONE","deny":[],"tag_expansion_state":"UNSPECIFIED"},"street_address":"'+address+'","zip":"'+zipcode+'","actor_id":"'+self.pageid+'","client_mutation_id":"2"},"scale":1,"sectionToken":"'+sectionToken+'"}',
            'server_timestamps': 'true',
            'doc_id': '6397656753583281',
        }
        setaddress = requests.post('https://www.facebook.com/api/graphql/', headers=headers2, data=dataaddress,proxies=self.proxies)
        #print(setaddress.text)
        
    def cheangeemail(self,email,collectionToken,sectionToken):
        self.sign.emit('Cập nhật email', 2, self.r)
        headers3 = {
            'authority': 'www.facebook.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': self.cookie_pro5,
            'origin': 'https://www.facebook.com',
            'referer': f'https://www.facebook.com/profile.php?id={self.pageid}&sk=about_contact_and_basic_info',
            'sec-ch-prefers-color-scheme': 'light',
            #'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.user_agent,#'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.4958.1 Safari/537.36',
            'viewport-width': '932',
            'x-fb-friendly-name': 'ProfileCometPublicEmailAddressProfileFieldSaveMutation',
        }
        dataemail = {
            'av': self.pageid,
            '__user': self.pageid,
            '__a': '1',
            '__comet_req': '15',
            'fb_dtsg': self.fb_dtsg,#'NAcMsG7reUrbL__4XKofdMlBFe-4GHvf_50PHyFpbpS04FDiRKDr5rg:9:1673039511',
            'jazoest': self.jazoest,#'25333',
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'ProfileCometPublicEmailAddressProfileFieldSaveMutation',
            #'variables': '{"collectionToken":"'+collectionToken+'","input":{"email_address":"'+'123123@gmail.com'+',"actor_id":"'+pageid+'","client_mutation_id":"1"},"scale":1,"sectionToken":"'+sectionToken+'"}',
            'variables': '{"collectionToken":"'+collectionToken+'","input":{"email_address":"'+email+'","actor_id":"'+self.pageid+'","client_mutation_id":"1"},"scale":1,"sectionToken":"'+sectionToken+'"}',
            'server_timestamps': 'true',
            'doc_id': '5978839192160543',
        }
        response = requests.post('https://www.facebook.com/api/graphql/', headers=headers3, data=dataemail,proxies=self.proxies)
        #print(response.text)
        
    def get_token(self):
        headers = {
            'authority': 'www.facebook.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': self.cookie_pro5,#'sb=mgS0Y2e1Z-i63rI5nm0V81FQ; datr=mgS0Y63cQzY-KaySOX2ph4vP; locale=fr_FR; c_user=100011053006549; xs=37%3A5gpies3EgzDVnA%3A2%3A1673033899%3A-1%3A9883; oo=v1%7C3%3A1673033901; m_page_voice=100011053006549; i_user=100089497651464; usida=eyJ2ZXIiOjEsImlkIjoiQXJvMnhvY2Rpa3FhciIsInRpbWUiOjE2NzMwMzQ0OTJ9; wd=783x979',
            'sec-ch-prefers-color-scheme': 'light',
            #'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': self.user_agent,#'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.23 Safari/537.36',
            'viewport-width': '1920',
        }
        params = {
            'id':self.pageid,
            'sk': 'about_contact_and_basic_info',
        }
        r_info = requests.get('https://www.facebook.com/profile.php', params=params, headers=headers,proxies=self.proxies).text
        sectionToken=r_info.split('"sectionToken":"')[1].split('"')[0]
        collectionToken=r_info.split('"collectionToken":"')[1].split('"')[0]
        return sectionToken,collectionToken
    def ChangeCategory(self,collectionToken,sectionToken,category_id):
        headers = {
            'authority': 'www.facebook.com',
            'accept': '/',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': self.cookie,
            'origin': 'https://www.facebook.com',
            'referer': f'https://www.facebook.com/profile.php?id={self.pageid}&sk=about_contact_and_basic_info',
            'sec-ch-prefers-color-scheme': 'dark',
            #'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': self.user_agent,#'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.144 Safari/537.36',
            'viewport-width': '1343',
            'x-fb-friendly-name': 'ProfileCometCategoryProfileFieldSaveMutation',
        }

        data = {
            'av': self.pageid,
            '__user': self.pageid,
            'fb_dtsg': self.fb_dtsg,
            'jazoest': self.jazoest,
            'fb_api_caller_class': 'RelayModern',
            'fb_api_req_friendly_name': 'ProfileCometCategoryProfileFieldSaveMutation',
            'variables': '{"collectionToken":"'+collectionToken+'","input":{"category_id":"'+category_id+'","actor_id":"'+self.pageid+'","client_mutation_id":"1"},"scale":1,"sectionToken":"'+sectionToken+'"}',
            'server_timestamps': 'true',
            'doc_id': '6067076286670486',
        }
        change = requests.post('https://www.facebook.com/api/graphql/', headers=headers, data=data)
    def switchpage(self,idpage):
        kl=0
        while True:
            try:
                if 'checkpoint' in self.driver.current_url:
                    return 'checkpoint'
            except:pass
            try:
                if f'actorID":"{idpage}' in self.driver.page_source:
                    self.sign.emit('Switch Success',2,self.r)
                    return True
            except:pass
            if kl ==60:
                self.sign.emit('không nhận diện được',2,self.r)
                self.closechrome()
                sleep(2)
                return False
            try:
                if self.driver.find_element('xpath','/html/body/div[4]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]'):
                    sleep(1)
                    self.driver.find_element('xpath','/html/body/div[4]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]').click()
                    #self.driver.find_element('xpath','/html/body/div[4]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]').click()
                    sleep(1)
            except:pass
            try:
                if self.driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div[1]/div/div/div/div/div/div/div/div[2]/div/div'):
                    self.driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div[1]/div/div/div/div/div/div/div/div[2]/div/div').click()
                    self.driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div[1]/div/div/div/div/div/div/div/div[2]/div/div').click()
                    sleep(0.5)
            except:pass
            try:
                if self.driver.find_element('xpath','/html/body/div[5]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]/div/div[1]/div/span/span'):
                    self.driver.find_element('xpath','/html/body/div[5]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]/div/div[1]/div/span/span').click()
                    sleep(0.1)
                    self.driver.find_element('xpath','/html/body/div[5]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]/div/div[1]/div/span/span').click()
            except:pass
            try:
                if self.driver.find_element('xpath','/html/body/div[5]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]'):
                    self.driver.find_element('xpath','/html/body/div[5]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]').click()
                    self.driver.find_element('xpath','/html/body/div[5]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]').click()
            except:pass
            try:
                if self.driver.find_element('xpath','/html/body/div[5]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]/div'):
                    self.driver.find_element('xpath','/html/body/div[5]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]/div').click()
                    self.driver.find_element('xpath','/html/body/div[5]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]/div').click()
            except:pass       
            try:
                if self.driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[4]/div[1]/div/div/div/div/div/div/div/div[2]/div/div'):
                    self.driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[4]/div[1]/div/div/div/div/div/div/div/div[2]/div/div').click()
                    self.driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[4]/div[1]/div/div/div/div/div/div/div/div[2]/div/div').click()
            except:
                try:
                    if self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[4]/div[1]/div/div/div/div/div/div/div/div[2]/div/div/div/div[1]/div/span/span'):
                        self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[4]/div[1]/div/div/div/div/div/div/div/div[2]/div/div/div/div[1]/div/span/span').click()
                        self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[4]/div[1]/div/div/div/div/div/div/div/div[2]/div/div/div/div[1]/div/span/span').click()
                except:
                    try:
                        if self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[1]/div/div/div/div/div/div/div/div[2]/div/div'):
                            self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[1]/div/div/div/div/div/div/div/div[2]/div/div').click()
                            self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[1]/div/div/div/div/div/div/div/div[2]/div/div').click()
                    except:pass
    def RegPage(self):
        #proxies = self.proxies
        numpage=0
        while True:
            if numpage==self.threadpage:
                sleep(0.5)
                open(os.path.join(os.getcwd(), 'data','successrepage.txt'),'a+').write("%s|%s|%s\n"%(self.userid,'Success',self.link))
                return True
            try:
                self.driver.get('https://mbasic.facebook.com')
                self.sign.emit('Load facebook',2,self.r)
                for checkcon in range(20):
                    # try:
                    #     if self.driver.find_element(By.ID,'m_login_email'):
                    #         self.closechrome()
                    #         sleep(2)
                    #         return 'nologin'
                    # except:pass
                    try:
                        if self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[6]/div/div/div[1]/div/div[2]/div/div/div/div[2]/div/div[4]/div'):
                            self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[6]/div/div/div[1]/div/div[2]/div/div/div/div[2]/div/div[4]/div').click()
                            sleep(2)
                    except:pass

                    try:
                        if self.driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[1]/form/div/div[3]/div/div[1]/label'):
                            self.driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[1]/form/div/div[3]/div/div[1]/label').click()
                    except:pass
                    try:
                        if self.driver.find_element(By.XPATH,'/html/body/div/div/div[1]/div/form/table/tbody/tr/td[2]/input'):
                            cookies_list=self.driver.get_cookies()
                            cookieString=''
                            for cookie in cookies_list[:-1]:
                                cookieString = cookieString + cookie["name"] + "="+cookie["value"]+"; "
                            self.cookie = cookieString
                            html = self.driver.page_source
                            self.userid = html.split('<input type="hidden" name="target" value="')[1].split('"')[0]
                            self.fb_dtsg = html.split('<input type="hidden" name="fb_dtsg" value="')[1].split('"')[0]
                            self.jazoest = html.split('<input type="hidden" name="jazoest" value="')[1].split('"')[0]
                            break
                    except:pass
                    try:
                        if self.driver.find_element('xpath','/html/body/div[1]/div/div[2]/div/div[1]/div[2]/div/a'):
                            cookies_list=self.driver.get_cookies()
                            cookieString=''
                            for cookie in cookies_list[:-1]:
                                cookieString = cookieString + cookie["name"] + "="+cookie["value"]+"; "
                            self.cookie = cookieString
                            html = self.driver.page_source
                            self.userid = html.split('<input type="hidden" name="target" value="')[1].split('"')[0]
                            self.fb_dtsg = html.split('<input type="hidden" name="fb_dtsg" value="')[1].split('"')[0]
                            self.jazoest = html.split('<input type="hidden" name="jazoest" value="')[1].split('"')[0]
                            break
                    except:pass
                    sleep(1)
                sleep(2)
                self.sign.emit('Bắt đầu reg page',2,self.r)
                while True:
                    name=random.choice(open(os.path.join(os.getcwd(),'data','profileaccount','ten_kenh.txt')).read().split('\n'))
                    if name!='':
                        break
                    else:
                        name=random.choice(open(os.path.join(os.getcwd(),'data','profileaccount','ten_kenh.txt')).read().split('\n'))
                
                list_categories = ['1548916632084224','2233','109578329118821']
                categories=random.choice(list_categories)
                self.sign.emit(f'Bắt đầu reg page {numpage+1}',2,self.r)
                #setreg=self.Reg(categories,name)
                setreg=self.Regwithselenium(name)
                if setreg =='toomany':
                    if numpage==0:
                        open(os.path.join(os.getcwd(), 'data','failregpage.txt'),'a+').write("%s|%s\n"%(self.userid,'Fail'))
                    else:
                        open(os.path.join(os.getcwd(), 'data','regover.txt'),'a+').write("%s|%s|%s\n"%(self.userid,'FailOver',self.link))
                    self.closechrome()
                    sleep(2)
                    return 'toomany'
                elif setreg == 'servererror':
                    return 'cantreg'
                else:
                    self.sign.emit(f'PageID: {setreg}',2,self.r)
                #print(setreg)
                self.driver.get(f'https://www.facebook.com/profile.php?id={self.pageid}')
                sleep(5)
                self.link+=self.driver.current_url+'|'
                #print(self.link)
                try:
                    if self.driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div[1]/div/div/div/div/div/div/div/div[2]/div/div'):
                        #sl
                        self.driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div[1]/div/div/div/div/div/div/div/div[2]/div/div').click()
                        break
                except:pass
                # try:
                #     m=self.driver.switch_to.alert.dismiss()
                # except:pass
                self.sign.emit(f'Chuyển đổi sang page {self.pageid}',2,self.r)
                chswitchpage=self.switchpage(self.pageid)
                if chswitchpage:
                    pass
                elif chswitchpage=='checkpoint':
                    return chswitchpage
                else:
                    return chswitchpage
                    #sleep(0.2)
                #path=os.path.join(os.getcwd(),'avarta',random.choice(os.listdir(os.path.join(os.getcwd(),'avarta'))))
                checkupimg=0
                timenew=0
                while True:
                    if checkupimg==1:
                        if timenew == 30:
                            self.sign.emit('refresh page',2,self.r)
                            self.driver.refresh()
                            timenew=0
                            checkupimg=0
                        else:
                            timenew+=1
                            self.sign.emit(f'Chờ {timenew}s',2,self.r)
                    try:
                        if self.driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[2]/div/div[4]/div'):
                            self.driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[2]/div/div[4]/div').click()
                    except:pass
                    try:
                        if self.driver.find_element('xpath','/html/body/div[4]/ul/li/div[1]/div/div/div[1]/div/div[2]'):
                            self.driver.find_element('xpath','/html/body/div[4]/ul/li/div[1]/div/div/div[1]/div/div[2]').click()
                    except:pass
                    try:
                        if self.driver.find_element('xpath','/html/body/div[6]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]'):
                            self.driver.find_element('xpath','/html/body/div[6]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]').click()
                            sleep(1)
                    except:pass
                    try:
                        if self.driver.find_element('xpath','/html/body/div[2]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]/div/div[1]/div/span/span'):
                            self.driver.find_element('xpath','/html/body/div[2]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]/div/div[1]/div/span/span').click()
                            sleep(2)
                    except:pass
                    try:
                        if self.driver.find_element('xpath','/html/body/div[3]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]/div/div[1]/div/span/span'):
                            self.driver.find_element('xpath','/html/body/div[3]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]/div/div[1]/div/span/span').click()
                            sleep(2)
                    except:pass
                    try:
                        if self.driver.find_element('xpath','/html/body/div[2]/div[1]/div/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div/div[1]/div/span/span'):
                            self.driver.find_element('xpath','/html/body/div[2]/div[1]/div/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div/div[1]/div/span/span').click()
                            sleep(2)
                    except:pass
                    try:
                        if self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[1]/div[2]/div/div/div/div[1]/div/div/div/div[2]/div/div[2]'):
                            self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[1]/div[2]/div/div/div/div[1]/div/div/div/div[2]/div/div[2]').click()
                            sleep(2)
                    except:pass
                    try:
                        self.driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[1]/div[2]/div/div/div/div[1]/div/div/div/div[2]/div/div[2]').click()
                    except:pass
                    try:
                        self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[6]/div/div/div[1]/div/div[2]/div/div/div/div[2]/div/div[4]/div').click()
                    except:pass
                    sleep(4)
                    if checkupimg==0:
                        try:
                            if self.driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[3]/div[1]/div/div[1]/input'):
                                path=os.path.join(os.getcwd(),'avarta',random.choice(os.listdir(os.path.join(os.getcwd(),'avarta'))))
                                self.sign.emit('Up ảnh',2,self.r)
                                checkupimg=1
                                self.driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[3]/div[1]/div/div[1]/input').send_keys(path)
                                sleep(5)
                        except:pass

                        try:
                            if self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[6]/div/div/div[1]/div/div[2]/div/div/div/div[3]/div[1]/div[1]/input'):
                                path=os.path.join(os.getcwd(),'avarta',random.choice(os.listdir(os.path.join(os.getcwd(),'avarta'))))
                                self.sign.emit('Up ảnh',2,self.r)
                                checkupimg=1
                                self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[6]/div/div/div[1]/div/div[2]/div/div/div/div[3]/div[1]/div[1]/input').send_keys(path)
                                sleep(5)
                        except:pass
                        
                        try:
                            if self.driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[3]/div[1]/div[1]/input'):
                                path=os.path.join(os.getcwd(),'avarta',random.choice(os.listdir(os.path.join(os.getcwd(),'avarta'))))
                                self.sign.emit('Up ảnh',2,self.r)
                                checkupimg=1
                                self.driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[3]/div[1]/div[1]/input').send_keys(path)
                                sleep(5)
                        except:pass
                        try:
                            if self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[6]/div/div/div[1]/div/div[2]/div/div/div/div[3]/div[1]/div/div[1]/input'):
                                path=os.path.join(os.getcwd(),'avarta',random.choice(os.listdir(os.path.join(os.getcwd(),'avarta'))))
                                self.sign.emit('Up ảnh',2,self.r)
                                checkupimg=1
                                self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[6]/div/div/div[1]/div/div[2]/div/div/div/div[3]/div[1]/div/div[1]/input').send_keys(path)
                                sleep(5)
                        except:pass
                    try:
                        if self.driver.find_element('xpath','/html/body/div[5]/div[1]/div/div[2]/div/div/div/div[1]/div'):
                            self.driver.find_element('xpath','/html/body/div[5]/div[1]/div/div[2]/div/div/div/div[1]/div').click()
                            sleep(1)
                    except:pass
                    try:
                        if self.driver.find_element('xpath','/html/body/div[4]/div[1]/div/div[2]/div/div/div/div[1]/div'):
                            self.driver.find_element('xpath','/html/body/div[4]/div[1]/div/div[2]/div/div/div/div[1]/div').click()
                            sleep(1)
                    except:pass
                    #/html/body/div[4]/div[1]/div/div[2]/div/div/div/div[1]/div
                    #except:pass
                    try:
                        self.driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[3]/div[5]/div[2]/div').click()
                        sleep(10)
                        self.sign.emit('Up ảnh xong',2,self.r)
                        break
                    except:pass
                    try:
                        self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[6]/div/div/div[1]/div/div[2]/div/div/div/div[3]/div[5]/div[2]/div').click()
                        sleep(10)
                        self.sign.emit('Up ảnh xong',2,self.r)
                        break
                    except:pass
                    sleep(0.2)
                
                sleep(1)
                #print(self.pageid)
                #self.driver.get(f'https://www.facebook.com/profile.php?id={self.pageid}&sk=about_contact_and_basic_info')
                self.driver.execute_script('window.location.replace("https://www.facebook.com/profile.php?id='+self.pageid+'&sk=about_contact_and_basic_info");')
                #('to')
                #sleep(5)
                clickpage=0
                while True:
                    if clickpage==0:
                        try:
                            if self.driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[2]/div/div[4]/div'):
                                self.driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[2]/div/div[4]/div').click()
                                sleep(2)
                                clickpage=1
                        except:pass
                        try:
                            if self.driver.find_element('xpath','/html/body/div[3]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]'):
                                sleep(1)
                                self.driver.find_element('xpath','/html/body/div[3]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]').click()
                                sleep(2)
                                clickpage=1
                        except:pass
                        try:
                            if self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[6]/div/div/div[1]/div/div[2]/div/div/div/div[2]/div/div[4]/div'):
                                sleep(1)
                                self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[6]/div/div/div[1]/div/div[2]/div/div/div/div[2]/div/div[4]/div').click()
                                sleep(1)
                                clickpage=1
                        except:pass
                        try:
                            if self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[1]/div[1]/h2/span'):
                                #self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[1]/div[1]/h2/span'):
                                sleep(1)
                                clickpage=1
                        except:pass
                        try:
                            if self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[1]/div[1]/h2/span/a'):
                                sleep(1)
                                clickpage=1
                        except:pass
                    elif clickpage==1:
                        list_city_id = ['108685149163106','110184922344060','108424279189115','109434842408576','109659625720552','112131982132741','110444738976181','105756796124329','108161062545219','105618626137781','113373948676083','104063499628686','104983062871920','110419212320033']
                        while True:
                            email=random.choice(open(os.path.join(os.getcwd(),'data','profileaccount','MAIL.txt')).read().split('\n'))
                            if email=='':
                                email=random.choice(open(os.path.join(os.getcwd(),'data','profileaccount','MAIL.txt')).read().split('\n'))
                            else:break
                        while True:
                            zipcode=random.choice(open(os.path.join(os.getcwd(),'data','profileaccount','CODE_ZIP.txt')).read().split('\n'))
                            if zipcode=='':
                                zipcode=random.choice(open(os.path.join(os.getcwd(),'data','profileaccount','CODE_ZIP.txt')).read().split('\n'))
                            else:break
                        while True:
                            address=random.choice(open(os.path.join(os.getcwd(),'data','profileaccount','dia_chi.txt')).read().split('\n'))
                            if address=='':
                                address=random.choice(open(os.path.join(os.getcwd(),'data','profileaccount','dia_chi.txt')).read().split('\n'))
                            else:break
                        while True:
                            phone=random.choice(open(os.path.join(os.getcwd(),'data','profileaccount','sdt.txt')).read().split('\n'))
                            if phone=='':
                                phone=random.choice(open(os.path.join(os.getcwd(),'data','profileaccount','sdt.txt')).read().split('\n'))
                            else:break
                        try:
                            cookies_list=self.driver.get_cookies()
                            cookieString=''
                            for cookie in cookies_list[:-1]:
                                cookieString = cookieString + cookie["name"] + "="+cookie["value"]+"; "
                            self.cookie_pro5 = cookieString
                            #print(self.cookie_pro5)
                            #print(self.user_agent)
                            sleep(2)
                            sectionToken,collectionToken=self.get_token()
                            #print(self.pageid)
                            sleep(2)
                            self.changephone(phone,collectionToken,sectionToken)
                            sleep(2)
                            self.ChangeCategory(collectionToken,sectionToken,categories)
                            sleep(2)
                            self.cheangeemail(email,collectionToken,sectionToken)
                            sleep(2)
                            self.changeaddress(address,zipcode,list_city_id,collectionToken,sectionToken)
                            self.driver.refresh()
                            sleep(10)
                            numpage+=1
                            break
                        except:pass
                
            except:pass
            sleep(0.5)
        # worksheet.write(f'A{self.r+1}', f'{self.userid}')
        # worksheet.write(f'B{self.r+1}', 'Thành công')
        # worksheet.write(f'C{self.r+1}', f'{self.link}')
        # workbook.close()
        #self.closechrome()
    def checkpage(self):
        list_idpage=[]
        headers_get = {
            'authority': 'www.facebook.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': self.cookie,#'sb=mgS0Y2e1Z-i63rI5nm0V81FQ; datr=mgS0Y63cQzY-KaySOX2ph4vP; locale=fr_FR; c_user=100011053006549; xs=37%3A5gpies3EgzDVnA%3A2%3A1673033899%3A-1%3A9883; oo=v1%7C3%3A1673033901; m_page_voice=100011053006549; i_user=100089497651464; usida=eyJ2ZXIiOjEsImlkIjoiQXJvMnhvY2Rpa3FhciIsInRpbWUiOjE2NzMwMzQ0OTJ9; wd=783x979',
            'sec-ch-prefers-color-scheme': 'light',
            #'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': self.user_agent, #'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.23 Safari/537.36',
            'viewport-width': '1920',
        }
        idpef = requests.post('https://www.facebook.com/api/graphql/', headers=headers_get, data={'fb_dtsg': self.fb_dtsg,'jazoest': self.jazoest,'variables': '{"showUpdatedLaunchpointRedesign":true,"useAdminedPagesForActingAccount":false,"useNewPagesYouManage":true}','doc_id': '5300338636681652'},proxies=self.proxies).json()
        #print(idpef)
        a = idpef['data']['viewer']['actor']['profile_switcher_eligible_profiles']['nodes']
        for b in a:
            uid = b['profile']['id']
            #print(uid)
            list_idpage.append(uid)
        return list_idpage
    # def checkpage9(self):
    #     self.driver.get('https://mbasic.facebook.com')
    #     self.sign.emit('Load account facebook',2,self.r)
    #     sleep(3)
    #     for checkcon in range(20):
    #         try:
    #             if self.driver.find_element(By.XPATH,'/html/body/div/div/div[1]/div/form/table/tbody/tr/td[2]/input'):
    #                 cookies_list=self.driver.get_cookies()
    #                 cookieString=''
    #                 for cookie in cookies_list[:-1]:
    #                     cookieString = cookieString + cookie["name"] + "="+cookie["value"]+"; "
    #                 self.cookie = cookieString
    #                 html = self.driver.page_source
    #                 self.userid = html.split('<input type="hidden" name="target" value="')[1].split('"')[0]
    #                 self.fb_dtsg = html.split('<input type="hidden" name="fb_dtsg" value="')[1].split('"')[0]
    #                 self.jazoest = html.split('<input type="hidden" name="jazoest" value="')[1].split('"')[0]
    #                 break
    #         except:pass
    #         try:
    #             if self.driver.find_element('xpath','/html/body/div[1]/div/div[2]/div/div[1]/div[2]/div/a'):
    #                 cookies_list=self.driver.get_cookies()
    #                 cookieString=''
    #                 for cookie in cookies_list[:-1]:
    #                     cookieString = cookieString + cookie["name"] + "="+cookie["value"]+"; "
    #                 self.cookie = cookieString
    #                 html = self.driver.page_source
    #                 self.userid = html.split('<input type="hidden" name="target" value="')[1].split('"')[0]
    #                 self.fb_dtsg = html.split('<input type="hidden" name="fb_dtsg" value="')[1].split('"')[0]
    #                 self.jazoest = html.split('<input type="hidden" name="jazoest" value="')[1].split('"')[0]
    #                 break
    #         except:pass
    #         try:
    #             if self.driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[1]/form/div/div[3]/div/div[1]/label'):
    #                 self.driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[1]/form/div/div[3]/div/div[1]/label').click()
    #                 sleep(4)
    #                 now=1
    #         except:pass
    #         if now==1:
    #             try:
    #                 if self.driver.find_element(By.XPATH,'/html/body/div/div/div[1]/div/form/table/tbody/tr/td[2]/input'):
    #                     cookies_list=self.driver.get_cookies()
    #                     cookieString=''
    #                     for cookie in cookies_list[:-1]:
    #                         cookieString = cookieString + cookie["name"] + "="+cookie["value"]+"; "
    #                     self.cookie = cookieString
    #                     html = self.driver.page_source
    #                     self.userid = html.split('<input type="hidden" name="target" value="')[1].split('"')[0]
    #                     self.fb_dtsg = html.split('<input type="hidden" name="fb_dtsg" value="')[1].split('"')[0]
    #                     self.jazoest = html.split('<input type="hidden" name="jazoest" value="')[1].split('"')[0]
    #                     break
    #             except:pass
    #         sleep(1)
    #     try:
    #         if 'forced_account_switch' in self.driver.current_url:
    #             if self.driver.find_element('xpath','/html/body/div[1]/div[2]/div[1]/form/div/div[3]/div/div[1]/label/input'):
    #                 sleep(2)
    #                 self.driver.find_element('xpath','/html/body/div[1]/div[2]/div[1]/form/div/div[3]/div/div[1]/label/input').click()
    #                 sleep(2)
    #                 break
    #     except:pass
    #     try:
    #         if 'forced_account_switch' in self.driver.current_url:
    #             if self.driver.find_element(By.ID,'u_0_1_KP'):
    #                 self.driver.find_element(By.ID,'u_0_1_KP').click()
    #                 sleep(2)
    #                 break
    #     except:pass
    def checkspam(self,countvideoup,link):
        try:
            if self.driver.find_element('xpath','/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div/div'):
                print(1)
                if countvideoup >0:
                    open(os.path.join(os.getcwd(), 'data','spamupreel.txt'),'a+').write("%s|%s|%s\n"%(self.userid,'spam',link))
                else:
                    open(os.path.join(os.getcwd(), 'data','spamupreel.txt'),'a+').write("%s|%s\n"%(self.userid,'spam'))
                self.sign.emit('Spam',2,self.r)
                self.closechrome()
                sleep(2)
                self.sign2.emit(1,1,self.r)
                return
        except:pass
        try:
            if self.driver.find_element('xpath','/html/body/div[4]/div[1]/div/div[2]/div/div/div'):
                print(2)
                if countvideoup >0:
                    open(os.path.join(os.getcwd(), 'data','spamupreel.txt'),'a+').write("%s|%s|%s\n"%(self.userid,'spam',link))
                else:
                    open(os.path.join(os.getcwd(), 'data','spamupreel.txt'),'a+').write("%s|%s\n"%(self.userid,'spam'))
                self.sign.emit('Spam',2,self.r)
                self.closechrome()
                sleep(2)
                self.sign2.emit(1,1,self.r)
                return
        except:pass
    def UpReels(self):
        idpr=0
        #workbook = xlsxwriter.Workbook('upvideo.xlsx')
        #worksheet = workbook.add_worksheet()
        now=0
        link=''
        while True:
            self.driver.get('https://mbasic.facebook.com')
            self.sign.emit('Load account facebook',2,self.r)
            sleep(3)
            for checkcon in range(20):
                try:
                    if self.driver.find_element(By.XPATH,'/html/body/div/div/div[1]/div/form/table/tbody/tr/td[2]/input'):
                        cookies_list=self.driver.get_cookies()
                        cookieString=''
                        for cookie in cookies_list[:-1]:
                            cookieString = cookieString + cookie["name"] + "="+cookie["value"]+"; "
                        self.cookie = cookieString
                        html = self.driver.page_source
                        self.userid = html.split('<input type="hidden" name="target" value="')[1].split('"')[0]
                        self.fb_dtsg = html.split('<input type="hidden" name="fb_dtsg" value="')[1].split('"')[0]
                        self.jazoest = html.split('<input type="hidden" name="jazoest" value="')[1].split('"')[0]
                        break
                except:pass
                try:
                    if self.driver.find_element('xpath','/html/body/div[1]/div/div[2]/div/div[1]/div[2]/div/a'):
                        cookies_list=self.driver.get_cookies()
                        cookieString=''
                        for cookie in cookies_list[:-1]:
                            cookieString = cookieString + cookie["name"] + "="+cookie["value"]+"; "
                        self.cookie = cookieString
                        html = self.driver.page_source
                        self.userid = html.split('<input type="hidden" name="target" value="')[1].split('"')[0]
                        self.fb_dtsg = html.split('<input type="hidden" name="fb_dtsg" value="')[1].split('"')[0]
                        self.jazoest = html.split('<input type="hidden" name="jazoest" value="')[1].split('"')[0]
                        break
                except:pass
                try:
                    if self.driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[1]/form/div/div[3]/div/div[1]/label'):
                        self.driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[1]/form/div/div[3]/div/div[1]/label').click()
                        sleep(4)
                        now=1
                except:pass
                if now==1:
                    try:
                        if self.driver.find_element(By.XPATH,'/html/body/div/div/div[1]/div/form/table/tbody/tr/td[2]/input'):
                            cookies_list=self.driver.get_cookies()
                            cookieString=''
                            for cookie in cookies_list[:-1]:
                                cookieString = cookieString + cookie["name"] + "="+cookie["value"]+"; "
                            self.cookie = cookieString
                            html = self.driver.page_source
                            self.userid = html.split('<input type="hidden" name="target" value="')[1].split('"')[0]
                            self.fb_dtsg = html.split('<input type="hidden" name="fb_dtsg" value="')[1].split('"')[0]
                            self.jazoest = html.split('<input type="hidden" name="jazoest" value="')[1].split('"')[0]
                            break
                    except:pass
                sleep(1)
            try:
                if 'forced_account_switch' in self.driver.current_url:
                    if self.driver.find_element('xpath','/html/body/div[1]/div[2]/div[1]/form/div/div[3]/div/div[1]/label/input'):
                        sleep(2)
                        self.driver.find_element('xpath','/html/body/div[1]/div[2]/div[1]/form/div/div[3]/div/div[1]/label/input').click()
                        sleep(2)
                        break
            except:pass
            try:
                if 'forced_account_switch' in self.driver.current_url:
                    if self.driver.find_element(By.ID,'u_0_1_KP'):
                        self.driver.find_element(By.ID,'u_0_1_KP').click()
                        sleep(2)
                        break
            except:pass
            try:
                if 'forced_account_switch' in self.driver.current_url:
                    if self.driver.find_element(By.ID,'u_0_0_SI'):
                        self.driver.find_element(By.ID,'u_0_0_SI').click()
                        sleep(2)
                        break
            except:pass
            try:
                if 'forced_account_switch' in self.driver.current_url:
                    if self.driver.find_element(By.ID,'u_0_1_4N'):
                        self.driver.find_element(By.ID,'u_0_1_4N').click()
                        sleep(2)
                        break
            except:pass
            
            self.sign.emit('Check page',2,self.r)
            sleep(1)
            list_linkfb=self.checkpage()
            if len(list_linkfb)>0:
                for idpage in list_linkfb:
                    while True:
                        self.driver.get('https://mbasic.facebook.com')
                        #.sign.emit('Load account facebook',2,self.r)
                        sleep(2)
                        try:
                            if self.driver.find_element(By.XPATH,'/html/body/div/div/div[1]/div/form/table/tbody/tr/td[2]/input'):
                                break
                        except:pass
                        try:
                            if self.driver.find_element('xpath','/html/body/div[1]/div/div[2]/div/div[1]/div[2]/div/a'):
                                break
                        except:pass
                        try:
                            if self.driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[1]/form/div/div[3]/div/div[1]/label'):
                                self.driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div[1]/form/div/div[3]/div/div[1]/label').click()
                                sleep(4)
                                now=1
                        except:pass
                        if now==1:
                            try:
                                if self.driver.find_element(By.XPATH,'/html/body/div/div/div[1]/div/form/table/tbody/tr/td[2]/input'):
                                    break
                            except:pass
                        try:
                            if 'forced_account_switch' in self.driver.current_url:
                                if self.driver.find_element('xpath','/html/body/div[1]/div[2]/div[1]/form/div/div[3]/div/div[1]/label/input'):
                                    sleep(2)
                                    self.driver.find_element('xpath','/html/body/div[1]/div[2]/div[1]/form/div/div[3]/div/div[1]/label/input').click()
                                    sleep(2)
                                    break
                        except:pass
                        try:
                            if 'forced_account_switch' in self.driver.current_url:
                                if self.driver.find_element(By.ID,'u_0_1_KP'):
                                    self.driver.find_element(By.ID,'u_0_1_KP').click()
                                    sleep(2)
                                    break
                        except:pass
                        try:
                            if 'forced_account_switch' in self.driver.current_url:
                                if self.driver.find_element(By.ID,'u_0_0_SI'):
                                    self.driver.find_element(By.ID,'u_0_0_SI').click()
                                    sleep(2)
                                    break
                        except:pass
                        try:
                            if 'forced_account_switch' in self.driver.current_url:
                                if self.driver.find_element(By.ID,'u_0_1_4N'):
                                    self.driver.find_element(By.ID,'u_0_1_4N').click()
                                    sleep(2)
                                    break
                        except:pass
                    try:
                        #linkfb=self.driver.find_element(By.XPATH,f'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div[1]/div/div[{idpr}]/div/div/div/div/div[1]/div/div[1]/div/a').get_attribute('href')
                        linkfb=f'https://www.facebook.com/profile.php?id={idpage}'
                        print(linkfb)
                        #print(linkfb)
                        self.sign.emit(f'Đến link : {linkfb}',2,self.r)
                        self.driver.get(f'{linkfb}')
                        link+=linkfb+'|'
                        timeline=0
                        while True:
                            timeline+=1
                            #print(timeline)
                            #self.checkspam(countvideoup,link)
                            try:
                                if self.driver.find_element('xpath','/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div/div'):
                                    self.sign.emit('Spam',2,self.r)
                                    self.closechrome()
                                    sleep(2)
                                    self.sign2.emit(1,1,self.r)
                                    return
                            except:pass
                            try:
                                if self.driver.find_element('xpath','/html/body/div[4]/div[1]/div/div[2]/div/div/div'):
                                    self.sign.emit('Spam',2,self.r)
                                    self.closechrome()
                                    sleep(2)
                                    self.sign2.emit(1,1,self.r)
                                    return
                            except:pass
                            try:
                                if f'actorID":"{idpage}' in self.driver.page_source:
                                    self.sign.emit('Switch Success',2,self.r)
                                    break
                            except:pass
                            if timeline==60:
                                self.driver.refresh()
                                timeline=0
                                #self.sign.emit('không nhận diện được',2,self.r)
                                #self.closechrome()
                                #return False
                            try:
                                if self.driver.find_element('xpath','/html/body/div[2]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]/div/div[1]/div/span/span'):
                                    self.driver.find_element('xpath','/html/body/div[2]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]/div/div[1]/div/span/span').click()
                                    sleep(2)
                            except:pass
                            try:
                                if self.driver.find_element('xpath','/html/body/div[4]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]'):
                                    sleep(1)
                                    self.driver.find_element('xpath','/html/body/div[4]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]').click()
                                    #self.driver.find_element('xpath','/html/body/div[4]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]').click()
                                    sleep(1)
                            except:pass
                            try:
                                if self.driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div[1]/div/div/div/div/div/div/div/div[2]/div/div'):
                                    self.driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div[1]/div/div/div/div/div/div/div/div[2]/div/div').click()
                                    self.driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[4]/div[1]/div/div/div/div/div/div/div/div[2]/div/div').click()
                                    sleep(0.5)
                            except:pass
                            try:
                                if self.driver.find_element('xpath','/html/body/div[5]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]/div/div[1]/div/span/span'):
                                    self.driver.find_element('xpath','/html/body/div[5]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]/div/div[1]/div/span/span').click()
                                    sleep(0.1)
                                    self.driver.find_element('xpath','/html/body/div[5]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]/div/div[1]/div/span/span').click()
                            except:pass
                            try:
                                if self.driver.find_element('xpath','/html/body/div[5]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]'):
                                    self.driver.find_element('xpath','/html/body/div[5]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]').click()
                                    self.driver.find_element('xpath','/html/body/div[5]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]').click()
                            except:pass
                            try:
                                if self.driver.find_element('xpath','/html/body/div[5]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]/div'):
                                    self.driver.find_element('xpath','/html/body/div[5]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]/div').click()
                                    self.driver.find_element('xpath','/html/body/div[5]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]/div').click()
                            except:pass       
                            try:
                                if self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[4]/div[1]/div/div/div/div/div/div/div/div[2]/div/div'):
                                    self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[4]/div[1]/div/div/div/div/div/div/div/div[2]/div/div').click()
                                    self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[4]/div[1]/div/div/div/div/div/div/div/div[2]/div/div').click()
                            except:pass
                            try:
                                if self.driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[4]/div[1]/div/div/div/div/div/div/div/div[2]/div/div'):
                                    self.driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[4]/div[1]/div/div/div/div/div/div/div/div[2]/div/div').click()
                                    self.driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[4]/div[1]/div/div/div/div/div/div/div/div[2]/div/div').click()
                            except:
                                try:
                                    if self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[4]/div[1]/div/div/div/div/div/div/div/div[2]/div/div/div/div[1]/div/span/span'):
                                        self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[4]/div[1]/div/div/div/div/div/div/div/div[2]/div/div/div/div[1]/div/span/span').click()
                                        self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[4]/div[1]/div/div/div/div/div/div/div/div[2]/div/div/div/div[1]/div/span/span').click()
                                except:
                                    try:
                                        if self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[1]/div/div/div/div/div/div/div/div[2]/div/div'):
                                            self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[1]/div/div/div/div/div/div/div/div[2]/div/div').click()
                                            self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div[1]/div/div/div/div/div/div/div/div[2]/div/div').click()
                                    except:pass
                            sleep(0.25)
                    except:pass
                    try:
                        vpn_app = Application(backend="uia").connect(title='MD5 Hash Changer',timeout=5)
                        m=vpn_app.MD5_Hash_Changer.child_window(title="Start Change MD5").wrapper_object().click_input()
                    except:pass
                    sleep(5)
                    checkpagereel=0
                    for countvideoup in range(int(self.threadvideo)):
                        self.checkspam(countvideoup,link)
                        try:
                            if countmax==1:
                                self.driver.get('https://www.facebook.com/reels/create/?surface=ADDL_PROFILE_PLUS')
                                countmax=0
                                # try:
                                #     self.driver.switch_to.alert.accept()
                                # except:pass
                                break
                        except:pass
                        
                        try:
                            try:
                                if self.driver.find_element('xpath','/html/body/div[2]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]/div/div[1]/div/span/span'):
                                    self.driver.find_element('xpath','/html/body/div[2]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]/div/div[1]/div/span/span').click()
                                    #sleep(2)
                            except:pass
                            try:
                                if self.driver.find_element('xpath','/html/body/div[4]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]'):
                                    self.driver.find_element('xpath','/html/body/div[4]/div[1]/div/div[2]/div/div/div/div[2]/div[3]/div/div[1]/div[2]').click()
                            except:pass
                            try:
                                if self.driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[2]/div/div[3]/div'):
                                    self.driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[2]/div/div[3]/div').click()
                            except:pass
                            try:
                                if self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[2]/div/div[4]/div'):
                                    self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[2]/div/div[4]/div').click()
                            except:pass
                            try:
                                if self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[1]/div[3]/a'):
                                    #.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[1]/div[3]/a')
                                    checkpagereel=0
                            except:
                                try:
                                    if self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[1]/div[3]/a/div/div[1]/div/span'):
                                        checkpagereel=0
                                except:
                                    checkpagereel=1
                            if checkpagereel==1:
                                self.sign.emit('Go page up reels',2,self.r)
                                self.driver.get('https://www.facebook.com/reels/create/?surface=ADDL_PROFILE_PLUS')
                                rdvideos=random.choice(os.listdir(os.path.join(os.getcwd(),'video_data')))
                                path=os.path.join(os.getcwd(),'video_data',rdvideos)
                                sleep(2)
                                tabin=0
                                checkup=0
                                timeout=0
                                while True:
                                    self.checkspam(countvideoup,link)
                                    timeout+=1
                                    try:
                                        if self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div/div[3]/div'):
                                            self.sign.emit('Không thể upvideo',2,self.r)
                                            checkup=1
                                            break 
                                    except:pass
                                    try:
                                        if self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[1]/div[3]/a/div'):    
                                            #self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div/div/div[1]/div[3]/a/div')    
                                            #open(os.path.join(os.getcwd(), 'data','spamupreel.txt'),'a+').write("%s|%s|%s\n"%(self.userid,'spam'))
                                            self.sign.emit('Không thể upvideo',2,self.r)
                                            checkup=1
                                            break
                                    except:pass
                                    try:
                                        if self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[3]/a/div/div[1]/div'):
                                            self.sign.emit('Không thể upvideo',2,self.r)
                                            checkup=1
                                            break
                                    except:pass
                                    self.checkspam(countvideoup,link)
                                    if timeout==100:
                                        self.driver.refresh()
                                    try:#/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/form/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div/div[1]/div
                                        #print(self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/form/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div/div[1]/div').get_attribute('innerHTML'))
                                        if 'blob:http' in self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/form/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div/div[1]/div').get_attribute('innerHTML'):
                                            break
                                    except:
                                        try:
                                            if 'blob:http' in self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/form/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div/div/div/div[1]/div/div/div[1]/div/div/div').get_attribute('innerHTML'):
                                                break
                                        except:pass
                                    try:
                                        if self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/form/div/div/div[1]/div/div[2]/div[1]/div[2]/div/div/div[1]/div/div'):
                                            #self.sign.emit('Add videos',2,self.r)
                                            self.sign.emit(f'Úp videos lượt {countvideoup+1}',2,self.r)
                                            sleep(5)
                                            self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/form/div/div/div[1]/div/div[2]/div[1]/div[2]/div/div/div[1]/div/div').send_keys('a')
                                            tabin=1
                                    except:pass
                                    try:
                                        if self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/form/div/div/div[1]/div/div[2]/div[1]/div[2]/div/div/div[1]/div/div'):
                                            #self.sign.emit('Add videos',2,self.r)
                                            self.sign.emit(f'Úp videos lượt {countvideoup+1}',2,self.r)
                                            sleep(5)
                                            self.driver.find_element('xpath','html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/form/div/div/div[1]/div/div[2]/div[1]/div[2]/div/div/div[1]/div/div').send_keys('a')
                                            tabin=1
                                    except:pass
                                    if tabin==1:
                                        try:
                                            if self.driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div[5]/div/div/div[3]/form/div/div/div[1]/div/div[3]/div[1]/div[2]/div/div/div[1]/div/input'):
                                                self.sign.emit('Add videos',2,self.r)
                                                sleep(2)
                                                self.driver.find_element('xpath','/html/body/div[1]/div[1]/div[1]/div/div[5]/div/div/div[3]/form/div/div/div[1]/div/div[3]/div[1]/div[2]/div/div/div[1]/div/input').send_keys(path)
                                                sleep(3)
                                        except:pass
                                        try:
                                            if self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/form/div/div/div[1]/div/div[2]/div[1]/div[2]/div/div/div[1]/div/input'):
                                                self.sign.emit('Add videos',2,self.r)
                                                sleep(2)
                                                self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/form/div/div/div[1]/div/div[2]/div[1]/div[2]/div/div/div[1]/div/input').send_keys(path)
                                                sleep(3)
                                        except:
                                            try:
                                                if self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/form/div/div/div[1]/div/div[2]/div[1]/div[2]/div/div/div[1]/div/input'):
                                                    self.sign.emit('Add videos',2,self.r)
                                                    sleep(2)
                                                    self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/form/div/div/div[1]/div/div[2]/div[1]/div[2]/div/div/div[1]/div/input').send_keys(path)
                                                    sleep(3)
                                            except:pass
                                    sleep(0.5)
                                if checkup==1:
                                    break
                                else:
                                    try:
                                        if self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/form/div/div/div[1]/div/div[3]/div[2]/div/div'):
                                            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/form/div/div/div[1]/div/div[3]/div[2]/div/div')))
                                            self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/form/div/div/div[1]/div/div[3]/div[2]/div/div').click()
                                            sleep(0.5)
                                            self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/form/div/div/div[1]/div/div[3]/div[2]/div[2]/div[1]').click()
                                            sleep(1)
                                    except:pass
                                    try:
                                        if self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/form/div/div/div[1]/div/div[3]/div[2]/div/div'):
                                            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/form/div/div/div[1]/div/div[3]/div[2]/div/div')))
                                            self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/form/div/div/div[1]/div/div[3]/div[2]/div/div').click()
                                            sleep(0.5)
                                            self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/form/div/div/div[1]/div/div[3]/div[2]/div[2]/div[1]/div').click()
                                            sleep(1)
                                    except:pass

                                    #if self.cmtup:
                                    self.sign.emit('Add details',2,self.r)
                                    cmt=random.choice(open(os.path.join(os.getcwd(),'data','title.txt')).read().split('\n'))
                                    if 'ï»¿' in cmt:
                                        cmt=cmt.split('ï»¿')[1]
                                    for checkcap in range(20):
                                        try:
                                            if self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/form/div/div/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div/div[1]/div[1]/div[1]/div[1]'):
                                                #self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/form/div/div/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div/div[1]/div[1]/div[1]/div[1]').click()
                                                for sendcmt in cmt:
                                                    self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/form/div/div/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div/div[1]/div[1]/div[1]/div[1]').send_keys(sendcmt)
                                                    sleep(0.1)
                                                break
                                        except:pass
                                        try:
                                            if self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/form/div/div/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div/div[1]/div[1]/div[1]/div[1]'):
                                                #self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/form/div/div/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div/div[1]/div[1]/div[1]/div[1]').click()
                                                for sendcmt in cmt:
                                                    self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/form/div/div/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div/div[1]/div[1]/div[1]/div[1]').send_keys(sendcmt)
                                                    sleep(0.1)
                                                break
                                        except:pass
                                        try:
                                            if self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/form/div/div/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div/div[1]/div[1]/div[1]'):
                                                #self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/form/div/div/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div/div[1]/div[1]/div[1]').click()
                                                for sendcmt in cmt:
                                                    self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/form/div/div/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div/div[1]/div[1]/div[1]').send_keys(sendcmt)
                                                    sleep(0.1)
                                                break
                                        except:pass
                                        sleep(0.5)
                                    self.sign.emit('Add details xong',2,self.r)
                                    sleep(6)
                                    publish='/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/form/div/div/div[1]/div/div[3]/div[2]/div[2]/div[1]'
                                    #WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH,publish)))
                                    sleep(1)
                                    checkreload=0
                                    while True:
                                        if checkreload==100:
                                            self.driver.refresh()
                                            break
                                        self.checkspam(countvideoup,link)
                                        try:
                                            self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div/div/div[1]/form/div/div/div[1]/div/div[3]/div[2]/div[2]/div[1]').click()
                                        except:
                                            try:
                                                self.driver.find_element(By.XPATH,publish).click()
                                            except:pass
                                        try:
                                            checkup=self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div/div[1]/form/div/div/div[1]/div/div[3]/div[1]/div[1]/div/div/div/div[2]/div/div/div/div/span/span/div/div').get_attribute('innerHTML')
                                            if "can't be uploaded" in checkup:
                                                #print('no up')
                                                countmax=1
                                                break
                                        except:pass
                                        get_url = self.driver.current_url
                                        if '/?s=reel_composer'in get_url:
                                            #print(get_url)
                                            self.sign.emit('Úp xong',2,self.r)
                                            if self.cmtup:
                                                self.cmtvideo()
                                            self.sign.emit('Load video xong',2,self.r)
                                            sleep(1)
                                            timeline=random.randint(50,60)
                                            self.sign.emit(f'Chờ {timeline}s',2,self.r)
                                            for timedelay in range(timeline):
                                                self.sign.emit(f'Chờ {(timeline-(timedelay+1))}s',2,self.r)
                                                sleep(1)
                                            break
                                        elif 'videos' in get_url:
                                            self.sign.emit('Úp xong',2,self.r)
                                            if self.cmtup:
                                                self.cmtvideo()
                                            self.sign.emit('Load video xong',2,self.r)
                                            sleep(1)
                                            timeline=random.randint(50,60)
                                            self.sign.emit(f'Chờ {timeline}s',2,self.r)
                                            for timedelay in range(timeline):
                                                self.sign.emit(f'Chờ {(timeline-(timedelay+1))}s',2,self.r)
                                                sleep(1)
                                            break
                                        checkreload+=1
                                        sleep(0.5)
                            else:pass
                        except:pass
                        sleep(0.5)
                open(os.path.join(os.getcwd(), 'data','successupreels.txt'),'a+').write("%s|%s|%s\n"%(self.userid,'Success',link))
                self.sign.emit('Hoàn thành',2,self.r)
                self.closechrome()
                sleep(2)
                self.sign2.emit(1,1,self.r)
                return
            else:
                open(os.path.join(os.getcwd(), 'data','nopage.txt'),'a+').write("%s|%s\n"%(self.userid,'Fail'))
                self.sign.emit('Chưa có page',2,self.r)
                self.closechrome()
                sleep(2)
                self.sign2.emit(1,1,self.r)
                return
    def cmtvideo(self):
        rdcmt=random.choice(open(os.path.join(os.getcwd(),'data','cmtreel.txt')).read().split('\n'))
        while True:
            try:
                if self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div[2]/div/div/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div[3]/div/div/div/div[1]/div'):
                    self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div[2]/div/div/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div[3]/div/div/div/div[1]/div').click()
                    sleep(1)
                    break
            except:pass
            try:
                if self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[7]/div/div/div[3]/div[2]/div/div/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div[3]/div/div/div/div[1]/div/html/body/div[1]/div/div[1]/div/div[7]/div/div/div[3]/div[2]/div/div/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div[3]/div/div/div/div[1]/div'):
                    self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[7]/div/div/div[3]/div[2]/div/div/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div[3]/div/div/div/div[1]/div/html/body/div[1]/div/div[1]/div/div[7]/div/div/div[3]/div[2]/div/div/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div[3]/div/div/div/div[1]/div').click()
                    sleep(1)
                    break
            except:pass
            try:
                if self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div[2]/div/div/div[1]/div/div/div/div/div[3]/div[2]/div/div/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/form/div/div/div[1]/div/div[1]'):
                    self.sign.emit('Comment reel',2,self.r)
                    #sleep(2)
                    self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div[2]/div/div/div[1]/div/div/div/div/div[3]/div[2]/div/div/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/form/div/div/div[1]/div/div[1]').click()
                    sleep(1)
                    break
            except:pass
            
            try:
                if self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div[1]/div/div/div[5]/div[2]/div/div[2]/div[1]/form/div/div/div[1]/div/div[1]'):
                    self.sign.emit('Comment reel',2,self.r)
                    #sleep(2)
                    self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div[1]/div/div/div[5]/div[2]/div/div[2]/div[1]/form/div/div/div[1]/div/div[1]').click()
                    sleep(2)
                    break
            except:pass
            
            try:
                if self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div[2]/div/div/div[1]/div/div/div/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div[3]/div/div/div/div[1]/div'):
                    self.sign.emit('Comment reel',2,self.r)
                    sleep(2)
                    self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div[2]/div/div/div[1]/div/div/div/div/div[2]/div/div/div/div[2]/div[2]/div/div/div/div[3]/div/div/div/div[1]/div').click()
                    sleep(5)
                    break
            except:pass
        while True:
            try:
                if self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div[2]/div/div/div[1]/div/div/div/div/div[3]/div[2]/div/div/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/form/div/div/div[1]/div/div[1]'):
                    for cmtr in rdcmt:
                            self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div[2]/div/div/div[1]/div/div/div/div/div[3]/div[2]/div/div/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/form/div/div/div[1]/div/div[1]').send_keys(cmtr)
                            sleep(0.1)
                    self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div[2]/div/div/div[1]/div/div/div/div/div[3]/div[2]/div/div/div[1]/div/div[3]/div[2]/div/div/div[2]/div[1]/form/div/div/div[1]/div/div[1]').send_keys(Keys.ENTER)
                    self.sign.emit('Comment xong',2,self.r)
                    sleep(random.randint(10,15))
                    break
            except:pass
            try:
                if self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div[1]/div/div/div[5]/div[2]/div/div[2]/div[1]/form/div/div/div[1]/div/div[1]'):
                    for cmtr in rdcmt:
                        self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div[1]/div/div/div[5]/div[2]/div/div[2]/div[1]/form/div/div/div[1]/div/div[1]').send_keys(cmtr)
                        sleep(0.1)
                    self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div[2]/div/div/div[2]/div[1]/div/div[1]/div/div/div[5]/div[2]/div/div[2]/div[1]/form/div/div/div[1]/div/div[1]').send_keys(Keys.ENTER)
                    self.sign.emit('Comment xong',2,self.r)
                    sleep(random.randint(10,15))
                    break
            except:pass
            try:
                if self.driver.find_element('xpath','/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div[2]/div/div/div[1]/div/div/div/div/div[3]/div[2]/div/div/div[1]/div/div[3]/div[2]/div/div[2]/div[2]/div[1]/form/div/div/div[1]/div/div[1]'):
                    for cmtr in rdcmt:
                            self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div[2]/div/div/div[1]/div/div/div/div/div[3]/div[2]/div/div/div[1]/div/div[3]/div[2]/div/div[2]/div[2]/div[1]/form/div/div/div[1]/div/div[1]').send_keys(cmtr)
                            sleep(0.1)
                    self.driver.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[5]/div/div/div[3]/div[2]/div/div/div[1]/div/div/div/div/div[3]/div[2]/div/div/div[1]/div/div[3]/div[2]/div/div[2]/div[2]/div[1]/form/div/div/div[1]/div/div[1]').send_keys(Keys.ENTER)
                    self.sign.emit('Comment xong',2,self.r)
                    sleep(random.randint(10,15))
                    break
            except:pass
        sleep(0.5)       
def main():
    app=QApplication(sys.argv)
    main_win=MainWindow()
    main_win.show()
    app.exec()
    #sys.exit(app.exec())
if __name__=='__main__':
    main()
