import os,sys
import numpy as np
from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass
import tkinter
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
from sklearn.preprocessing import MinMaxScaler

@dataclass
class Datatransformationconfig:
    train_data_file_path=os.path.join('artifacts','train.csv')
    test_data_file_path=os.path.join('artifacts','test.csv')
    distribution_plot_file_path=os.path.join('Plots','Data_Distribution_graph.jpg')

class Datatransformation:
    def __init__(self):
        self.transformationconfig=Datatransformationconfig()
    
    def initiate_data_transformation(self,stock_dataframe):
        try:
            global train_data,test_data
            logging.info('>>>>>>>>>>>>>>>>Data transformation initiated<<<<<<<<<<<<<<<<<')
            #Close_stock=stock_dataframe['close']
            
            # NUll check 
            logging.info('checking null values in dataset')
            Null_check=stock_dataframe.isnull().sum()

            if (Null_check.values>0).any():
                logging.info('Null values present in dataset. Check before Proceeding. Suggestion: use "SimpleImputer" while creating transformation pipeline')
            else:
                logging.info('No null values in dataset ')

            ##choosing column for prediction
            
            pred_df=stock_dataframe.reset_index()['close']
            logging.info("choosing column from dataset for further analysis with dataset length {prediction_column}".format(prediction_column=len(pred_df)))
            ''''
            plt.plot(pred_df)
            logging.info('Distribution of "close" category over years graph representation available in path {dist_plot}'.format(dist_plot=self.transformationconfig.distribution_plot_file_path))
            plt.title('Distribution of "close" column')
            plt.show()
            plt.savefig(self.transformationconfig.distribution_plot_file_path)
            '''

            logging.info('Data Scaling initiated')
            #Data scaling using MinMaxScaler

            scaler=MinMaxScaler(feature_range=(0,1))
            logging.info('LSTM are sensitive to the scale of data. So we apply "MinMax scaler"')
            pred_df=scaler.fit_transform(np.array(pred_df).reshape(-1,1))

            #Splitting test and train

            logging.info('Splitting data to test and train in ratio "65%" and "35%"')
            training_size=int(len(pred_df)*0.65)
            test_size=len(pred_df)-training_size
            train_data,test_data=pred_df[0:training_size,:],pred_df[training_size:len(pred_df),:1]

            logging.info('train and test data split is done with size with "train data length":{train_len} and "test data length":{test_len}'.format(train_len=len(train_data),test_len=len(test_data)))
            
            return(train_data,
                    test_data,pred_df,scaler)
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
    

    

         