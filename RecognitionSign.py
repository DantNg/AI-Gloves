import pandas as pd
import numpy as np
import os
import glob
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix



class CharactersRecognition:
    def __init__(self):
        
        self.df = pd.read_csv('ALL_DATA.csv',index_col=None)
        print('Done reading!')
        self.X = self.df.drop(columns=['LABEL'], axis=1)
        #print (self.X)
        self.y = self.df['LABEL']
        self.TrainData()
    def TrainData(self):
        path = 'TrainingData/'
        csv_files = glob.glob(os.path.join(path, "*.csv"))
        all_df= pd.DataFrame()
        try:
            # loop over the list of csv files
            for f in csv_files:
                # read the csv file
                df = pd.read_csv(f)
                all_df = all_df.append(df)  
        except Exception:
            print('Có lỗi khi đọc file')
        #print(all_df)
        all_df.to_csv('ALL_DATA.csv',index=False)
        X_train, X_test, y_train, y_test = train_test_split(
            self.X, self.y, test_size=0.4)
        self.rf = RandomForestClassifier()
        self.rf.fit(X_train.values, y_train)
        print("Trainning complete!")
    def predictData(self, test_data):
        test = [test_data]
        predictions = self.rf.predict(test)
        print(predictions[0])
        return predictions[0]
        # print(confusion_matrix(y_test,predictions))
        # print('\n')
        # print(classification_report(y_test,predictions))


if __name__ == '__main__':
    DataTrain = CharactersRecognition()
    serial = [2266,	1434, 1389,	4095, 1305]
    DataTrain.predictData(serial)
