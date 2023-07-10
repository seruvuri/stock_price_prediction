from src.logger import logging
from src.exception import CustomException
import os,sys
from dataclasses import dataclass
import math
from sklearn.metrics import mean_squared_error
import numpy as np
import matplotlib.pyplot as plt

@dataclass
class Predictpipeline:
    def predict(self,model,X_train,X_test,y_train,y_test,test_data,prediction_column):
        try:
            logging.info('>>>>>>>>>>>>>>>Predcit pipeline initiated<<<<<<<<<<<<<<<<')
            prediction_days=100

            logging.info('Predicting for X_train and X_test')
            train_predict=model.predict(X_train)
            test_predict=model.predict(X_test)

            logging.info('Transforming back to original form for calculating RMSE')

            train_predict=scaler.inverse_transform(train_predict)
            test_predict=scaler.inverse_transform(test_predict)

            train_RMSE=math.sqrt(mean_squared_error(y_train,train_predict))
            test_RMSE=math.sqrt(mean_squared_error(y_test,test_predict))
            logging.info('RMSE of "train data prediction":{train_rmse} and "test data prediction":{test_rmse}'.format(train_rmse=train_RMSE,test_rmse=test_RMSE))
            
            #considering 150 previous days for next 100 days predictions
            previous_days=150
            restofdays_in_dataset=len(test_data)-previous_days
            X_input=test_data[restofdays_in_dataset:].reshape(1,-1)

            logging.info('input for model is "X_input":{X_input_shape}'.format(X_input.shape))

            #converting into list
            logging.info('Converting X_input into a list')
            temp_input=list(X_input)
            temp_input=temp_input[0].tolist()


            lst_output=[]
            n_steps=150
            i=0
            while (i<100):
                #if pevious input is greater than 100 . the whole process will happen util we finish 100 days
                if(len(temp_input)>150):
                    #we shift the position
                    x_input=np.array(temp_input[1:])
                    logging.info("{} day input {}".format(i,x_input) )
                    x_input=x_input.reshape(1,-1)
                    x_input=x_input.reshape((1,n_steps,1))
                    yhat=model.predict(x_input,verbose=0)
                    logging.info("{} day output".format(i,yhat))
                    temp_input.extend(yhat[0].tolist())
                    temp_input=temp_input[1:]
                    lst_output.extend(yhat.tolist())
                    i=i+1
                else:
                    x_input=x_input.reshape(1,n_steps,1)
                    #passing 100 values to model 
                    yhat=model.predict(x_input,verbose=0)
                    #adding yhat value to previous values i.e temp_input.once we add value it will have 151 value then we shift from one postion and take from next(if condition)
                    temp_input.extend(yhat[0].tolist())
                    logging.info(len(temp_input))
                    #adding yhat value from predict to final output
                    lst_output.extend(yhat.tolist())
                    i=i+1

            
            day_new=np.arange(1,len(temp_input))
            day_pred=np.arange(len(temp_input),len(temp_input)+prediction_days)

            df=prediction_column.tolist()
            df.extend(lst_output)
            logging.info('plotting graph for prediction of "{prediction_days}" days'.format(prediction_days=previous_days))
            plt.plot(df[len(prediction_column)-previous_days:])
            plt.show()
        except Exception as e:
            raise CustomException(e,sys)