import os,sys
import numpy as np
from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass
import matplotlib.pyplot as plt

from sklearn.preprocessing import MinMaxScaler

@dataclass
class Datatransformationconfig:
    train_data_file_path=os.path.join('artifacts','train.csv')
    test_data_file_path=os.path.join('artifacts','test.csv')

class Datatransformation:
    def __init__(self):
        self.transformationconfig=Datatransformationconfig()
    
    def initiate_data_transformation(self,stock_dataframe):
        try:
            global train_data,test_data
            logging.info('data transformation initiated')
            
            # NUll check 
            logging.info('checking null values in dataset')
            Null_check=stock_dataframe.isnull().sum()

            if (Null_check.values>0).any():
                logging.info('Null values present in dataset. Check before Proceeding. Suggestion: use "SimpleImputer" while creating transformation pipeline')
            else:
                logging.info('No null values in dataset ')

            ##choosing column for prediction
            logging.info("choosing column from dataset for further analysis")
            pred_df=stock_dataframe['close']
            plt.plot(pred_df)
            #logging.info('Distribution of "close" category over years graph representation window will popup')
            #plt.show()

            logging.info('Data Scaling initiated')
            #Data scaling using MinMaxScaler

            scaler=MinMaxScaler(feature_range=(0,1))
            logging.info('LSTM are sensitive to the scale of data. So we apply "MinMax scaler"')
            pred_df=scaler.fit_transform(np.array(pred_df).reshape(-1,1))

            #Splitting test and train

            logging.info('Splitting data to test and train in ratio "65%" and "35%"')
            training_size=int(len(pred_df)*0.65)
            test_size=len(pred_df)-training_size
            train_data,test_data=pred_df[0:training_size],pred_df[training_size:len(pred_df),:1]

            logging.info('train and test data split is done with size with "train data length":{train_len} and "test data length":{test_len}'.format(train_len=len(train_data),test_len=len(test_data)))

            return(train_data,
                    test_data)
        except Exception as e:
            raise CustomException(e,sys)
        
        
            
    def create_dataset(self,dataset,time_step=1):
        logging.info('creating dataset for model')
        dataX,dataY=[],[]
        for i in range(len(dataset)-time_step-1):
            a=dataset[i:(i+time_step),0]
            dataX.append(a)
            dataY.append(dataset[i+time_step,0])
        
        return np.array(dataX),np.array(dataY)
    

    

         