import pandas as pd
import os
import glob
  
  
# use glob to get all the csv files 
# in the folder
path = 'TrainingData/'
csv_files = glob.glob(os.path.join(path, "*.csv"))
  
all_df= pd.DataFrame()
# loop over the list of csv files
for f in csv_files:
      
    # read the csv file
    df = pd.read_csv(f)
    print (df)
    all_df = all_df.append(df)  
    # # print the location and filename
    # print('Location:', f)
    # print('File Name:', f.split("\\")[-1])
      
    # # print the content
    # print('Content:')
    # print(df)
    # print()
print(all_df)
all_df.to_csv('ALL_DATA.csv',index=False)