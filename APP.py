import sys
# pip install pyqt5
from PyQt5.QtWidgets import QApplication, QMainWindow
from MainUI import Ui_MainWindow
from Gloves import Gloves
from RecognitionSign import CharactersRecognition
from Transplate import convertText2Speech,convertSpeech2Text
from pyvi import ViUtils
import threading 
import pandas as pd
import time
class MainWindow:
    def __init__(self):
        self.main_win = QMainWindow()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self.main_win)
        self.device = Gloves()
        self.characterRecognition = CharactersRecognition()
        self.contentEntry =''
        all_com_ports = self.device.getAllComPorts()
        for port,detail,_ in all_com_ports:
            self.uic.comSelect.addItem(port)
        for baudrate in self.device.baudrate_list:
            self.uic.baudSelect.addItem(str(baudrate))
        #self.uic.pushButton_3.setStyleSheet("")
        #self.uic.baudSelect.addItem()
        
        self.initBtn()
    
    def show(self):
        # command to run
        self.main_win.show()
    
    def initBtn(self):
        #--------------------------------- TAB 1 -----------------------------------
        self.uic.transBtn.clicked.connect(self.translateText)
        self.uic.connectDeviceBtn_2.clicked.connect(self.startConnect2Device_TAB1)
        ### example speechh #### 
        self.uic.exBtn1.clicked.connect(self.translateBtn)
        self.uic.exBtn2.clicked.connect(self.translateBtn)
        self.uic.exBtn3.clicked.connect(self.translateBtn)
        self.uic.exBtn4.clicked.connect(self.translateBtn)
        self.uic.exBtn5.clicked.connect(self.translateBtn)
        self.uic.exBtn6.clicked.connect(self.translateBtn)
        self.uic.exBtn7.clicked.connect(self.translateBtn)
        self.uic.exBtn8.clicked.connect(self.translateBtn)
        self.uic.exBtn9.clicked.connect(self.translateBtn)
        self.uic.exBtn10.clicked.connect(self.translateBtn)
        self.uic.exBtn11.clicked.connect(self.translateBtn)
        self.uic.exBtn12.clicked.connect(self.translateBtn)
        #---------------------------------- TAB 2 ------------------------------------
        self.uic.turnVoiceBtn.clicked.connect(self.translateSpeech)
        
        #--------------------------------- TAB 3 -----------------------------------
        self.uic.trainBtn.clicked.connect(self.characterRecognition.TrainData)
        self.uic.connectDeviceBtn.clicked.connect(self.startConnect2Device_TAB3)
        self.uic.save_log_btn.clicked.connect(self.startLogData)
        #self.uic.trainBtn.clicked.connect(CharactersRecognition().TrainData)
    # @pyqtSlot()
    # def fade(self):
    #     self.uic.pushButton_3 = self.sender()  # enter the "fading button" state
    #     self.uic.pushButton_3.setWindowOpacity(0.5)
    #     self.uic.pushButton_3.setStyleSheet("background-color: red")
    
    def startConnect2Device_TAB1(self):
        print(self.uic.connectDeviceBtn_2.text())
        if self.uic.connectDeviceBtn_2.text() == 'Ngắt kết nối':
            self.uic.connectDeviceBtn_2.setText('Kết nối')
            self.device.disconnect2Device()
        else:
            try:
                self.uic.connectDeviceBtn_2.setText('Ngắt kết nối')
                self.device.set_device_connections(self.uic.comSelect.currentText(),int(self.uic.baudSelect.currentText()))
                if self.device.connect2Devices():
                    tab1_reading = threading.Thread(target=self.getDataFromDevice_TAB1)
                    tab1_reading.start()
            except:
                self.device.disconnect2Device()
                print("Lỗi kết nối đến thiết bị!")
        
    def startConnect2Device_TAB3(self):
        if self.uic.connectDeviceBtn.text() == 'Kết nối' or self.uic.connectDeviceBtn_2.text() == 'Kết nối':
            self.uic.connectDeviceBtn.setText('Ngắt kết nối')
            self.uic.connectDeviceBtn_2.setText('Ngắt kết nối')
            self.device.set_device_connections(self.uic.comSelect.currentText(),int(self.uic.baudSelect.currentText()))
            if self.device.connect2Devices():
               
                tab2_reading = threading.Thread(target=self.getDataFromDevice_TAB3)
                tab2_reading.start()
            else:
                self.uic.connectDeviceBtn.setText('Kết nối')
                self.uic.connectDeviceBtn_2.setText('Kết nối')
        else:
            self.device.disconnect2Device()
            self.uic.connectDeviceBtn.setText('Kết nối')
            self.uic.connectDeviceBtn_2.setText('Kết nối')   
    def getDataFromDevice_TAB1(self):
        lastCharacterRecognition =''
        confirmChar =0
        SOS_COUNT = 0
        while(self.uic.connectDeviceBtn_2.text() == 'Ngắt kết nối'):
            self.device.readData()
            #self.displayValue()
            serial = self.device.data
            self.characterRecognition = CharactersRecognition().predictData(serial)
            if(self.characterRecognition == lastCharacterRecognition):
                confirmChar= confirmChar +1
            else:
                lastCharacterRecognition =self.characterRecognition 
                confirmChar = 0 #reset confirm
            if SOS_COUNT == 3:
                print("SOS")
                SOS_COUNT = 0
            if(confirmChar == 3): #Xác nhận đúng 3 lần 
                if self.characterRecognition == 'DELETE' and len(self.contentEntry) > 0:
                    self.contentEntry = self.contentEntry[:-1]
                elif self.characterRecognition == 'SPACE':
                    self.contentEntry = self.contentEntry +' '
                elif self.characterRecognition == 'ENTER':
                    convertText2Speech(ViUtils.add_accents(self.contentEntry))
                    print("Phát âm thanh")
                    self.contentEntry = ''
                elif self.characterRecognition == 'S':
                    SOS_COUNT = SOS_COUNT + 1
                else:
                    self.contentEntry = self.contentEntry+self.characterRecognition
                print(self.contentEntry)    
                #self.uic.charDetec.setText(self.characterRecognition)
                self.uic.mutedEntryLabel.setText(self.contentEntry)
                confirmChar =0 #reset đếm confirm
    def getDataFromDevice_TAB3(self):
        while(self.uic.connectDeviceBtn.text() == 'Ngắt kết nối'):
            self.device.readData()
            self.displayValue()
            serial = self.device.data
            self.characterRecog = CharactersRecognition().predictData(serial)
            self.uic.charDetec.setText(self.characterRecog)  
    def startLogData(self):
        try:
            self.uic.num_sample.setText('0')
            logDataThread =threading.Thread(target=self.logDataTrain)
            logDataThread.start()
        except:
            print ("Không thể mở voice")

    def logDataTrain(self):
        self.device.set_device_connections(self.uic.comSelect.currentText(),int(self.uic.baudSelect.currentText()))
        label = self.uic.trainLabel.text()
        if self.device.connect2Devices():
            lst = []
            for i in range(20):
                self.device.readData()
                lst.append(self.device.data)
                self.uic.num_sample.setText(str(i+1))
                #self.displayValue()
            self.device.disconnect2Device()
            df = pd.DataFrame(lst,columns=['F1','F2','F3','F4','F5','X','Y','B1','B2','B3'])
            df['LABEL'] = label
            df.to_csv('TrainingData\\'+label+'.csv',index=False)
            print("Đã lưu dữ liệu!")
        else:
            print('Hãy kết nối với thiết bị')
    def displayValue(self):
        self.uic.F1_status.setText(str(self.device.data[0]))
        self.uic.F2_status.setText(str(self.device.data[1]))
        self.uic.F3_status.setText(str(self.device.data[2]))
        self.uic.F4_status.setText(str(self.device.data[3]))
        self.uic.F5_status.setText(str(self.device.data[4]))
        self.uic.X_status.setText(str(self.device.data[5]))
        self.uic.Y_status.setText(str(self.device.data[6]))
    def translateText(self):
        text = self.uic.mutedEntry.text()
        print(text)
        if(text!=''):
            convertText2Speech(text)
    def translateSpeech(self):
        
        try:
            voice = convertSpeech2Text()
            
            if voice != 0:
                self.uic.normalEntryLabel.setText(voice)
        except:
            print("Kiểm tra microphone!")
    def translateBtn(self):
        text =  self.main_win.sender().text()
        print(text)
        if(text!=''):
            convertText2Speech(text)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())

