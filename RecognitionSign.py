import pandas as pd
import numpy as np
import os
import glob
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib


class CharactersRecognition:
    def __init__(self):
        if os.path.exists('random_forest_model.pkl'):
            print("Random forest model has existed")
        else:
            print("Random forest model has not been created")
            try:
                self.df = pd.read_csv('ALL_DATA.csv',index_col=None)
                print('Done reading!')
                self.X = self.df.drop(columns=['LABEL'], axis=1)
                #print (self.X)
                self.y = self.df['LABEL']
            except :
                pass
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
                all_df = pd.concat([all_df,df],ignore_index=True)  
        except Exception as e:
            print(f'Có lỗi khi đọc file : {e}')
            return

        #print(all_df)
        all_df.to_csv('ALL_DATA.csv',index=False)
        X_train, X_test, y_train, y_test = train_test_split(
            self.X, self.y, test_size=0.4)
        self.rf = RandomForestClassifier()
        self.rf.fit(X_train.values, y_train)
        # Lưu model vào tệp
        joblib.dump(self.rf, 'random_forest_model.pkl')
        print("Trainning complete!")

    def predictData(self, test_data):
        test = [test_data]
        model =  joblib.load('random_forest_model.pkl')
        predictions = model.predict(test)
        print(predictions[0])
        return predictions[0]
        # print(confusion_matrix(y_test,predictions))
        # print('\n')
        # print(classification_report(y_test,predictions))


if __name__ == '__main__':
    DataTrain = CharactersRecognition()
    serial = [1922,2813,2397,1099,3731,90,0,1,0,1]
    DataTrain.predictData(serial)
