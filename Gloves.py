import serial
import serial.tools.list_ports
import pandas as pd
import time

class Gloves:
        def __init__(self):
            self.device_com_port = ''
            self.device_baudrate = 115200
            self.baudrate_list = [9600,38400,57600,115200]
            self.data = ''
        def getAllComPorts(self):
            ports = serial.tools.list_ports.comports()
            for port, desc, hwid in sorted(ports):
                print("{}: {} ".format(port, desc))
            return ports
                
        def set_device_connections(self, port,baudrate):
            self.device_com_port = port
            self.device_com_baudrate = baudrate
        def connect2Devices(self):
            if self.device_com_port != '':
                print("Connect to {}".format(self.device_com_port))
                try:
                    # make sure the 'COM#' is set according the Windows Device Manager
                    self.serial = serial.Serial(self.device_com_port, self.device_baudrate, timeout=1)
                    time.sleep(2)
                    return 1
                    #self.serial.close()
                    
                except :
                    print("Failed to connect device!")
                    return 0
            else:
                print("Select COM port!")
                return 0
        def disconnect2Device(self):
            try:
                self.serial.close()
            except :
                print("Failed to unconnect device!")
        def readData(self):
            #self.getAllComPorts()
            try:
                    line = self.serial.readline()   # read a byte
                    if line:
                        string = line.decode()  # convert the byte string to a unicode string
                        self.data = string.split('\t')
                        self.data[6] = self.data[6][:-1] 
                        for i in range(0, len(self.data)):
                            self.data[i] = int(self.data[i])
                        print(self.data)
            except :
                print("Failed to read serial!")
if __name__ == "__main__":
    gloves = Gloves()
    gloves.set_device_connections('COM34',115200)
    gloves.connect2Devices()
    log_data =[]
    for i in range(10):
        gloves.readData()
        log_data.append(gloves.data)
    gloves.disconnect2Device()
    df = pd.DataFrame(log_data,columns=['F1','F2','F3','F4','F5','X','Y'])
    df['LABEL']='B'
    print(df)
    df.to_csv('TrainingData\B.csv',index=False)
    
