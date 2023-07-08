import os,sys
import numpy as np
from src.logger import logging
from src.exception import CustomException
from dataclasses import dataclass
from src.components.data_transformation import Datatransformation

@dataclass
class ModelTrainer:
    def initiate_model_trainer(self):
        try:
           pass
        except Exception as e:
            raise CustomException(e,sys)
    