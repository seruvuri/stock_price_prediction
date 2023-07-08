import os,sys
import pandas as pd


from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
from src.utils import *
from src.components.data_transformation import *

@dataclass
class DataingestionConfig:
    raw_data_file_path:str=os.path.join('artifacts','raw.csv')
   
    

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataingestionConfig()

    def initiate_data_ingestion(self):
        try:
            logging.info('data ingestion initiated')
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
    train_dataset,test_dataset=transformation_obj.initiate_data_transformation(stock_dataframe=stock_dataset)