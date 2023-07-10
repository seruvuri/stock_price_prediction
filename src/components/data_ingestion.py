import os,sys
import pandas as pd


from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
from src.utils import *
from src.components.data_transformation import *
from src.components.model_trainer import *
from src.pipeline.predict_pipeline import *

@dataclass
class DataingestionConfig:
    raw_data_file_path:str=os.path.join('artifacts','raw.csv')
   
    

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataingestionConfig()

    def initiate_data_ingestion(self):
        try:
            logging.info('>>>>>>>>>>>>>>>>Data ingestion initiated<<<<<<<<<<<<<<<<<<<')
            json_dataset=api_data_extraction(ticker_name='aapl',startDate='2019-01-02',resampleFreq='1hour',token='a159a3a83b1754845d7353fbec1c9f2902d4a8e1')
            
            
            
            stock_df=pd.json_normalize(json_dataset)
            logging.info('converted json data to pandas dataframe')

            stock_df.to_csv(self.ingestion_config.raw_data_file_path,header=True,index=False)
            logging.info('saving raw data from api to "{file_path_name}" path'.format(' ',file_path_name=self.ingestion_config.raw_data_file_path))
            
            return stock_df
        
        except Exception as e:
            raise CustomException(e,sys)

if __name__=="__main__":
    ingestion_obj=DataIngestion()
    stock_dataset=ingestion_obj.initiate_data_ingestion()

    #combining data transformation
    transformation_obj=Datatransformation()
    train_dataset,test_dataset,close_df=transformation_obj.initiate_data_transformation(stock_dataframe=stock_dataset)
    time_step=150
    X_train,y_train=transformation_obj.create_dataset(dataset=train_dataset,time_step=time_step)
    X_test,y_test=transformation_obj.create_dataset(dataset=test_dataset,time_step=time_step)
    logging.info('created dataset for "LSTM" model input with "X_train" size:{X_train_size},"y_train" size:{y_train_size},"X_test" size:{X_test_size},"y_test" size:{y_test_size}'.format(X_train_size=X_train.shape,y_train_size=y_train.shape,X_test_size=X_test.shape,y_test_size=y_test.shape))

    #model trainer
    model_trainer_obj=ModelTrainer()
    Model=model_trainer_obj.initiate_model_trainer(X_train=X_train,X_test=X_test,y_train=y_train,y_test=y_test)

    #prediction pipeline
    Predict_pipline_obj=Predictpipeline()
    obj=Predict_pipline_obj.predict(model=Model,X_train=X_train,X_test=X_test,y_train=y_train,y_test=y_test,test_data=test_dataset,prediction_column=close_df)