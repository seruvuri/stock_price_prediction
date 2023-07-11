import os,sys
import numpy as np
from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
import math
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error

from src.utils import *


@dataclass
class ModelTrainerConfig:
    model_pickle_file_path=os.path.join('artifacts','model.pkl')

class ModelTrainer:
    def __init__(self):
        self.modeltrainerconfig=ModelTrainerConfig()

    def initiate_model_trainer(self,X_train,X_test,y_train,y_test,test_data,minmaxscaler,prediction_column):
        try:
            logging.info('>>>>>>>>>>>>>>Model trainer initiated<<<<<<<<<<<<<<<<<<<<<')
            logging.info('Reshaping input to be [samples, time steps, features] which is required for LSTM')
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
            model.fit(X_train,y_train,validation_data=(X_test,y_test),epochs=2,batch_size=64,verbose=1)
            
            
            logging.info('Predicting for X_train and X_test')
            train_predict=model.predict(X_train)
            test_predict=model.predict(X_test)

            logging.info('Transforming back to original form for calculating RMSE')

            train_predict=minmaxscaler.inverse_transform(train_predict)
            test_predict=minmaxscaler.inverse_transform(test_predict)

            train_RMSE=math.sqrt(mean_squared_error(y_train,train_predict))
            test_RMSE=math.sqrt(mean_squared_error(y_test,test_predict))
            logging.info('RMSE of "train data prediction":{train_rmse} and "test data prediction":{test_rmse}'.format(train_rmse=train_RMSE,test_rmse=test_RMSE))
            
            #considering 150 previous days for next 100 days predictions
            previous_days=150
            restofdays_in_dataset=len(test_data)-previous_days
            x_input=test_data[restofdays_in_dataset:].reshape(1,-1)
            #print(type(x_input))

            logging.info('input for model is "x_input":{X_input_shape}'.format(X_input_shape=x_input.shape))

            #converting into list
            logging.info('Converting X_input into a list')
            temp_input=list(x_input)
            temp_input=temp_input[0].tolist()




            prediction_days=100
            previous_days=150
            

            lst_output=[]
            n_steps=150
            i=0
            while(i<100):
                
                if(len(temp_input)>150):
                    #print(temp_input)
                    x_input=np.array(temp_input[1:])
                    print("{} day input {}".format(i,x_input))
                    x_input=x_input.reshape(1,-1)
                    x_input = x_input.reshape((1, n_steps, 1))
                    #print(x_input)
                    yhat = model.predict(x_input, verbose=0)
                    print("{} day output {}".format(i,yhat))
                    temp_input.extend(yhat[0].tolist())
                    temp_input=temp_input[1:]
                    #print(temp_input)
                    lst_output.extend(yhat.tolist())
                    i=i+1
                else:
                    x_input = x_input.reshape((1, n_steps,1))
                    yhat = model.predict(x_input, verbose=0)
                    print(yhat[0])
                    temp_input.extend(yhat[0].tolist())
                    print(len(temp_input))
                    lst_output.extend(yhat.tolist())
                    i=i+1

            
            day_new=np.arange(1,len(temp_input))
            day_pred=np.arange(len(temp_input),len(temp_input)+prediction_days)

            df=prediction_column.tolist()
            df.extend(lst_output)

        
            logging.info('plotting graph for prediction of "{prediction_days}" days'.format(prediction_days=previous_days))
            prediction_graph=df[len(prediction_column)-previous_days:]
            plt.plot(prediction_graph)
            plt.show()
            
            
            #return model
        except Exception as e:
            raise CustomException(e,sys)
        
        