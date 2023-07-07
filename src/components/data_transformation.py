import os,sys
from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass

@dataclass
class Datatransformationconfig:
    train_data_file_path=os.path.join('artifacts','train.csv')
    test_data_file_path=os.path.join('artifacts','test.csv')

class Datatransformation:
    def __init__(self):
        self.transformationconfig=Datatransformationconfig()
    
    def initiate_data_transformation(self,stock_dataframe):
        try:
            logging.info('data transformation initiated')
            
            # NUll check 
            logging.info('checking null values in dataset')
            Null_check=stock_dataframe.isnull().sum()

            if (Null_check.values>0).any():
                logging.info('Null values present in dataset. Check before Proceeding. Suggestion: use "SimpleImputer" while creating transformation pipeline')
            else:
                logging.info('No null values in dataset ')


        except Exception as e:
            raise CustomException(e,sys) 