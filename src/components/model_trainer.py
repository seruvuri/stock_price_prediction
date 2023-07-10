import os,sys
import numpy as np
from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM

from src.utils import *


@dataclass
class ModelTrainerConfig:
    model_pickle_file_path=os.path.join('artifacts','model.pkl')

class ModelTrainer:
    def __init__(self):
        self.modeltrainerconfig=ModelTrainerConfig()

    def initiate_model_trainer(self,X_train,X_test,y_train,y_test):
        try:
            logging.info('>>>>>>>>>>>>>>Model trainer initiated<<<<<<<<<<<<<<<<<<<<<')
            logging.info('Reshaping X_train and X_test data')
            X_train=X_train.reshape(X_train.shape[0],X_train.shape[1],1)
            X_test=X_test.reshape(X_test.shape[0],X_test.shape[1],1)
            logging.info('Building sequential "LSTM" model with 3 hidden layers and 1 output layer')
            model=Sequential()
            model.add(LSTM(50,return_sequences=True,input_shape=(150,1)))# first layer we pass "X_train.shape[1],1"
            model.add(LSTM(50,return_sequences=True))# second layer
            model.add(LSTM(50))#third layer
            model.add(Dense(1))#output layer

            model.compile(loss="mean_squared_error",optimizer='adam')
            #model summary
            print(model.summary())

            logging.info('Training LSTM model')

            LSTM_model=model.fit(X_train,y_train,validation_data=(X_test,y_test),epochs=100,batch_size=64,verbose=1)
            
            #logging.info("Saving LSTM model to pickle file and available in path: {pickle_file_path}".format(' ',pickle_file_path=self.modeltrainerconfig.model_pickle_file_path))

            #save_obj(file_path=self.modeltrainerconfig.model_pickle_file_path,obj=LSTM_model)
            return LSTM_model
        except Exception as e:
            raise CustomException(e,sys)
    